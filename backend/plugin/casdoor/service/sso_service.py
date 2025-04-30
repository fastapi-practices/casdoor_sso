#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any

from fast_captcha import text_captcha
from fastapi import BackgroundTasks, Request, Response

from backend.app.admin.conf import admin_settings
from backend.app.admin.crud.crud_user import user_dao
from backend.app.admin.schema.token import GetLoginToken
from backend.app.admin.schema.user import RegisterUserParam
from backend.app.admin.service.login_log_service import login_log_service
from backend.common.enums import LoginLogStatusType
from backend.common.security import jwt
from backend.core.conf import settings
from backend.database.db import async_db_session
from backend.database.redis import redis_client
from backend.utils.timezone import timezone


class SSOService:
    """Casdoor SSO 服务类"""

    @staticmethod
    async def create_with_login(
        *,
        request: Request,
        response: Response,
        background_tasks: BackgroundTasks,
        user: dict[str, Any],
    ) -> GetLoginToken | None:
        """
        创建 SSO 用户并登录

        :param request: FastAPI 请求对象
        :param response: FastAPI 响应对象
        :param background_tasks: FastAPI 后台任务
        :param user: SSO 用户信息
        :return:
        """
        async with async_db_session.begin() as db:
            # 获取 Casdoor 平台用户信息
            sso_username = user.get('name')
            sso_nickname = user.get('displayName')
            sso_email = user.get('email')
            sys_user = await user_dao.check_email(db, sso_email)
            if not sys_user:
                sys_user = await user_dao.get_by_username(db, sso_username)
                if sys_user:
                    sso_username = f'{sso_username}#{text_captcha(5)}'
                sys_user = await user_dao.get_by_nickname(db, sso_nickname)
                if sys_user:
                    sso_nickname = f'{sso_nickname}#{text_captcha(5)}'
                new_sys_user = RegisterUserParam(
                    username=sso_username,
                    password=None,
                    nickname=sso_nickname,
                    email=sso_email,
                )
                await user_dao.create(db, new_sys_user, social=True)
                await db.flush()
                sys_user = await user_dao.check_email(db, sso_email)
            # 创建 token
            sys_user_id = sys_user.id
            access_token = await jwt.create_access_token(
                str(sys_user_id),
                sys_user.is_multi_login,
                # extra info
                username=sys_user.username,
                nickname=sys_user.nickname,
                last_login_time=timezone.t_str(timezone.now()),
                ip=request.state.ip,
                os=request.state.os,
                browser=request.state.browser,
                device=request.state.device,
            )
            refresh_token = await jwt.create_refresh_token(str(sys_user_id), multi_login=sys_user.is_multi_login)
            await user_dao.update_login_time(db, sys_user.username)
            await db.refresh(sys_user)
            login_log = dict(
                db=db,
                request=request,
                user_uuid=sys_user.uuid,
                username=sys_user.username,
                login_time=timezone.now(),
                status=LoginLogStatusType.success.value,
                msg='登录成功（SSO）',
            )
            background_tasks.add_task(login_log_service.create, **login_log)
            await redis_client.delete(f'{admin_settings.CAPTCHA_LOGIN_REDIS_PREFIX}:{request.state.ip}')
            response.set_cookie(
                key=settings.COOKIE_REFRESH_TOKEN_KEY,
                value=refresh_token.refresh_token,
                max_age=settings.COOKIE_REFRESH_TOKEN_EXPIRE_SECONDS,
                expires=timezone.f_utc(refresh_token.refresh_token_expire_time),
                httponly=True,
            )
            data = GetLoginToken(
                access_token=access_token.access_token,
                access_token_expire_time=access_token.access_token_expire_time,
                user=sys_user,  # type: ignore
                session_uuid=access_token.session_uuid,
            )
            return data


sso_service: SSOService = SSOService()
