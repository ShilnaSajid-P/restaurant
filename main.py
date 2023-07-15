from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from routers import router
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def login_to_account(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
