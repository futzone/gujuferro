import json
import os

from chatterbot import ChatBot

chatbot = ChatBot(
    "Gujuferro",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database_uri="postgresql+psycopg2://postgres:zamon@localhost/postgres"
)

# from chatterbot.trainers import ListTrainer
#
# trainer = ListTrainer(chatbot)
#
# data_dir = "resources/json"
#
# for filename in os.listdir(data_dir):
#     if filename.endswith(".json"):
#         filepath = os.path.join(data_dir, filename)
#         with open(filepath, "r", encoding="utf-8") as f:
#             pairs = json.load(f)
#             for pair in pairs:
#                 if pair.get("input", None) is not None and pair.get("output", None) is not None:
#                     trainer.train([pair["input"], pair["output"]])
#         print(f"✅ Trained: {filename}")

response = chatbot.get_response('Nima gaplar')

print(response)
