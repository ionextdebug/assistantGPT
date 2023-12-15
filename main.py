from fastapi import FastAPI
from openai import OpenAI
from dotenv import load_dotenv
import os
from fastapi.templating import Jinja2Templates
from fastapi import Request, Body
import json

load_dotenv()
app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))
templates = Jinja2Templates(directory="templates")


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(model=model,
    messages=messages,
    temperature=0)
    return response.choices[0].message.content

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = client.chat.completions.create(model=model,
    messages=messages,
    temperature=temperature)
#     print(str(response.choices[0].message))
    return response.choices[0].message.content

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("homepage.html", {"request": request})


@app.get("/escolaGPT")
async def root(request: Request):
    return templates.TemplateResponse("frontend.html", {"request": request})


@app.post("/perguntar")
async def perguntar(payload = Body(None)):
    
    question = payload["text"]
    
    messages =  [
        {'role':'system', 'content':'You are an assistant that teach to high schools students, you answer using Portuguese of Brazil, and you can only search on sites: Wikipedia.com'},    
        {'role':'user', 'content': question},
    ]

    response = get_completion_from_messages(messages, temperature=1)
    return {"response": response}