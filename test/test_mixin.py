from firedantic_mixin.mixin import FiredanticMonkey
import pytest
from unittest.mock import Mock

import google.auth.credentials
from firedantic import configure
from google.cloud.firestore import Client, Query

from os import environ



class Orders(FiredanticMonkey): 
    
    __collection__ = "Monkey-Orders"
    
    item : str
    quantity : int
    price: float



@pytest.fixture
def firebase_client(): 
    environ.setdefault("FIRESTORE_EMULATOR_HOST", "127.0.0.1:8686")
    
    client = Client(
        project="firedantic-test",
        credentials=Mock(spec=google.auth.credentials.Credentials)
    )
    
    configure(client, prefix="firedantic-test-")
    
    return client

@pytest.fixture
def setup_orders(firebase_client) : 
    orders = [
        {"item" : "banana", "quantity": 1, "price": 0.1},
        {"item" : "hand of bananas", "quantity": 5, "price": 0.5},
        {"item" : "stalk of bananas", "quantity": 30, "price": 3.00}
    ]
    
    for o in orders : 
        monkey_order = Orders(**o)
        monkey_order.save()
    

def test_orders_select(setup_orders) : 
    
    #Orders.select = getattr
    query = Orders.select(['item', 'price'])
    
    for row in query.stream() : 
        res = row.to_dict()
        assert all( k in ["item", "price"] for k in res.keys())
        
    Orders.truncate_collection()
    
    
def test_orders_order_by(setup_orders) : 
    query = Orders.select(['item', 'price']).order_by("price", Query.ASCENDING)
    
    
    initial_price = 0
    for row in query.stream() : 
        assert row.get("price") >= initial_price
        initial_price = row.get("price")
    
    Orders.truncate_collection()
    
def test_orders_limit(setup_orders) : 
    query = Orders.query({"price": {">": 1}}).limit(1)

    results = list(query.stream())
    assert len(results) == 1
    print(results)
    
    models = [Orders(** x.to_dict()) for x in results]
    print(models)
    
    models_list = Orders.to_dantic(results)
    
    print(models_list)
    
    Orders.truncate_collection()
