from fastapi import Depends, FastAPI
import httpx
from pydantic import BaseModel, EmailStr, HttpUrl
from starlette.config import Config
from contextlib import asynccontextmanager
from fastapi_pagination import Page, Params, paginate

config = Config('.env')
API = config('RANDOMUSER_URI')
fields=config('USER_FIELDS')
no_of_users= config('NO_OF_USERS')

class User(BaseModel):
    id:int
    name:str
    email: EmailStr
    picture: HttpUrl

def get_data():
    response = httpx.get(f'{API}?inc={fields}&results={no_of_users}')
    return response.json()['results']

@asynccontextmanager
async def lifespan(app:FastAPI):
    raw_users=get_data()
    users=[]
    for id,raw_user in enumerate(raw_users):
        users.append(
            User(
                id=id,
                name=f'{raw_user['name']['first']}{raw_user['name']['last']}',
                email=raw_user['email'],
                picture=raw_user['picture']['medium']
            )
        )
    app.state.users=users
    yield
#life span error resolved through https://stackoverflow.com/questions/78042466/fastapi-app-on-event-decorator-is-deprecated-how-can-i-create-a-simple-repeat
#on_event is depriciated so we used lifespan function

app=FastAPI(lifespan=lifespan)



@app.get('/users',response_model=Page[User])
async def get_users(
    params:Params=Depends()
):
    return paginate(app.state.users,params)