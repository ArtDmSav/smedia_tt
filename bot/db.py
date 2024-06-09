from bot.models import User, async_session
from sqlalchemy import select, update
from datetime import datetime


async def create_user(user_id: int):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(User).where(User.id == user_id))
            user = result.scalar()
            if user is None:
                now = datetime.now()
                user = User(
                    id=user_id,
                    created_at=now,
                    status='alive',
                    last_updated_at=now,
                    steps=0,
                    steps_updated_at=now
                )
                session.add(user)
                await session.commit()
            return user


async def update_user_status(user_id: int, status: str):
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                update(User).where(User.id == user_id).values(status=status, last_updated_at=datetime.now())
            )
            await session.commit()


async def update_user_steps(user_id: int, steps: int):
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                update(User).where(User.id == user_id).values(steps=steps, steps_updated_at=datetime.now())
            )
            await session.commit()
