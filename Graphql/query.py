import strawberry
from Service.note import NoteService
from schema import NoteType
from Middleware.JWTBearer import IsAuthenticated

@strawberry.type
class Query:

    @strawberry.field
    def hello(self) -> str:
        return "Hello, world!"
    
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def get_all_notes(self, limit: int = 10, offset: int = 0) -> list[NoteType]:
        return await NoteService.get_all(limit, offset)

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def get_note_by_id(self, id: int) -> NoteType | None:
        return await NoteService.get_by_id(id)