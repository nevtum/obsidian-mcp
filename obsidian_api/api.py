from fastapi import FastAPI


def create_app():
    from .routes import router

    app = FastAPI()
    app.include_router(router)
    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
