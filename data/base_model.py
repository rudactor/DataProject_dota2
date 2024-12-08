from pydantic import BaseModel

class TopHeroesRequest(BaseModel):
    top_n: int

class NewRecord(BaseModel):
    hero_id: int
    hero_name: str
    chat_message: str
