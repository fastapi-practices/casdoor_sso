from fastapi import APIRouter, BackgroundTasks, Depends, Request, Response
from starlette.responses import RedirectResponse

from backend.common.limiter import rate_limit
from backend.common.response.response_schema import ResponseSchemaModel, response_base
from backend.core.conf import settings
from backend.database.db import CurrentSessionTransaction
from backend.plugin.casdoor_sso.service.casdoor_client import casdoor_client, get_access_token
from backend.plugin.casdoor_sso.service.sso_service import sso_service

router = APIRouter()


@router.get('', summary='获取 Casdoor SSO 授权链接')
async def casdoor_sso(request: Request) -> ResponseSchemaModel[str]:
    sso_url = casdoor_client.get_auth_link(redirect_uri=f'{request.url}/callback')
    return response_base.success(data=sso_url)


@router.get(
    '/callback',
    summary='Casdoor SSO 授权自动重定向',
    description='Casdoor SSO 授权后，自动重定向到当前地址并获取用户信息，通过用户信息自动创建系统用户',
    dependencies=[Depends(rate_limit('5/minute'))],
)
async def casdoor_sso_login(
    db: CurrentSessionTransaction,
    request: Request,
    response: Response,
    background_tasks: BackgroundTasks,
) -> RedirectResponse:
    code = request.query_params.get('code')
    _state = request.query_params.get('state')
    token = await casdoor_client.get_oauth_token(code)
    access_token = get_access_token(token)
    user = casdoor_client.parse_jwt_token(access_token)
    data = await sso_service.create_with_login(
        db=db,
        request=request,
        response=response,
        background_tasks=background_tasks,
        user=user,
    )
    return RedirectResponse(
        url=f'{settings.CASDOOR_SSO_FRONTEND_REDIRECT_URI}?access_token={data.access_token}&session_uuid={data.session_uuid}'
    )
