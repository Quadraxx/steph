import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("steph-api")


class StephAPI:
    def __init__(self, assistant=None, config=None):
        self.assistant = assistant
        self.config = config
        self.app = None
        self.server = None

    def start(self, host: str = "0.0.0.0", port: int = 8741):
        try:
            from fastapi import FastAPI, HTTPException
            from fastapi.middleware.cors import CORSMiddleware
            from pydantic import BaseModel
            import uvicorn
        except ImportError:
            log.error("fastapi/uvicorn not installed. Run: pip install fastapi uvicorn")
            return

        app = FastAPI(
            title="STEPH API",
            version="0.1.0",
            description="STEPH - AI Desktop Commander API",
        )

        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        class ExecuteRequest(BaseModel):
            command: str

        class ExecuteResponse(BaseModel):
            status: str
            result: str

        @app.get("/")
        async def root():
            return {"name": "STEPH", "version": "0.1.0", "status": "running"}

        @app.get("/health")
        async def health():
            return {"status": "ok"}

        @app.post("/v1/execute", response_model=ExecuteResponse)
        async def execute(req: ExecuteRequest):
            if not self.assistant:
                raise HTTPException(503, "Assistant not initialized")
            result = self.assistant.process(req.command)
            return ExecuteResponse(status="success", result=result)

        @app.get("/v1/system")
        async def system_info():
            if not self.assistant:
                raise HTTPException(503, "Assistant not initialized")
            result = self.assistant.process("sistem bilgisi ver")
            return {"status": "success", "data": result}

        @app.get("/v1/history")
        async def get_history():
            if self.config:
                from ..core.config import HISTORY_FILE
                if HISTORY_FILE.exists():
                    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                        return json.load(f)
            return []

        self.app = app
        log.info(f"API starting on http://{host}:{port}")
        import threading
        self.server = threading.Thread(
            target=uvicorn.run,
            args=(app,),
            kwargs={"host": host, "port": port, "log_level": "info"},
            daemon=True,
        )
        self.server.start()

    def stop(self):
        if self.server:
            log.info("API stopping...")
