from Models.user import User
from config import db
from sqlalchemy import select, update, delete


class UserRepository:


    
    @staticmethod
    async def create(user: User):
        async with db as session:
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    @staticmethod
    async def get_all():
        async with db as session:
            query = select(User)
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def get_by_id(id: int):
        async with db as session:
            query = select(User).where(User.id == id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @staticmethod
    async def update(id: int, user_data):
        async with db as session:
            # We locate the existing note
            query = select(User).where(User.id == id)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            
            if user:
                # We expect note_data to be a dict
                for key, value in user_data.items():
                    setattr(user, key, value)
                
                session.add(user)
                await session.commit()
                await session.refresh(user)
                return user
            return None

    @staticmethod
    async def delete(id: int):
        async with db as session:
            query = select(User).where(User.id == id)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            
            if user:
                await session.delete(user)
                await session.commit()
                return True
            return False

    @staticmethod
    async def get_by_email(email: str):
        async with db as session:
            query = select(User).where(User.email == email)
            result = await session.execute(query)
            return result.scalar_one_or_none()
