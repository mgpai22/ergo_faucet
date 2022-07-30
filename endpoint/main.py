from fastapi import FastAPI, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

import SQL_functions
import ergo
import uuid

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/faucet_api")
async def faucet_api(bg_tasks: BackgroundTasks, address: str = Form()):
    if ergo.address_validity(address):
        uu_id = str(uuid.uuid4())
        bg_tasks.add_task(ergo.getERG, address, uu_id)
        return {"task_id": uu_id}
    return "Error"


@app.get("/api_hash/{task_id}")
async def api_hash(task_id):
    try:
        return {"tx_hash": SQL_functions.query_faucet_table(task_id)[1]}
    except Exception as e:
        return {"tx_hash": "None"}
