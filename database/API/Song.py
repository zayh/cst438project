from DatabaseObject import DatabaseObject

class Song(DatabaseObject):
  
  def __init__(self, data=None):
    '''
    Creates an Object. If a dict is passed, pass it to the super(), then add the 
    table_name and the table_layout to it.
    Test with test_createObject()
    '''
    DatabaseObject.__init__(self, data)
    self.data['table_name'] = 'song'
    self.data['table_layout'] = {
      '0': 'song_id',
      '1': 'song_name',
      '2': 'is_solo_release',
      '3': 'band_id',
    }
    self.data['unique_combos'] = [
      'song_name',
      'band_id'
    ]
    