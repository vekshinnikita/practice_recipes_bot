

from app.repository.admin import AdminRepo


class AdminService:

    @classmethod
    async def set_admin(cls, tg_id: int):
        await AdminRepo.set_admin(tg_id=tg_id)
