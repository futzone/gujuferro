from aiogram import Bot
from aiogram.types import Message
from app.chat.app import get_chat_bot, train_bot
from app.chat.trainer import train_new_conversation
from app.services.badword_services import check_message_for_badwords
from bot.controller.message_controller import MessageController
from bot.styles.text_styles import to_bold


async def on_start_training_handler(message: Message):
    if message.text is None or message.text != 'guju_start_training':
        return
    train_bot()
    await message.reply('Training completed!')


async def text_handler(bot: Bot, message: Message):
    if message.text is None or message.text.startswith('/'):
        return

    message_text = message.text
    badwords_list = check_message_for_badwords(message_text)

    if len(badwords_list) != 0:
        await bot.send_message(
            chat_id=message.chat.id,
            text=to_bold(f"{message.from_user.first_name}, iltimos, haqoratli so'zlar ishlatmang!"),
            parse_mode='html'
        )
        await MessageController.delete(message=message)
        return

    chat_bot = get_chat_bot()
    response = chat_bot.get_response(message_text)
    await message.reply(f'{response}')

    try:
        if message.reply_to_message is not None and message.reply_to_message.text is not None:
            train_new_conversation(message.reply_to_message.text, message_text)
            print('trained')
    except:
        pass
