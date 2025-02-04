from fastapi import FastAPI
from fastapi import Body


app = FastAPI()

# request Get method url: "/"
@app.get("/") 
async def root():
    return {"message": "Welcome to the API !"}

@app.get("/posts")
def get_posts():
    return{"data": "These are your posts"}

@app.post("/createposts")
def create_posts(payload: dict = Body(...)):
    print(payload)
    return{"new_post": f"title {payload}" } 