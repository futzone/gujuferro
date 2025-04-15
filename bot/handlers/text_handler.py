from aiogram import Bot
from aiogram.types import Message
from app.chat.app import get_chat_bot
from app.services.badword_services import check_message_for_badwords
from bot.controller.message_controller import MessageController
from bot.styles.text_styles import to_bold


async def text_handler(bot: Bot, message: Message):
    if message.text is None:
        return

    message_text = message.text
    badwords_list = check_message_for_badwords(message_text)

    if len(badwords_list) != 0:
        await bot.send_message(
            chat_id=message.chat.id,
            text=to_bold(f"{message.from_user.first_name}, iltimos, haqoratli so'zlar ishlatmang!")
        )
        await MessageController.delete(message=message)
        return

    response = get_chat_bot()
    await message.reply(response)
