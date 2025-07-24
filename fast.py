from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from together import Together
from pydantic import BaseModel
from typing import Dict, List
import os

load_dotenv()

app = FastAPI()
client = Together()

chat_histories: Dict[str, List[Dict[str, str]]] = {}

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello {name}"}

class Query(BaseModel):
    userid: str
    message: str

@app.post("/chat/")
def chat(query: Query):
    try:
        userid = query.userid
        user_msg = query.message

        if not userid or not user_msg:
            raise HTTPException(status_code=400, detail="User ID and message are required")

        if userid not in chat_histories:
            chat_histories[userid] = []

        chat_histories[userid].append({"role": "user", "content": user_msg})

        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            messages=chat_histories[userid]
        )

        bot_msg = response.choices[0].message.content
        chat_histories[userid].append({"role": "assistant", "content": bot_msg})

        return {
            "answer": bot_msg,
            "history": chat_histories[userid]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)