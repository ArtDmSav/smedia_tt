from pyrogram import Client, filters
from bot.config import API_ID, API_HASH, MY_ACCOUNT
from bot.db import create_user

app = Client(
    MY_ACCOUNT,
    api_id=int(API_ID),
    api_hash=API_HASH
)


@app.on_message(filters.text & filters.private)
async def handle_message(client, message):
    if not message.from_user.is_self:
        await create_user(message.from_user.id)


if __name__ == "__main__":
    app.run()
