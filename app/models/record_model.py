class RecordModel:
    def __init__(self, id: int, chat_id: int, user_id: int, created_date: str, type: str, data: str, source: str):
        self.id = id
        self.chat_id = chat_id
        self.user_id = user_id
        self.created_date = created_date
        self.type = type
        self.data = data
        self.source = source

    def to_dict(self):
        return {
            "id": self.id,
            "chat_id": self.chat_id,
            "user_id": self.user_id,
            "created_date": self.created_date,
            "type": self.type,
            "data": self.data,
            "source": self.source
        }

    @staticmethod
    def from_dict(data: dict):
        return RecordModel(
            id=data.get("id"),
            chat_id=data.get("chat_id"),
            user_id=data.get("user_id"),
            created_date=data.get("created_date"),
            type=data.get("type"),
            data=data.get("data"),
            source=data.get("source")
        )