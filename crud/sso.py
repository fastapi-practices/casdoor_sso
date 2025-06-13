#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import bcrypt

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import Role, User
from backend.common.security.jwt import get_hash_password
from backend.plugin.casdoor_sso.schema.sso import AddSsoUserParam


class CRUDSso(CRUDPlus[User]):
    """用户数据库操作类"""

    async def add_by_sso(self, db: AsyncSession, obj: AddSsoUserParam) -> None:
        """
        通过 SSO 添加用户

        :param db: 数据库会话
        :param obj: 注册用户参数
        :return:
        """
        salt = bcrypt.gensalt()
        obj.password = get_hash_password(obj.password, salt)
        dict_obj = obj.model_dump()
        dict_obj.update({'is_staff': True, 'salt': salt})
        new_user = self.model(**dict_obj)

        stmt = select(Role)
        role = await db.execute(stmt)
        new_user.roles = [role.scalars().first()]  # 默认绑定第一个角色

        db.add(new_user)
        await db.flush()


sso_dao: CRUDSso = CRUDSso(User)
