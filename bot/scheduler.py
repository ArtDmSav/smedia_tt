import asyncio
from datetime import datetime, timedelta
from sqlalchemy import select
from pyrogram import Client, errors

from bot.db import update_user_steps, update_user_status
from bot.models import User, async_session
from bot.config import API_HASH, API_ID, WAIT_TIME_3, WAIT_TIME_2, WAIT_TIME_1, TRIGGER_FOR_MISS_MSG, \
    TRIGGERS_FOR_FINISHED, MSG_HISTORY_LIMIT, CHECK_TIME, FINISHED, USER_ERROR, MY_ACCOUNT_2

app_2 = Client(
    MY_ACCOUNT_2,
    api_id=API_ID,
    api_hash=API_HASH
)


async def schedule_messages() -> None:
    while True:
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(select(User).where(User.steps.in_([0, 1, 2])))
                users = result.scalars().all()
                for user in users:
                    now = datetime.now()
                    try:
                        if user.steps == 0 and (now - user.steps_updated_at) >= timedelta(seconds=WAIT_TIME_1):
                            if await check_trigger_word(user.id):
                                await update_user_steps(user_id=user.id, steps=FINISHED)
                                await update_user_status(user.id, "finished")
                            else:
                                await app_2.send_message(user.id, "Текст1")
                                await update_user_steps(user.id, 1)
                        elif user.steps == 1 and (now - user.steps_updated_at) >= timedelta(seconds=WAIT_TIME_2):
                            if await check_trigger_word(user.id):
                                await update_user_steps(user_id=user.id, steps=FINISHED)
                                await update_user_status(user.id, "finished")
                            elif not await check_trigger_miss_msg(user.id):
                                await app_2.send_message(user.id, "Текст2")
                            await update_user_steps(user.id, 2)
                        elif user.steps == 2 and (now - user.steps_updated_at) >= timedelta(seconds=WAIT_TIME_3):
                            if await check_trigger_word(user.id):
                                await update_user_steps(user_id=user.id, steps=FINISHED)
                                await update_user_status(user.id, "finished")
                            else:
                                await app_2.send_message(user.id, "Текст3")
                                await update_user_steps(user.id, 3)
                                await update_user_status(user.id, "finished")

                    except errors.UserIsBlocked:
                        await update_user_status(user.id, "dead")
                        await update_user_steps(user.id, USER_ERROR)

                    except errors.UserDeactivated:
                        await update_user_status(user.id, "dead")
                        await update_user_steps(user.id, USER_ERROR)

                    except errors.PeerIdInvalid:
                        await update_user_status(user.id, "dead")
                        await update_user_steps(user.id, USER_ERROR)

                    except Exception as e:
                        await update_user_status(user.id, "dead")
                        await update_user_steps(user.id, USER_ERROR)

        await asyncio.sleep(CHECK_TIME)  # Ожидание CHECK_TIME секунд перед следующим циклом


async def check_trigger_miss_msg(user_id: int) -> bool:
    messages = await get_message_history(user_id)
    for message in messages:
        if message.from_user.is_self:
            if TRIGGER_FOR_MISS_MSG in str(message.text).lower():
                return True
    return False


async def check_trigger_word(user_id: int) -> bool:
    messages = await get_message_history(user_id)
    for message in messages:
        if message.from_user.is_self:
            for trigger_word in TRIGGERS_FOR_FINISHED:
                if trigger_word in str(message.text).lower():
                    return True
    return False


async def get_message_history(user_id: int) -> list:
    messages = []
    async for message in app_2.get_chat_history(user_id, limit=MSG_HISTORY_LIMIT):
        messages.append(message)
    return messages


async def main():
    await app_2.start()
    try:
        await schedule_messages()
    except asyncio.CancelledError:
        pass
    finally:
        await app_2.stop()

if __name__ == "__main__":
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Остановка пользователем")
