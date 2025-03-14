from typing import Optional
from fastapi import FastAPI,Response , status, HTTPException
from fastapi import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

# pydantic data validation model
class Post(BaseModel):
    title:str   
    content:str
    published: bool = True
# id 
# created at 
#    rating: Optional[int] = None
while True:

    try:
        conn = psycopg2.connect( host = "localhost", database = 'fastapi', 
        user = 'postgres', password = 'jj', cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print("Connected to the database")
        break
    except Exception as error:
        print(" connecting to database failed ")
        print ("Error: ", error)
        time.sleep(5)


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
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
#    print(posts)
    return{"data": posts}

@app.post("/posts", status_code = status.HTTP_201_CREATED)
def create_posts(post: Post):
#    post_dict = post.dict()
#    post_dict['id'] = randrange(0, 100000000)
#    my_posts.append(post_dict)
    cursor.execute(""" INSERT INTO posts (title, content,published) VALUES (%s, %s, %s)""",(post.title, post.content, post.published))
    new_post = cursor.fetchone()

    return {"data": new_post }

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

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_posts(id)
    if index == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} does not exist")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return{'message' : "updated post "}

    # around 4 