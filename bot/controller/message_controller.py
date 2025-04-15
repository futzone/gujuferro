from aiogram.types import Message


class MessageController:
    @staticmethod
    async def delete(message: Message):
        try:
            await message.delete()
        except:
            pass
