import json
import os
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

from utils.train_checker import check_if_trained, save_trained_file

chatbot = ChatBot(
    "Gujuferro",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database_uri="postgresql+psycopg2://postgres:zamon@localhost/postgres"
)

trainer = ListTrainer(chatbot)

data_dir = "resources/json"

for filename in os.listdir(data_dir):
    file_status = check_if_trained(filename)
    if file_status:
        continue
    if filename.endswith(".json"):
        filepath = os.path.join(data_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            pairs = json.load(f)
            for pair in pairs:
                input_text = pair.get("input")
                output_text = pair.get("output")

                if isinstance(input_text, str) and isinstance(output_text, str):
                    trainer.train([input_text, output_text])
                else:
                    print(f"⚠️ Noto‘g‘ri ma'lumot: {input_text} - {output_text} (input yoki output noto‘g‘ri formatda)")
        save_trained_file(filename)


def get_chat_bot() -> ChatBot:
    return chatbot
