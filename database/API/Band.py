from DatabaseObject import DatabaseObject

class Band(DatabaseObject):
  
  def __init__(self, data=None):
    '''
    Creates an Object. If a dict is passed, pass it to the super(), then add the 
    table_name and the table_layout to it.
    Test with test_createObject()
    '''
    DatabaseObject.__init__(self, data)
    self.data['table_name'] = 'band'
    self.data['table_layout'] = {
      '0': 'band_id',
      '1': 'is_solo_artist',
      '2': 'band_name',
    }
    self.data['unique_combos'] = [
      'band_name',
    ]
    