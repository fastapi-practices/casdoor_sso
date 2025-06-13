#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydantic import EmailStr, Field, HttpUrl

from backend.app.admin.schema.user import AuthSchemaBase


class AddSsoUserParam(AuthSchemaBase):
    """添加 OAuth2 用户参数"""

    nickname: str | None = Field(None, description='昵称')
    email: EmailStr = Field(description='邮箱')
    avatar: HttpUrl | None = Field(None, description='头像地址')
