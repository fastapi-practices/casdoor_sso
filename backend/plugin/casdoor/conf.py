#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from backend.core.path_conf import BASE_PATH


class CasdoorSettings(BaseSettings):
    """casdoor Settings"""

    model_config = SettingsConfigDict(
        env_file=f'{BASE_PATH}/.env',
        secrets_dir='',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    # Dir secrets
    CASDOOR_CERTIFICATE: str

    # Env casdoor
    CASDOOR_CLIENT_ID: str
    CASDOOR_CLIENT_SECRET: str

    # Casdoor
    CASDOOR_ENDPOINT: str = 'http://localhost:8080'
    CASDOOR_ORG_NAME: str = 'casdoor'
    CASDOOR_APPLICATION_NAME: str = 'Casdoor'
    CASDOOR_FRONT_ENDPOINT: str = 'http://localhost:8080'  # Casdoor UI 地址
    CASDOOR_FRONTEND_REDIRECT_URI: str = ''  # 成功后的重定向 URI，可参考：backend/app/admin/conf.py


@lru_cache
def get_casdoor_settings() -> CasdoorSettings:
    """获取 casdoor 配置"""
    return CasdoorSettings()


casdoor_settings = get_casdoor_settings()
