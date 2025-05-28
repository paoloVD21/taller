from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum

app = FastAPI()

class Supplier(Enum):
    supplier1 = "Supplier 1"
    supplier2 = "Supplier 2"
    supplier3 = "Supplier 3"

class Item(BaseModel):
    name: str
    price: float
    stock: bool
    supplier: Supplier

items = [
    {"id": 1, "nombre": "Laptop", "precio": 3500.0, "stock": False},
    {"id": 2, "nombre": "Teclado", "precio": 150.0, "stock": True},
    {"id": 3, "nombre": "Monitor", "precio": 900.0, "stock": False}
]


@app.get('/')
def index():
    return {
        'message': "Hello"
    }

@app.get('/items')
def get_items():
    return {
        'items': items
    }

@app.get('/items/{item_name}')
def get_item(item_name: str):
    print(item_name)
    for item in items:
        if item['nombre'] == item_name:
            return { 'item': item}
    return {'error': 'Item no encontrado'}

@app.post('/items')
def create_item(item_data: Item):
    print(item_data)
    items.append(item_data)
    return {'new_item': item_data}

@app.put('/items/{item_name}')
def update_item(item_name: str, item_data: Item):
    for item in items:
        if item['nombre'] == item_name:
            item['nombre'] = item_data.name
            item['precio'] = item_data.price
            item['stock'] = item_data.stock
            item['proveedor'] = item_data.supplier
            return{'updated_item': item}
    return {'error': 'Item no encontrado'}

@app.delete('/items/{item_name}')
def delete_item(item_name: str):
    for item in items:
        if item['nombre'] == item_name:
            items.remove(item)
            return {'deleted_item': item}
    return {'error': 'Item no encontrado'}
