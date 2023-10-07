## Firedantic Order by / Select  / Limit


### Objective 
This is a quick 'monkeypatch' / mixin for Firedantic to provide missing capabilities
Based on the issue https://github.com/ioxiocom/firedantic/issues/43

Firedantic is a pydantic wrapper for Google Firestore, it's actually quite handy, however it is missing some design / direction and strategy. 

Currently is no select, order_by capabilities, which limits (a function also missing) you to filter and listing, reducing the ability to use it for most needs. 

Attempts to influence and encourage direction are met with hostility from the maintainer(s).
This had driven the direction of this solution to use a monkey patch and extension to allow for easy integration. 

### Installation 

Standard install, note - vs _

```
poetry add firedantic-mixin
```

Usage
```python
from firedantic_mixin.mixin import FiredanticMonkey
```

### How to use

Simply swap the super class of firedantic.Model for FiredanticMonkey

<table>
<tr><th>Firedantic standard</th><th> Firedantic mixin</th></tr>
<tr><td>

 ```python
 from firedantic import Model

 class Orders(Model):  
    __collection__ = "Monkey-Orders"
    
    item : str
    quantity : int
    price: float

```

</td><td>

```python
from firedantic_mixin.mixin import FiredanticMonkey

class Orders(FiredanticMonkey): 
    
    __collection__ = "Monkey-Orders"
    
    item : str
    quantity : int
    price: float

```
</td></tr>
</table>

This opens up the ability to do standard compound tasks by returning [Firestores BaseQuery](https://cloud.google.com/python/docs/reference/firestore/latest/google.cloud.firestore_v1.base_query.BaseQuery)

```python

# return just item and price fields, order by price
query = Orders.select(['item', 'price']).\
            order_by("price", Query.ASCENDING)

results = list(query.stream())

```

Results will be [Firestores DocumentSnapshots](https://cloud.google.com/python/docs/reference/firestore/latest/google.cloud.firestore_v1.base_document.DocumentSnapshot) to go back to a Firedantic model simply do: 

```python

models = Orders.to_dantic(results)

```

### What else can you now do? 

As you have direct access to BasicQuery as part of the model


```python

Orders.query() # returns a BaseQuery
Orders.query({"price": {">": 1}}) # filtering

Orders.query().offset(20).limit(10) # pagination

Orders.select(['item', 'price']) # field selects

Orders.query().order_by("price", Query.ASCENDING) # ordering by 

```

There is currently less than 70 lines of code that just opens this up and makes it usable.
