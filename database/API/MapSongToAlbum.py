from DatabaseObject import DatabaseObject

class MapSongToAlbum(DatabaseObject):
  
  def __init__(self, data=None):
    '''
    Creates an Object. If a dict is passed, pass it to the super(), then add the 
    table_name and the table_layout to it.
    Test with test_createObject()
    '''
    DatabaseObject.__init__(self, data)
    self.data['table_name'] = 'map_song_to_album'
    self.data['table_layout'] = {
      '0': 'map_song_to_album_id',
      '1': 'track_number',
      '2': 'album_id',
      '3': 'song_id',
    }
    self.data['unique_combos'] = [
      'song_id',
      'album_id'
    ]  
    