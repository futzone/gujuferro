class TgUserModel:
    def __init__(self, telegram_id, user_id, fullname, created_date, state, chat_id, status, language):
        self.telegram_id = telegram_id
        self.user_id = user_id
        self.fullname = fullname
        self.created_date = created_date
        self.state = state
        self.chat_id = chat_id
        self.status = status
        self.language = language

    def to_map(self):
        return {
            "telegram_id": self.telegram_id,
            "user_id": self.user_id,
            "fullname": self.fullname,
            "created_date": f"{self.created_date}",
            "state": self.state,
            "chat_id": self.chat_id,
            "status": self.status,
            "language": self.language
        }
