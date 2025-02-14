from typing import Optional
from fastapi import FastAPI,Response , status, HTTPException
from fastapi import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

# pydantic data validation model
class Post(BaseModel):
    title:str   
    content:str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "title of post 2", "content": " like pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_posts(id):
    for i ,p in enumerate(my_posts):
        if p['id'] ==id:
            return i 
    

# request Get method url: "/"
@app.get("/") 
async def root():
    return {"message": "Welcome to the API !"}

@app.get("/posts")
def get_posts():
    return{"data": my_posts}

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 100000000)
    my_posts.append(post_dict)
    return {"data": post_dict }

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}


#path parameter
@app.get("/posts/{id}")
def get_post(id: int):

    post = find_post(id)
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} was not found")
    return{" post_detail":  post}
#        response.status_code = status.HTTP_404_NOT_FOUND
#        return{'Message': 'Post not found'}
#   print(post)
#    return{" post_detail":  post}

@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    # deleting post 
    # find index in array tha has required id
    #my_post.pop(index)
    index = find_index_posts(id)
    if index == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} does not exist")
    my_posts.pop(index)
    return Response(status_code= status.HTTP_204_NO_CONTENT)