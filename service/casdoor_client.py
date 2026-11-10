"""Casdoor OIDC 授权码流程客户端

插件不再依赖 casdoor 包：它对 PyJWT、cryptography、requests 的版本约束会把宿主的
安全依赖回退到存在已知漏洞的旧版本（PyJWT 2.13.0 起才修复算法混淆等漏洞），
因此在插件内实现所需的最小 OIDC 流程，行为与 casdoor SDK 保持一致
"""

import base64

from typing import Any
from urllib.parse import urlencode

import httpx
import jwt

from cryptography import x509

from backend.common.exception import errors
from backend.core.conf import settings

# Casdoor 签发的令牌使用 RS256
_ALGORITHMS = ('RS256',)


class CasdoorClient:
    """Casdoor OIDC 客户端"""

    def __init__(
        self,
        *,
        endpoint: str,
        client_id: str,
        client_secret: str,
        certificate: str,
        application_name: str,
        front_endpoint: str,
    ) -> None:
        """
        初始化客户端

        :param endpoint: Casdoor 服务端地址
        :param client_id: 应用 Client ID
        :param client_secret: 应用 Client Secret
        :param certificate: 应用证书 PEM
        :param application_name: 应用名称
        :param front_endpoint: Casdoor 前端地址
        :return:
        """
        self.endpoint = endpoint.rstrip('/')
        self.front_endpoint = front_endpoint.rstrip('/')
        self.client_id = client_id
        self.client_secret = client_secret
        self.certificate = certificate
        self.application_name = application_name

    def get_auth_link(self, redirect_uri: str) -> str:
        """
        获取授权链接

        :param redirect_uri: 授权回调地址
        :return:
        """
        query = urlencode({
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': redirect_uri,
            'scope': 'read',
            'state': self.application_name,
        })
        return f'{self.front_endpoint}/login/oauth/authorize?{query}'

    def _headers(self) -> dict[str, str]:
        """
        构造请求头

        :return:
        """
        basic_auth = base64.b64encode(f'{self.client_id}:{self.client_secret}'.encode()).decode()
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Basic {basic_auth}',
        }

    async def get_oauth_token(self, code: str) -> dict[str, Any]:
        """
        用授权码换取访问令牌

        :param code: 授权码
        :return:
        """
        payload = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
        }
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f'{self.endpoint}/api/login/oauth/access_token',
                    data=payload,
                    headers=self._headers(),
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            raise errors.ServerError(msg='Casdoor 授权失败，请稍后重试') from e

    def parse_jwt_token(self, token: str) -> dict[str, Any]:
        """
        解析 Casdoor 签发的访问令牌

        :param token: 访问令牌
        :return:
        """
        if not self.certificate:
            raise errors.ServerError(msg='Casdoor 证书未配置，无法校验访问令牌')
        try:
            certificate = x509.load_pem_x509_certificate(self.certificate.encode())
        except ValueError as e:
            raise errors.ServerError(msg='Casdoor 证书格式非法') from e
        try:
            return jwt.decode(
                token,
                certificate.public_key(),
                algorithms=list(_ALGORITHMS),
                audience=self.client_id,
            )
        except jwt.PyJWTError as e:
            raise errors.ServerError(msg='Casdoor 访问令牌校验失败') from e


def get_access_token(token_payload: dict[str, Any]) -> str:
    """
    从 Casdoor 响应中取出访问令牌

    :param token_payload: Casdoor 响应体
    :return:
    """
    access_token = token_payload.get('access_token') or token_payload.get('accessToken')
    if not access_token:
        raise errors.ServerError(msg='Casdoor 未返回访问令牌')
    return access_token


casdoor_client = CasdoorClient(
    endpoint=settings.CASDOOR_SSO_ENDPOINT,
    client_id=settings.CASDOOR_SSO_CLIENT_ID,
    client_secret=settings.CASDOOR_SSO_CLIENT_SECRET,
    certificate=settings.CASDOOR_SSO_CERTIFICATE,
    application_name=settings.CASDOOR_SSO_APPLICATION_NAME,
    front_endpoint=settings.CASDOOR_SSO_ACCESS_ENDPOINT,
)
