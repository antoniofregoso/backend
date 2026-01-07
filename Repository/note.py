from sqlmodel import select
from config import db
from Models.note import Note

class NoteRepository:
    
    @staticmethod
    async def create(note: Note):
        async with db as session:
            session.add(note)
            await session.commit()
            await session.refresh(note)
            return note

    @staticmethod
    async def get_all(limit: int = 10, offset: int = 0):
        async with db as session:
            query = select(Note).offset(offset).limit(limit)
            result = await session.execute(query)
            return result.scalars().all()

    @staticmethod
    async def get_by_id(id: int):
        async with db as session:
            query = select(Note).where(Note.id == id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @staticmethod
    async def update(id: int, note_data):
        async with db as session:
            # We locate the existing note
            query = select(Note).where(Note.id == id)
            result = await session.execute(query)
            note = result.scalar_one_or_none()
            
            if note:
                # We expect note_data to be a dict
                for key, value in note_data.items():
                    setattr(note, key, value)
                
                session.add(note)
                await session.commit()
                await session.refresh(note)
                return note
            return None

    @staticmethod
    async def delete(id: int):
        async with db as session:
            query = select(Note).where(Note.id == id)
            result = await session.execute(query)
            note = result.scalar_one_or_none()
            
            if note:
                await session.delete(note)
                await session.commit()
                return True
            return False