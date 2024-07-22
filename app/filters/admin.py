from typing import Any, Dict
from aiogram.filters import BaseFilter
from aiogram.types import Message

from app.repository.admin import AdminRepo

class AdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user:
            return await AdminRepo.is_admin(message.from_user.id)
        return False
        
