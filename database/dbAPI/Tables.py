from dbAPI.DatabaseObject import DatabaseObject
import hashlib

class Account(DatabaseObject):
  
  def __init__(self, data=None):
    '''
    Creates an Object. If a dict is passed, pass it to the super(), then add the 
    table_name and the table_layout to it.
    Test with test_createObject()
    '''
    DatabaseObject.__init__(self, data)
    self.data['table_name'] = 'account'
    self.data['table_layout'] = {
      '0': 'account_id',
      '1': 'username',
      '2': 'firstname',
      '3': 'lastname',
      '4': 'lyric',
      '5': 'password'
    }
    self.data['unique_combos'] = [
      'username',
    ]
  
  def addPassword(self, passwordInText):
    success = False
    if self.setItem('password', self.hashPassword(passwordInText)):
      success = True
    return success
    
  def hashPassword(self, passwordInText):
    return hashlib.sha256( passwordInText.encode('utf-8') ).hexdigest()
  
  def checkPassword(self, passwordInText):
    success = False
    if self.getItem('password') == self.hashPassword(passwordInText):
      success = True
    return success     
        
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
    
class Favorite(DatabaseObject):
  
  def __init__(self, data=None):
    '''
    Creates an Object. If a dict is passed, pass it to the super(), then add the 
    table_name and the table_layout to it.
    Test with test_createObject()
    '''
    DatabaseObject.__init__(self, data)
    self.data['table_name'] = 'favorite'
    self.data['table_layout'] = {
      '0': 'favorite_id',
      '1': 'account_id',
      '2': 'album_id',
    }
    self.data['unique_combos'] = [
      'account_id',
      'album_id'
    ]  
    
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
  