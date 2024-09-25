from fastapi import FastAPI,HTTPException,Depends
from models import Band,BandCreate,Album,GenreURLChoices
from contextlib import asynccontextmanager
from db import init_db,get_session
from sqlmodel import create_engine,SQLModel,Session

@asynccontextmanager
async def lifespan(app:FastAPI):
    init_db()
    yield

app=FastAPI(lifespan=lifespan)


BANDS=[
    {'id':1,'name':'The Knicks','genre':'Rock'},
    {'id':2,'name':'Aphex Twin','genre':'Electronic'},
    {'id':3,'name':'Black Sabbath','genre':'Metal'},
    {'id':4,'name':'Wu-Tang Clan','genre':'Hip-Hop'},
]

@app.get('/bands')
async def bands()->list[Band]:
    return [
        Band(**b) for b in BANDS
    ]

@app.get('/bands/{band_id}')
async def band(band_id:int)-> Band:
    band=next ((b for b in BANDS if b['id']==band_id),None)
    if band is None:
        raise HTTPException(status_code=404,detail=f"No band with ID {band_id} found")
    return band

@app.post("/bands")
async def create_band(
    band_data: BandCreate,
    session:Session=Depends(get_session)
    )->Band:
    band=Band(name=band_data.name,genre=band_data.genre)
    session.add(band)

    if band_data.albums:
        for album in band_data.albums:
            album_obj=Album(
                title=album.title,release_date=album.release_date,band=band
                )
            session.add(album_obj)


    session.commit()
    session.refresh(band)
    return band

@app.get('/')
async def index():
    return {"hello":"World"}

@app.get('/about')
async def about():
    return 'An execptional company'

@app.get('/company')
async def company():
    return {"Rabsols":"This is my company"}

@app.get('/another')
async def another():
    return 'Just other Things12'