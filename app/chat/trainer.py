from chatterbot.trainers import ListTrainer
from app.chat.app import get_chat_bot

chat_bot = get_chat_bot()
trainer = ListTrainer(chat_bot)


def train_new_conversation(input_text, output_text):
    trainer.train([input_text, output_text])
