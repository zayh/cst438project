from settings import *
import json

class Album:
  
  def __init__(self, data=None):
    ''' Create an empty object '''
    ''' Test with test_createEmptyAccout '''
    self.data = {}
    if data is not None:
      for key in data:
        self.data[key] = data[key]
    
  def getBy(self, column, value):
    ''' Populate the object from the database, using album_id '''
    ''' Test by test_getBy* scripts '''
    success = False
    noSqlErrors = True
    if column == 'album_id':
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor(buffered=True)
        query = ("SELECT * from album where {} = %s".format(column))
        try:
          cursor.execute(query, (value,))
        except mysql.connector.Error as err:
          noSqlErrors = False
        if noSqlErrors == True and cursor.rowcount == 1:
          row = cursor.fetchone()
          self.setAlbumID(row[0])
          self.setReleaseDate(row[1])
          self.setAlbumName(row[2])
          self.setGenre(row[3])
          self.setURLtoBuy(row[4])
          self.setBandID(row[5])
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
    ''' Takes a JSON string and imports it into the object '''
    data = json.loads(jsonStr)
    self.__init__(data)
  
  def addToDatabase(self):
    ''' Adds the current object to the database '''
    ''' Only works on new objects '''
    ''' Test with test_SaveAndDeleteToDatabase() '''
    success = False
    noSqlErrors = True
    if self.getAlbumID() == '' and self.isAlbumNameAvailable() == True:
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("INSERT INTO album (album_name, release_date, genre, url_to_buy, band_id) "
                 "VALUES (%s, %s, %s, %s, %s)")
                 
        try:
          cursor.execute( query, (
            self.getAlbumName(), 
            self.getReleaseDate(), 
            self.getGenre(), 
            self.getURLtoBuy(), 
            self.getBandID() ) 
          )
        except mysql.connector.Error as err:
          noSqlErrors = False        
        if noSqlErrors == True:
          query = ("SELECT album_id FROM album WHERE album_name = %s AND band_id = %s")
          try:
            cursor.execute( query, (
              self.getAlbumName(), 
              self.getBandID() )
            )
          except mysql.connector.Error as err:
            noSqlErrors = False
          if noSqlErrors == True:
            self.setAlbumID(cursor.fetchone()[0])
            if self.getAlbumID() != '':
              cnx.commit()
              success = True 
        cursor.close()
        cnx.close() 
    return success

  # Accessors  
  def getAlbumID(self):
    returnVal = ''
    if 'album_id' in self.data:
      returnVal = self.data['album_id']
    return returnVal
    
  def getAlbumName(self):
    returnVal = ''
    if 'album_name' in self.data:
      returnVal = self.data['album_name']
    return returnVal
    
  def getReleaseDate(self):
    returnVal = ''
    if 'release_date' in self.data:
      returnVal = self.data['release_date']
    return returnVal
    
  def getGenre(self):
    returnVal = ''
    if 'genre' in self.data:
      returnVal = self.data['genre']
    return returnVal
    
  def getURLtoBuy(self):
    returnVal = ''
    if 'url_to_buy' in self.data:
      returnVal = self.data['url_to_buy']
    return returnVal
    
  def getBandID(self):
    returnVal = ''
    if 'band_id' in self.data:
      returnVal = self.data['band_id']
    return returnVal
    
  # Mutators
  # Test with test_Mutators()
  def setAlbumID(self, album_id):
    success = False
    if (1):
      self.data['album_id'] = album_id
      success = True
    return success
  
  def setAlbumName(self, albumname):
    success = False
    if (1):
      self.data['album_name'] = albumname
      success = True
    return success
      
  def setReleaseDate(self, date):
    success = False
    if (1):
      self.data['release_date'] = date
      success = True
    return success
  
  def setGenre(self, genre):
    success = False
    if (1):
      self.data['genre'] = genre
      success = True
    return success
    
  def setURLtoBuy(self, url):
    success = False
    if (1):
      self.data['url_to_buy'] = url
      success = True
    return success
    
  def setBandID(self, band_id):
    success = False
    if (1):
      self.data['band_id'] = band_id
      success = True
    return success
    
  ####

  def isAlbumNameAvailable(self):
    ''' Checks to see if the given albumname is already in use '''
    ''' Test with test_isAlbumNameAvailable '''
    available = False
    noSqlErrors = True
    cnx = connectToDatabase()
    if cnx != False:
      cursor = cnx.cursor(buffered=True)
      query = ("SELECT * FROM album WHERE album_name = %s AND band_id = %s")
      try:
        cursor.execute(query, (self.getAlbumName(), self.getBandID()) )
      except mysql.connector.Error as err:
        noSqlErrors = False
      if noSqlErrors == True and cursor.rowcount == 0:
        available = True
      cursor.close()
      cnx.close()
    return available
    
    
  def deleteFromDatabase(self):
    ''' Deletes the object from the database '''
    ''' Test with test_SaveAndDeleteFromDatabase '''
    success = False
    noSqlErrors = True
    if self.getAlbumID() != '':
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("DELETE FROM album WHERE album_id = %s")
        try:
          cursor.execute(query, (self.getAlbumID(),))
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
    NoSqlErrors = True
    if self.getAlbumID() != '':
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("UPDATE album SET release_date = %s, album_name = %s, genre = %s, url_to_buy = %s, band_id = %s "
          "WHERE album_id = %s")
        try:
          cursor.execute(query, 
            (self.getReleaseDate(), 
            self.getAlbumName(), 
            self.getGenre(), 
            self.getURLtoBuy(),
            self.getBandID(),
            self.getAlbumID()) 
          )
        except mysql.connector.Error as err:
          NoSqlErrors = False
        if NoSqlErrors == True:
          cnx.commit()
          self.getBy('album_id', self.getAlbumID())
          success = True
        cursor.close()
        cnx.close()
    return success
    