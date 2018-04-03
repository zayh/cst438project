from DatabaseObject import DatabaseObject

class Rating(DatabaseObject):
  
  def __init__(self, data=None):
    '''
    Creates an Object. If a dict is passed, pass it to the super(), then add the 
    table_name and the table_layout to it.
    Test with test_createObject()
    '''
    DatabaseObject.__init__(self, data)
    self.data['table_name'] = 'rating'
    self.data['table_layout'] = {
      '0': 'rating_id',
      '1': 'account_id',
      '2': 'album_id',
      '3': 'rating',
      '4': 'comment',
      '5': 'date',
    }
    self.data['unique_combos'] = [
      'account_id',
      'album_id'
    ]
  