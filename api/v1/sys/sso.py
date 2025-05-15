#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from casdoor import AsyncCasdoorSDK
from fastapi import APIRouter, BackgroundTasks, Depends, Request, Response
from fastapi_limiter.depends import RateLimiter
from starlette.responses import RedirectResponse

from backend.common.response.response_schema import ResponseSchemaModel, response_base
from backend.core.conf import settings
from backend.plugin.fba_casdoor.service.sso_service import sso_service

router = APIRouter()

sdk = AsyncCasdoorSDK(
    endpoint=settings.CASDOOR_ENDPOINT,
    client_id=settings.CASDOOR_CLIENT_ID,
    client_secret=settings.CASDOOR_CLIENT_SECRET,
    certificate=settings.CASDOOR_CERTIFICATE,
    org_name=settings.CASDOOR_ORG_NAME,
    application_name=settings.CASDOOR_APPLICATION_NAME,
    front_endpoint=settings.CASDOOR_FRONT_ENDPOINT,
)


@router.get('', summary='获取 Casdoor SSO 授权链接')
async def casdoor_sso(request: Request) -> ResponseSchemaModel[str]:
    sso_url = await sdk.get_auth_link(redirect_uri=f'{request.url}/callback')
    return response_base.success(data=sso_url)


@router.get(
    '/callback',
    summary='Casdoor SSO 授权自动重定向',
    description='Casdoor SSo 授权后，自动重定向到当前地址并获取用户信息，通过用户信息自动创建系统用户',
    dependencies=[Depends(RateLimiter(times=5, minutes=1))],
)
async def casdoor_sso_login(request: Request, response: Response, background_tasks: BackgroundTasks):
    code = request.query_params.get('code')
    _state = request.query_params.get('state')
    token = await sdk.get_oauth_token(code)
    access_token = token['access_token']
    user = sdk.parse_jwt_token(access_token)
    data = await sso_service.create_with_login(
        request=request,
        response=response,
        background_tasks=background_tasks,
        user=user,
    )
    return RedirectResponse(url=f'{settings.CASDOOR_FRONTEND_REDIRECT_URI}?access_token={data.access_token}')
