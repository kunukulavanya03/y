from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# Database setup
engine = create_engine('postgresql://user:password@localhost/dbname')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Models
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)

class Hotel(Base):
    __tablename__ = 'hotels'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    address = Column(String)
    description = Column(String)

class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    hotel_id = Column(Integer, ForeignKey('hotels.id'))
    checkin = Column(Date)
    checkout = Column(Date)

# API Endpoints
@app.get('/api/users')
def get_users():
    users = session.query(User).all()
    return JSONResponse(content=[user.__dict__ for user in users], media_type='application/json')

@app.get('/api/users/{id}')
def get_user(id: int):
    user = session.query(User).filter(User.id == id).first()
    return JSONResponse(content=user.__dict__, media_type='application/json')

@app.post('/api/users')
def create_user(username: str, email: str, password: str):
    new_user = User(username=username, email=email, password=password)
    session.add(new_user)
    session.commit()
    return JSONResponse(content=new_user.__dict__, media_type='application/json')

@app.put('/api/users/{id}')
def update_user(id: int, username: str, email: str, password: str):
    user = session.query(User).filter(User.id == id).first()
    user.username = username
    user.email = email
    user.password = password
    session.commit()
    return JSONResponse(content=user.__dict__, media_type='application/json')

@app.delete('/api/users/{id}')
def delete_user(id: int):
    user = session.query(User).filter(User.id == id).first()
    session.delete(user)
    session.commit()
    return JSONResponse(content={}, media_type='application/json')

# Hotels
@app.get('/api/hotels')
def get_hotels():
    hotels = session.query(Hotel).all()
    return JSONResponse(content=[hotel.__dict__ for hotel in hotels], media_type='application/json')

@app.get('/api/hotels/{id}')
def get_hotel(id: int):
    hotel = session.query(Hotel).filter(Hotel.id == id).first()
    return JSONResponse(content=hotel.__dict__, media_type='application/json')

@app.post('/api/hotels')
def create_hotel(name: str, address: str, description: str):
    new_hotel = Hotel(name=name, address=address, description=description)
    session.add(new_hotel)
    session.commit()
    return JSONResponse(content=new_hotel.__dict__, media_type='application/json')

@app.put('/api/hotels/{id}')
def update_hotel(id: int, name: str, address: str, description: str):
    hotel = session.query(Hotel).filter(Hotel.id == id).first()
    hotel.name = name
    hotel.address = address
    hotel.description = description
    session.commit()
    return JSONResponse(content=hotel.__dict__, media_type='application/json')

@app.delete('/api/hotels/{id}')
def delete_hotel(id: int):
    hotel = session.query(Hotel).filter(Hotel.id == id).first()
    session.delete(hotel)
    session.commit()
    return JSONResponse(content={}, media_type='application/json')

# Bookings
@app.get('/api/bookings')
def get_bookings():
    bookings = session.query(Booking).all()
    return JSONResponse(content=[booking.__dict__ for booking in bookings], media_type='application/json')

@app.get('/api/bookings/{id}')
def get_booking(id: int):
    booking = session.query(Booking).filter(Booking.id == id).first()
    return JSONResponse(content=booking.__dict__, media_type='application/json')

@app.post('/api/bookings')
def create_booking(user_id: int, hotel_id: int, checkin: Date, checkout: Date):
    new_booking = Booking(user_id=user_id, hotel_id=hotel_id, checkin=checkin, checkout=checkout)
    session.add(new_booking)
    session.commit()
    return JSONResponse(content=new_booking.__dict__, media_type='application/json')

@app.put('/api/bookings/{id}')
def update_booking(id: int, user_id: int, hotel_id: int, checkin: Date, checkout: Date):
    booking = session.query(Booking).filter(Booking.id == id).first()
    booking.user_id = user_id
    booking.hotel_id = hotel_id
    booking.checkin = checkin
    booking.checkout = checkout
    session.commit()
    return JSONResponse(content=booking.__dict__, media_type='application/json')

@app.delete('/api/bookings/{id}')
def delete_booking(id: int):
    booking = session.query(Booking).filter(Booking.id == id).first()
    session.delete(booking)
    session.commit()
    return JSONResponse(content={}, media_type='application/json')

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)