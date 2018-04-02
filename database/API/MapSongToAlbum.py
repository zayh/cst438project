from settings import *
import json

class MapSongToAlbum:
  
  def __init__(self, data=None):
    ''' Create an empty object '''
    ''' Test with test_createEmptyAccout '''
    self.data = {}
    if data is not None:
      for key in data:
        self.data[key] = data[key]
    
  def getBy(self, column, value):
    ''' Populate the object from the database, using map_song_to_album_id '''
    ''' Test by test_getBy* scripts '''
    success = False
    noSqlErrors = True
    if column == 'map_song_to_album_id':
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor(buffered=True)
        query = ("SELECT map_song_to_album_id,song_id,album_id,track_number from map_song_to_album where {} = %s".format(column))
        try:
          cursor.execute(query, (value,))
        except mysql.connector.Error as err:
          noSqlErrors = False
        if noSqlErrors == True and cursor.rowcount == 1:
          row = cursor.fetchone()
          self.setMapSongToAlbumID(row[0])
          self.setSongID(row[1])
          self.setAlbumID(row[2])
          self.setTrackNumber(row[3])
          success = True
        cursor.close()
        cnx.close()
    return success
  
  def toJSON(self):
    ''' Returns a JSON string of the object. '''
    ''' Test with test_toJSON '''
    jsonStr = json.dumps(self.data)
    return jsonStr
  
  def fromJSON(self, jsonStr):
    data = json.loads(jsonStr)
    self.__init__(data)
  
  def addToDatabase(self):
    ''' Adds the current object to the database '''
    ''' Only works on new objects '''
    ''' Test with test_SaveAndDeleteToDatabase() '''
    success = False
    noSqlErrors = True
    if self.getMapSongToAlbumID() == '' and self.notDuplicateMapSongToAlbum() == True:
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("INSERT INTO map_song_to_album (song_id, album_id, track_number) "
                 "VALUES (%s, %s, %s)")     
        try:
          cursor.execute( query, (self.getSongID(), self.getAlbumID(), self.getTrackNumber()) )
        except mysql.connector.Error as err:
          noSqlErrors = False
        if noSqlErrors == True:
          query = ("SELECT map_song_to_album_id FROM map_song_to_album "
            "WHERE song_id = %s AND album_id = %s")
          try: 
            cursor.execute( query, (self.getSongID(), self.getAlbumID()))
          except mysql.connector.Error as err:
            noSqlErrors = False
          if noSqlErrors == True:
            self.setMapSongToAlbumID(cursor.fetchone()[0])
            if self.getMapSongToAlbumID() != '':
              cnx.commit()
              success = True
        cursor.close()
        cnx.close()
    return success

  # Accessors  
  def getMapSongToAlbumID(self):
    returnVal = ''
    if 'map_song_to_album_id' in self.data:
      returnVal = self.data['map_song_to_album_id']
    return returnVal
    
  def getSongID(self):
    returnVal = ''
    if 'song_id' in self.data:
      returnVal = self.data['song_id']
    return returnVal
    
  def getAlbumID(self):
    returnVal = ''
    if 'album_id' in self.data:
      returnVal = self.data['album_id']    
    return returnVal
    
  def getTrackNumber(self):
    returnVal = ''
    if 'track_number' in self.data:
      returnVal = self.data['track_number']
    return returnVal

  # Mutators
  # Test with test_Mutators()
  def setMapSongToAlbumID(self, map_song_to_album_id):
    success = False
    if (1):
      self.data['map_song_to_album_id'] = map_song_to_album_id
      success = True
    return success
  
  def setSongID(self, song_id):
    success = False
    if (1):
      self.data['song_id'] = song_id
      success = True
    return success
    
  def setAlbumID(self, album_id):
    success = False
    if (1):
      self.data['album_id'] = album_id
      success = True
    return success
    
  def setTrackNumber(self, track_number):
    success = False
    if (1):
      self.data['track_number'] = track_number
      success = True
    return True
    
  ####

  def notDuplicateMapSongToAlbum(self):
    ''' Checks to see if the user has commented already '''
    ''' Test with test_notDuplicateComment '''
    notDuplicate = False
    noSqlErrors = True
    cnx = connectToDatabase()
    if cnx != False and self.getSongID() != '' and self.getAlbumID != '':
      cursor = cnx.cursor(buffered=True)
      query = ("SELECT * FROM map_song_to_album WHERE song_id = %s AND album_id = %s")
      try:
        cursor.execute(query, (self.getSongID(), self.getAlbumID()))
      except mysql.connector.Error as err:
        noSqlErrors = False
      if noSqlErrors == True and cursor.rowcount == 0:
        notDuplicate = True
      cursor.close()
      cnx.close()
    return notDuplicate
    
    
  def deleteFromDatabase(self):
    ''' Deletes the object from the database '''
    ''' Test with test_SaveAndDeleteFromDatabase '''
    success = False
    noSqlErrors = True
    if self.getMapSongToAlbumID() != '':
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("DELETE FROM map_song_to_album WHERE map_song_to_album_id = %s")
        try:
          cursor.execute(query, (self.getMapSongToAlbumID(),))
        except mysql.connector.Error as err:
          noSqlErrors = False
        if noSqlErrors == True:
          cnx.commit()
          success = True
        cursor.close()
        cnx.close()
    return success
  
  def saveToDatabase(self):
    ''' Saves current object to the database, using the primary index '''
    success = False
    noSqlErrors = True
    if self.getMapSongToAlbumID() != '':
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("UPDATE map_song_to_album SET song_id = %s, album_id = %s , track_number = %s "
          "WHERE map_song_to_album_id = %s")
        try:
          cursor.execute(query, 
            (self.getSongID(), self.getAlbumID(), self.getTrackNumber(), self.getMapSongToAlbumID()) 
          )
        except mysql.connector.Error as err:
          noSqlErrors = False
        if noSqlErrors == True:
          cnx.commit()
          self.getBy('map_song_to_album_id', self.getMapSongToAlbumID())
          success = True
        cursor.close()
        cnx.close()
    return success
    