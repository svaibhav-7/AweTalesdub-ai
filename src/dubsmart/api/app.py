from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router


def create_app() -> FastAPI:
    app = FastAPI(title="Dubsmart AI API")

    # Enable CORS for the React frontend (both local and Render deployment)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify your Render frontend URL
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)
    return app


app = create_app()
