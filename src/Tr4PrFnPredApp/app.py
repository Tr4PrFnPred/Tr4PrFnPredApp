# python modules
import logging
import sys

# used for starting the application
import uvicorn

# library for asynchronous operations
import asyncio

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from .routers import predict, result

app = FastAPI(
    title="Transformers for Protein Function Prediction",
    description="API for Transformers for Protein Function Prediction",
    version="0.0.1"
)

# enable CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# include routers
app.include_router(predict.router)
app.include_router(result.router)

# mount static and template files
app.mount("/tr4prfn/static", StaticFiles(directory="src/Tr4PrFnPredApp/static/"), name="static")
templates = Jinja2Templates(directory="src/Tr4PrFnPredApp/templates/")

# loggers
logging.basicConfig(level=logging.DEBUG)

# set the event loop depending on platform
# https://stackoverflow.com/questions/44633458/why-am-i-getting-notimplementederror-with-async-and-await-on-windows
if 'win32' in sys.platform:
    # asyncio.set_event_loop(asyncio.ProactorEventLoop())
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# home page
@app.get("/tr4prfn", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)