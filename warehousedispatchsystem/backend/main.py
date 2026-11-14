from fastapi import FastAPI, HTTPException, Header, Body;
from fastapi.middleware.cors import CORSMiddleware;
from datetime import datetime, date;
from pydantic import BaseModel
import function

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PackageCreate(BaseModel):
    name: str
    destination: str
    weight: float

class PackageUpdate(BaseModel):
    name: str | None = None
    destination: str | None = None
    weight: float | None = None

class DispatchCreate(BaseModel):
    destination: str
    vehicle_number: str
    dispatch_date: str

class UserCredentials(BaseModel):
    username: str
    password: str


#E1
@app.post("/packages")
def register_package(package: PackageCreate, token = Header(None)):
    username = function.verify_token(token = token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")
    return function.register_package(name=package.name, destination=package.destination, weight=package.weight)

#E2
@app.get("/packages/{package_id}")
def get_package_details(package_id,  token = Header(None)):
    username = function.verify_token(token = token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")
    return function.get_package_by_id(package_id)

#E3
@app.patch("/packages/{package_id}")
def update_package_details(package_id, package: PackageUpdate, token = Header(None)):
    username = function.verify_token(token = token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")
    return function.update_package_details(package_id=package_id, name=package.name, destination=package.destination, weight=package.weight)

#E4
@app.delete("/packages/{package_id}")
def delete_package(package_id,  token = Header(None)):
    username = function.verify_token(token = token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")
    return function.delete_package(package_id=package_id)

#E5
@app.get("/packages")    
def search_package(destination= None, status= None, arrival_date= None,  token = Header(None)):
    username = function.verify_token(token = token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")
    return function.search_package(destination=destination, status=status, arrival_date=arrival_date)

#E6
@app.get("/dispatch-batches")
def view_dispatchBatches(destination, vehicle_number, dispatch_status,  token = Header(None)):
    username = function.verify_token(token = token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")
    return function.view_dispatchBatches(destination=destination, vehicle_number=vehicle_number, dispatch_status=dispatch_status)

#E7
@app.get("/warehouse/summary")
def warehouse_summary( token = Header(None)):
    username = function.verify_token(token = token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")
    return function.get_warehouse_summary()

#E8 
@app.post("/dispatch-batches")
def add_dispatch(batch: DispatchCreate, token = Header(None)):
    username = function.verify_token(token = token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")
    return function.create_dispatchBatches(destination=batch.destination, vehicle_number=batch.vehicle_number, dispatch_date=batch.dispatch_date)


@app.post("/login")
def login(user: UserCredentials):
    token =  function.verify_login(username = user.username, password=user.password)
    if not token :
        raise HTTPException(status_code = 401, detail="Invalid credentials")
    return token

@app.post("/refresh")
def refresh(refresh_token = Header(None)):
   username =  function.verify_token(token=refresh_token , token_type= "refresh")
   if not username:
       raise HTTPException(status_code=401, detail="Invalid or Expired refresh token")
   
   access_token = function.create_token(username=username, token_type= "access")
   return {"access_token" : access_token}


@app.post("/register")
def register_user(user: UserCredentials):
    if function.register_user(username = user.username, password = user.password):
        return{"message": "user registered succesfully"}
    raise HTTPException(status_code=404, detail="user already exist")



