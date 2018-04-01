import mysql.connector
import hashlib

class MapSongToAlbum:
  
  def __init__(self):
    ''' Create an empty object '''
    ''' Test with test_createEmptyAccout '''
    self.map_song_to_album_id = ''
    self.song_id = ''
    self.album_id = ''
    self.track_number = ''
    
  def connectToDatabase(self):
    ''' Connect to the Database '''
    ''' Test with test_getBy '''
    try:
      cnx = mysql.connector.connect(
        user='webapp', 
        password='centralSolutions123',
        host='18.222.66.236', 
        database='musicproject'
      )
    except mysql.connector.Error as err:
      cnx = False
    
    return cnx
    
  def new(self, song_id, album_id, track_number):
    ''' Populate the current object '''
    ''' Test with test_new '''
    success = False
  
    self.song_id = song_id
    self.album_id = album_id
    self.track_number = track_number
    success = True
      
    return success
    
    
  def getBy(self, column, value):
    ''' Populate the object from the database, using map_song_to_album_id '''
    ''' Test by test_getBy* scripts '''
    success = False
    if column == 'map_song_to_album_id':
      cnx = self.connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor(buffered=True)
        query = ("SELECT map_song_to_album_id,song_id,album_id,track_number from map_song_to_album where {} = %s".format(column))
        cursor.execute(query, (value,))
        if cursor.rowcount == 1:
          row = cursor.fetchone()
          self.map_song_to_album_id = row[0]
          self.song_id = row[1]
          self.album_id = row[2]
          self.track_number = row[3]
          success = True
        cursor.close()
        cnx.close()
    return success
  
  def toJSON(self):
    ''' Returns a JSON string of the object. '''
    ''' Test with test_toJSON '''
    jsonStr = "{{ map_song_to_album_id: {}, song_id: {}, album_id: {}, track_number: {} }}".format(self.map_song_to_album_id, 
      self.song_id, self.album_id, self.track_number)
    return jsonStr
  
  def addToDatabase(self):
    ''' Adds the current object to the database '''
    ''' Only works on new objects '''
    ''' Test with test_SaveAndDeleteToDatabase() '''
    success = False
    noErrors = True
    if self.getMapSongToAlbumID() == '' and self.notDuplicateMapSongToAlbum(self.song_id, self.album_id) == True:
      cnx = self.connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("INSERT INTO map_song_to_album (song_id, album_id, track_number) "
                 "VALUES (%s, %s, %s)")
                 
        try:
          cursor.execute( query, (self.song_id, self.album_id, self.track_number) )
        except mysql.connector.Error as err:
          noErrors = False
        
        if noErrors == True:
          query = ("SELECT map_song_to_album_id FROM map_song_to_album WHERE song_id = %s AND album_id = %s")
          cursor.execute( query, (self.song_id, self.album_id))
          self.setMapSongToAlbumID(cursor.fetchone()[0])
          if self.getMapSongToAlbumID() != '':
            cnx.commit()
            success = True

        cursor.close()
        cnx.close()

    return success

  # Accessors  
  def getMapSongToAlbumID(self):
    return self.map_song_to_album_id
    
  def getSongID(self):
    return self.song_id
    
  def getAlbumID(self):
    return self.album_id
    
  def getTrackNumber(self):
    return self.track_number

  # Mutators
  # Test with test_Mutators()
  def setMapSongToAlbumID(self, map_song_to_album_id):
    success = False
    if (1):
      self.map_song_to_album_id = map_song_to_album_id
      success = True
    return success
  
  def setSongID(self, song_id):
    success = False
    if (1):
      self.song_id = song_id
      success = True
    return success
    
  def setAlbumID(self, album_id):
    success = False
    if (1):
      self.album_id = album_id
      success = True
    return success
    
  def setTrackNumber(self, track_number):
    success = False
    if (1):
      self.track_number = track_number
      success = True
    return True
    
  ####

  def notDuplicateMapSongToAlbum(self, song_id, album_id):
    ''' Checks to see if the user has commented already '''
    ''' Test with test_notDuplicateComment '''
    notDuplicate = False
    cnx = self.connectToDatabase()
    if cnx != False:
      cursor = cnx.cursor(buffered=True)
      query = ("SELECT * FROM map_song_to_album WHERE song_id = %s AND album_id = %s")
      cursor.execute(query, (song_id,album_id))
      if cursor.rowcount < 1:
        notDuplicate = True
      cursor.close()
      cnx.close()

    return notDuplicate
    
    
  def deleteFromDatabase(self):
    ''' Deletes the object from the database '''
    ''' Test with test_SaveAndDeleteFromDatabase '''
    success = False
    if self.getMapSongToAlbumID() != '':
      cnx = self.connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("DELETE FROM map_song_to_album WHERE map_song_to_album_id = %s")
        cursor.execute(query, (self.getMapSongToAlbumID(),))
        cnx.commit()
        cursor.close()
        cnx.close()
        success = True
    return success
  