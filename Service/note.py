from Models.note import Note
from Repository.note import NoteRepository
from schema import NoteInput, NoteType
from dataclasses import asdict

class NoteService:

    @staticmethod
    async def add_note(note: NoteInput):
        
        note = Note( **asdict(note))
        await NoteRepository.create(note)
        return NoteType(**note.dict())

    @staticmethod
    async def get_all():
        notes = await NoteRepository.get_all()
        return [NoteType(**note.dict()) for note in notes]

    @staticmethod
    async def get_by_id(id: int):
        note = await NoteRepository.get_by_id(id)
        return NoteType(**note.dict()) if note else None

    @staticmethod
    async def delete(id: int):
        return await NoteRepository.delete(id)

    @staticmethod
    async def update(id: int, note: NoteInput):
        note = await NoteRepository.update(id, asdict(note))
        return NoteType(**note.dict()) if note else None