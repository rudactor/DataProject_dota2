import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
import os
import pandas as pd

from analyse import DotaDataAnalysis
from routes import Routes
import data.cfg as cfg

class DotaBackend:
    def __init__(self):
        load_dotenv()
        self.app = FastAPI()
        self.analysis = DotaDataAnalysis()
        Routes(self.app, self)

    def add_new_record(self, hero_id: int, hero_name: str, chat_message: str) -> bool:
        record = {
            "hero_id": hero_id,
            "hero_name": hero_name,
            "chat_message": chat_message
        }
        try:
            if not os.path.exists(cfg.NEW_RECORDS_PATH):
                df = pd.DataFrame([record])
                df.to_csv(cfg.NEW_RECORDS_PATH, index=False)
            else:
                df = pd.DataFrame([record])
                df.to_csv(cfg.NEW_RECORDS_PATH, mode='a', header=False, index=False)
            return True
        except Exception as e:
            print(e)
            return False

    def run(self):
        uvicorn.run(self.app, host='0.0.0.0', port=8000)

backend = DotaBackend()
app = backend.app

if __name__ == '__main__':
    backend.run()
