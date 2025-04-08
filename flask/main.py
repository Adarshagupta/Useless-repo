from fastapi import Query, Path, FastAPI
from typing import Union

app = FastAPI(
    title = "Bharat is a gay",
    description = "Bharat is having sex with sakhyam",
    version = "1.0.0.0"
)

@app.get('/')
def imdex():
    return {"Hello world"}

@app.get('/search')
def search(keyword: str, max_price: float | None = None):
    return {"keyword": keyword, 'max_price': max_price}