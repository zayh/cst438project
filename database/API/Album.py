from DatabaseObject import DatabaseObject

class Album(DatabaseObject):
  
  def __init__(self, data=None):
    '''
    Creates an Object. If a dict is passed, pass it to the super(), then add the 
    table_name and the table_layout to it.
    Test with test_createObject()
    '''
    DatabaseObject.__init__(self, data)
    self.data['table_name'] = 'album'
    self.data['table_layout'] = {
      '0': 'album_id',
      '1': 'release_date',
      '2': 'album_name',
      '3': 'genre',
      '4': 'url_to_buy',
      '5': 'band_id'
    }
    self.data['unique_combos'] = [
      'album_name',
      'band_id'
    ]
    