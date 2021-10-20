from typing import Dict
from models.supplier import Supplier
import logging

logger = logging.getLogger(__name__)


class Database:
    '''
    Database defines access to application storage.
    Currently, this is simply in memory storage
    '''

    def __init__(self):
        '''
        Creates an instance of the Database class
        '''
        logging.info("initializing database")
        self._suppliers = {}

    def create_supplier(self, supplier: Supplier) -> Supplier:
        '''
        Inserts a new supplier into the database.
        The newly inserted supplier will be returned with the id
        appropriately set
        ----------
        supplier: Supplier
            A supplier object representing the record to insert
        '''
        logging.info("inserting supplier into database")
        new_id = len(self._suppliers) + 1
        supplier.id = new_id
        self._suppliers[new_id] = supplier
        return supplier

    def find(self, supplier_id: int) -> Supplier:
        '''
        Finds a supplier with the id.
        If found, returns the supplier. If not found, returns None.
        '''
        if supplier_id in self._suppliers:
            return self._suppliers[supplier_id]
        else:
            return None

    def delete_supplier(self, id) -> None:
        '''
        To avoid possible conflict, delete function is impelmented
        by setting its id pointing to None.
        '''
        logging.info("deleting a supplier from database")
        self._suppliers[id] = None

    def get_suppliers(self) -> Dict[int, Supplier]:
        return self._suppliers
