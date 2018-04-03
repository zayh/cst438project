from DatabaseObject import DatabaseObject
from settings import *

class Wishlist(DatabaseObject):
  
  def __init__(self, data=None):
    '''
    Creates an Object. If a dict is passed, pass it to the super(), then add the 
    table_name and the table_layout to it.
    Test with test_createObject()
    '''
    DatabaseObject.__init__(self, data)
    self.data['table_name'] = 'wishlist'
    self.data['table_layout'] = {
      '0': 'wishlist_id',
      '1': 'account_id',
      '2': 'album_id'
    }
    self.data['unique_combos'] = [
      'account_id',
      'album_id'
    ]
    