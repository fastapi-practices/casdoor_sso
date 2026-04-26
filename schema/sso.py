from pydantic import Field

from backend.app.admin.schema.user import AddOAuth2UserParam
from backend.common.schema import CustomEmailStr


class AddSsoUserParam(AddOAuth2UserParam):
    """添加 SSO 用户参数"""

    email: CustomEmailStr = Field(description='邮箱')
