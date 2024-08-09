from fastapi import FastAPI
from routes.user import router as user_router
from routes.event import router as event_router
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from prismadb import connect_prisma
from uvicorn import Config, Server

loop = asyncio.new_event_loop()
loop.run_until_complete(connect_prisma())
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(event_router)
app.include_router(user_router)

config = Config(app=app, port=8080, loop=loop)
server = Server(config=config)
loop.run_until_complete(server.serve())
