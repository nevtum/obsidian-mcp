from fastapi import FastAPI
from fastapi.responses import RedirectResponse


def create_app():
    from .routes import router

    app = FastAPI()

    @app.get("/")
    async def index():
        return RedirectResponse("/docs")

    app.include_router(router, prefix="/notes")

    return app


app = create_app()
