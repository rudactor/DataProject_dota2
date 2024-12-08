import threading
import time
import sys
import uvicorn
import streamlit.web.cli as stcli

def run_frontend():
    sys.argv = ["streamlit", "run", "frontend.py", "--server.port=8501", "--server.address=0.0.0.0"]
    stcli.main()

def run_backend():
    uvicorn.run("backend:app", host="0.0.0.0", port=8000, reload=False)

if __name__ == "__main__":
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()
    time.sleep(2)
    run_frontend()
