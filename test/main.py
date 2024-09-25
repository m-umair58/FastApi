from fastapi import FastAPI,HTTPException
from schemas import Band,GenreURLChoices
app=FastAPI()


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
        raise Exception("No band with this ID found")
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
    return 'Just other Things'