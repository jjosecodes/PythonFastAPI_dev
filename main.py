from typing import Optional
from fastapi import FastAPI
from fastapi import Body
from pydantic import BaseModel

app = FastAPI()

# pydantic data validation model
class Post(BaseModel):
    title:str   
    content:str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "title of post 2", "content": " like pizza", "id": 2}]



# request Get method url: "/"
@app.get("/") 
async def root():
    return {"message": "Welcome to the API !"}

@app.get("/posts")
def get_posts():
    return{"data": my_posts}

@app.post("/posts")
def create_posts(post: Post):


    my_posts.append(post.dict())
    return {"data": post }
#title str , content str 



