import aiogram.utils.markdown as fmt


def to_bold(text: str):
    return f"<b>{fmt.hbold(f'{text}')}</b>"


def to_mono(text: str):
    return f"<code>{fmt.hbold(f'{text}')}</code>"