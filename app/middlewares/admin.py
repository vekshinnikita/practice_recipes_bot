from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable

from app.repository.admin import AdminRepo

class AdminMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any]) -> Any:
        if event.from_user:
            data['is_admin'] = await AdminRepo.is_admin(event.from_user.id)
        else:
            data['is_admin'] = False
        
        return await handler(event, data)