from typing import Any
from fastapi import APIRouter, FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from data.base_model import TopHeroesRequest, NewRecord
import numpy as np

class Routes:
    def __init__(self, app: FastAPI, backend_instance: Any) -> None:
        self.app = app
        self.backend = backend_instance
        self.router = APIRouter()
        self.setup_cors()
        self.setup_routes()

    def setup_cors(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        )

    def setup_routes(self):

        @self.router.get("/api/")
        async def main() -> dict:
            return {"message": "Hello from Dota Data FastAPI."}

        @self.router.get("/api/clean_data/")
        async def clean_data():
            return {"message": "Data cleaning is not implemented yet."}

        @self.router.get("/api/top_heroes/")
        async def top_heroes(top_n: int = Query(10, description="Number of top heroes")):
            data = self.backend.analysis.get_top_heroes(top_n=top_n)
            return data.to_dict(orient='records')

        @self.router.get("/api/chat_activity/")
        async def chat_activity():
            data = self.backend.analysis.analyze_chat_activity()
            return data.to_dict(orient='records')

        @self.router.get("/api/bad_message_percentage/")
        async def bad_message_percentage():
            percentage = self.backend.analysis.calculate_bad_message_percentage()
            return {"bad_message_percentage": percentage}

        @self.router.get("/api/matches_stats/")
        async def matches_stats():
            stats = self.backend.analysis.get_matches_stats()
            return stats

        @self.router.post("/api/add_record/")
        async def add_record(record: NewRecord):
            success = self.backend.add_new_record(record.hero_id, record.hero_name, record.chat_message)
            if success:
                return {"message": "Record added successfully!", "data": record.dict()}
            else:
                raise HTTPException(status_code=500, detail="Could not save the record.")
            
        @self.router.get("/api/boots_compare/")
        async def boots_compare():
            df_boots_compare = self.backend.analysis.get_boots_compare_data()
            df_boots_compare = df_boots_compare.replace({np.nan: None})
            return df_boots_compare.to_dict(orient='records')

        @self.router.get("/api/hero_gpm_scatter_data/")
        async def hero_gpm_scatter_data():
            df_hero_gpm = self.backend.analysis.get_hero_gpm_data()
            # Заменяем NaN на None
            df_hero_gpm = df_hero_gpm.replace({np.nan: None})
            return df_hero_gpm.to_dict(orient='records')

        self.app.include_router(self.router)
