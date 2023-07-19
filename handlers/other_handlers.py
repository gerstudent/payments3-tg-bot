from aiogram import Router
from aiogram.types import Message

router = Router()


@router.message()
async def send_error_message(message: Message):
    await message.answer('Такой команды не существует')
