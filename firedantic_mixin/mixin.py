from typing import Union
from firedantic import Model
from google.cloud.firestore_v1.base_query import BaseQuery
from google.cloud.firestore_v1 import CollectionReference


class FiredanticMonkey(Model) : 
    
    def __getattr__(self, name, *args, **kwargs):
        """ A method handler for unknown attributes
        This is not called directly but attached to a class providing access to CollectionReference methods
        Foo.__getattr__ = FiredanticMonkey.__getattr__
        foo_instance = Foo()
        foo_instance.list_documents()
        
        """
        #print(f"called {name} with {args} or {kwargs}")
            
        def wrapper(*args, **kwargs):
            return self._get_col_ref().__getattribute__(name)(args, kwargs)
                
        return wrapper
    
    @classmethod
    def select(cls, *args, **kwargs) -> BaseQuery : 
        """Select implements :func:`google.cloud.firestore_v1.base_query.BaseQuery.select` 
        Returns BaseQuery
        """
        return cls._get_col_ref().select(*args, **kwargs)
    
    @classmethod
    def order_by(cls, *args, **kwargs) -> BaseQuery:
        """Select implements :func:`google.cloud.firestore_v1.base_query.BaseQuery.order_by` 
        Returns BaseQuery
        """
        return cls._get_col_ref().order_by(*args, **kwargs)
    
    
    @classmethod
    def limit(cls, *arg, **kwargs) -> BaseQuery: 
        """Select implements :func:`google.cloud.firestore_v1.base_query.BaseQuery.limit` 
        
        Returns BaseQuery
        """
        return cls._get_col_ref().limit(arg)
    
    @classmethod
    def offset(cls, *arg, **kwargs) -> BaseQuery: 
        """Select implements :func:`google.cloud.firestore_v1.base_query.BaseQuery.offset` 
        Returns BaseQuery
        """
        return cls._get_col_ref().offset(arg)
    
    @classmethod
    def query(cls, *args, **kwargs ) -> BaseQuery : 
        """Select implements :func:`google.cloud.firestore_v1.base_query.BaseQuery.query` 
        Returns BaseQuery
        """
        
        query: Union[BaseQuery, CollectionReference] = cls._get_col_ref()
        filters= kwargs | {}
        
        for key, value in filters.items():
            query = cls._add_filter(query, key, value)
            
        return query
    
    @classmethod
    def to_dantic(cls, results): 
        return [cls(** x.to_dict()) for x in results]