import mysql.connector
import hashlib

class Album:
  
  def __init__(self):
    ''' Create an empty object '''
    ''' Test with test_createEmptyAccout '''
    self.album_id = ''
    self.album_name = ''
    self.release_date = ''
    self.genre = ''
    self.url_to_buy = ''
    self.band_id = ''
    
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
      print ("Something went wrong: {}".format(err))
      cnx = False
    
    return cnx
    
  def new(self, album_name, release_date, genre, url_to_buy, band_id):
    ''' Populate the current object '''
    ''' Test with test_new '''
    success = False
  
    self.album_name = album_name
    self.band_id = band_id
    self.release_date = release_date
    self.genre = genre
    self.url_to_buy = url_to_buy
    success = True
      
    return success
    
    
  def getBy(self, column, value):
    ''' Populate the object from the database, using album_id '''
    ''' Test by test_getBy* scripts '''
    success = False
    if column == 'album_id':
      cnx = self.connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor(buffered=True)
        query = ("SELECT * from album where {} = %s".format(column))
        cursor.execute(query, (value,))
        if cursor.rowcount == 1:
          row = cursor.fetchone()
          self.album_id = row[0]
          self.release_date = row[1]
          self.album_name = row[2]
          self.genre = row[3]
          self.url_to_buy = row[4]
          self.band_id = row[5]
          success = True
        cursor.close()
        cnx.close()
    return success
  
  def toJSON(self):
    ''' Returns a JSON string of the object. '''
    ''' Test with test_toJSON '''
    jsonStr = "{{ album_id: {}, album_name: '{}', release_date: '{}', genre: '{}', url_to_buy: '{}', band_id: {} }}".format(self.album_id, 
      self.album_name, self.release_date, self.genre, self.url_to_buy, self.band_id)
    return jsonStr
  
  def addToDatabase(self):
    ''' Adds the current object to the database '''
    ''' Only works on new objects '''
    ''' Test with test_SaveAndDeleteToDatabase() '''
    success = False
    noErrors = True
    if self.getAlbumID() == '' and self.isAlbumNameAvailable(self.album_name, self.band_id):
      cnx = self.connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("INSERT INTO album (album_name, release_date, genre, url_to_buy, band_id) "
                 "VALUES (%s, %s, %s, %s, %s)")
                 
        try:
          cursor.execute( query, (self.album_name, self.release_date, self.genre, self.url_to_buy, self.band_id) )
        except mysql.connector.Error as err:
          noErrors = False
        
        if noErrors == True:
          query = ("SELECT album_id FROM album WHERE album_name = %s AND band_id = %s")
          cursor.execute( query, (self.album_name, self.band_id))
          self.setAlbumID(cursor.fetchone()[0])
          if self.getAlbumID() != '':
            cnx.commit()
            success = True
            
        cursor.close()
        cnx.close()
        
    return success

  # Accessors  
  def getAlbumID(self):
    return self.album_id
    
  def getAlbumName(self):
    return self.album_name
    
  def getReleaseDate(self):
    return self.release_date
    
  def getGenre(self):
    return self.genre
  
  def getURLtoBuy(self):
    return self.url_to_buy
    
  def getBandID(self):
    return self.band_id

  # Mutators
  # Test with test_Mutators()
  def setAlbumID(self, album_id):
    success = False
    if (1):
      self.album_id = album_id
      success = True
    return success
  
  def setAlbumName(self, albumname):
    success = False
    if (1):
      self.album_name = albumname
      success = True
    return success
      
  def setReleaseDate(self, date):
    success = False
    if (1):
      self.release_date = date
      success = True
    return success
  
  def setGenre(self, genre):
    success = False
    if (1):
      self.genre = genre
      success = True
    return success
    
  def setURLtoBuy(self, url):
    success = False
    if (1):
      self.url_to_buy = url
      success = True
    return success
    
  def setBandID(self, band_id):
    success = False
    if (1):
      self.band_id = band_id
      success = True
    return success
    
  ####

  def isAlbumNameAvailable(self, albumname, band_id):
    ''' Checks to see if the given albumname is already in use '''
    ''' Test with test_isAlbumNameAvailable '''
    available = False
    cnx = self.connectToDatabase()
    if cnx != False:
      cursor = cnx.cursor(buffered=True)
      query = ("SELECT * FROM album WHERE album_name = %s AND band_id = %s")
      cursor.execute(query, (albumname,band_id))
      if cursor.rowcount < 1:
        available = True
      cursor.close()
      cnx.close()
    return available
    
    
  def deleteFromDatabase(self):
    ''' Deletes the object from the database '''
    ''' Test with test_SaveAndDeleteFromDatabase '''
    success = False
    if self.getAlbumID() != '':
      cnx = self.connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("DELETE FROM album WHERE album_id = %s")
        cursor.execute(query, (self.getAlbumID(),))
        cnx.commit()
        cursor.close()
        cnx.close()
        success = True
    return success
  