import mysql.connector
import hashlib

class Song:
  
  def __init__(self):
    ''' Create an empty object '''
    ''' Test with test_createEmptyAccout '''
    self.song_id = ''
    self.song_name = ''
    self.band_id = ''
    self.is_solo_release = False
    
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
    
  def new(self, song_name, is_solo_release, band_id):
    ''' Populate the current object '''
    ''' Test with test_new '''
    success = False
  
    self.song_name = song_name
    self.band_id = band_id
    self.is_solo_release = is_solo_release
    success = True
      
    return success
    
    
  def getBy(self, column, value):
    ''' Populate the object from the database, using song_id '''
    ''' Test by test_getBy* scripts '''
    success = False
    if column == 'song_id':
      cnx = self.connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor(buffered=True)
        query = ("SELECT song_id, song_name, is_solo_release, band_id from song where {} = %s".format(column))
        cursor.execute(query, (value,))
        if cursor.rowcount == 1:
          row = cursor.fetchone()
          self.song_id = row[0]
          self.song_name = row[1]
          self.band_id = row[3]
          if row[2] == 0:
            self.is_solo_release = False
          else:
            self.is_solo_release = True
          success = True
        cursor.close()
        cnx.close()
    return success
  
  def toJSON(self):
    ''' Returns a JSON string of the object. '''
    ''' Test with test_toJSON '''
    jsonStr = "{{ song_id: {}, song_name: '{}', is_solo_release: {}, band_id: {} }}".format(self.song_id, 
      self.song_name, self.is_solo_release, self.band_id)
    return jsonStr
  
  def addToDatabase(self):
    ''' Adds the current object to the database '''
    ''' Only works on new objects '''
    ''' Test with test_SaveAndDeleteToDatabase() '''
    success = False
    noErrors = True
    if self.getSongID() == '' and self.isSongNameAvailable(self.song_name, self.band_id):
      cnx = self.connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        if self.isSoloRelease() == True:
          solo = 1
        else:
          solo = 0
        query = ("INSERT INTO song (song_name, is_solo_release, band_id) "
                 "VALUES (%s, %s, %s)")
                 
        try:
          cursor.execute( query, (self.song_name, solo, self.band_id) )
        except mysql.connector.Error as err:
          noErrors = False
        
        if noErrors == True:
          query = ("SELECT song_id FROM song WHERE song_name = %s AND band_id = %s")
          cursor.execute( query, (self.song_name, self.band_id))
          self.setSongID(cursor.fetchone()[0])
          if self.getSongID() != '':
            cnx.commit()
            success = True
            
        cursor.close()
        cnx.close()
        
    return success

  # Accessors  
  def getSongID(self):
    return self.song_id
    
  def getSongName(self):
    return self.song_name
    
  def isSoloRelease(self):
    return self.is_solo_release
    
  def getBandID(self):
    return self.band_id

  # Mutators
  # Test with test_Mutators()
  def setSongID(self, song_id):
    success = False
    if (1):
      self.song_id = song_id
      success = True
    return success
  
  def setSongName(self, songname):
    success = False
    if (1):
      self.song_name = songname
      success = True
    return success
      
  def setSoloRelease(self, boolean):
    success = False
    if (1):
      self.is_solo_release = boolean
      success = True
    return success
    
  def setBandID(self, band_id):
    success = False
    if (1):
      self.band_id = band_id
      success = True
    return success
    
  ####

  def isSongNameAvailable(self, songname, band_id):
    ''' Checks to see if the given songname is already in use '''
    ''' Test with test_isSongNameAvailable '''
    available = False
    cnx = self.connectToDatabase()
    if cnx != False:
      cursor = cnx.cursor(buffered=True)
      query = ("SELECT * FROM song WHERE song_name = %s AND band_id = %s")
      cursor.execute(query, (songname,band_id))
      if cursor.rowcount < 1:
        available = True
      cursor.close()
      cnx.close()
    return available
    
    
  def deleteFromDatabase(self):
    ''' Deletes the object from the database '''
    ''' Test with test_SaveAndDeleteFromDatabase '''
    success = False
    if self.getSongID() != '':
      cnx = self.connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("DELETE FROM song WHERE song_id = %s")
        cursor.execute(query, (self.getSongID(),))
        cnx.commit()
        cursor.close()
        cnx.close()
        success = True
    return success
  