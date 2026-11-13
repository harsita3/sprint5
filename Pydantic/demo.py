# { "name": "Asha", "age": "23" }
# def double(age: int):
#     return age * 2# print(double("23"))     # 👉 "2323"


# Pydantic is a python library, Pydantic automates data validation,
#  type conversion, and error handling, whereas without Pydantic,
#  you have to write all of that logic manually.If you don't use Pydantic, 
# you receive data as a standard Python dictionary. You have to manually check if the keys exist, 
# check if the types are correct, and convert strings to integers.




from pydantic import BaseModel
# 1. Model for creating a new warehouse
class WarehouseCreate(BaseModel):
    name: str
    type: str          # e.g., "Cold Storage", "General"
    location: str

# 2. Model for requesting to add items to a warehouse
class StockRequest(BaseModel):
    warehouse_id: str
    item_name: str

# 3. Model for requesting to move items between warehouses
class TransferRequest(BaseModel):
    from_warehouse_id: str
    to_warehouse_id: str