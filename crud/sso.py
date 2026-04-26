from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy_crud_plus import CRUDPlus

from backend.app.admin.model import Role, User
from backend.app.admin.model.m2m import user_role
from backend.app.admin.schema.user import AddUserRoleParam
from backend.common.enums import StatusType
from backend.common.exception import errors
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
        dict_obj = obj.model_dump()
        dict_obj.update({'is_staff': True, 'salt': None})
        new_user = self.model(**dict_obj)
        db.add(new_user)
        await db.flush()

        role_stmt = select(Role).where(Role.status == StatusType.enable)
        result = await db.execute(role_stmt)
        role = result.scalars().first()  # 默认绑定第一个可用角色
        if role is None:
            raise errors.NotFoundError(msg='未找到可用角色，请联系系统管理员')

        user_role_stmt = insert(user_role).values(AddUserRoleParam(user_id=new_user.id, role_id=role.id).model_dump())
        await db.execute(user_role_stmt)


sso_dao: CRUDSso = CRUDSso(User)
