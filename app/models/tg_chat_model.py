class TgChatModel:
    def __init__(self, chat_id: int, title: str, joined_time: str, language: str, badwords: str, actions: str, data: dict):
        self.chat_id = chat_id
        self.title = title
        self.joined_time = joined_time
        self.language = language
        self.badwords = badwords
        self.actions = actions
        self.data = data

    def to_dict(self):
        return {
            "chat_id": self.chat_id,
            "title": self.title,
            "joined_time": self.joined_time,
            "language": self.language,
            "badwords": self.badwords,
            "actions": self.actions,
            "data": self.data
        }

    @staticmethod
    def from_dict(data: dict):
        return TgChatModel(
            chat_id=data.get("chat_id"),
            title=data.get("title"),
            joined_time=data.get("joined_time"),
            language=data.get("language"),
            badwords=data.get("badwords"),
            actions=data.get("actions"),
            data=data.get("data", {})
        )