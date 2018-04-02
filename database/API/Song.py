from settings import *
import json

class Song:
  
  def __init__(self, data=None):
    ''' Create an empty object '''
    ''' Test with test_createEmptyAccout '''
    self.data = {}
    if data is not None:
      for key in data:
        self.data[key] = data[key]
    
  def getBy(self, column, value):
    ''' Populate the object from the database, using song_id '''
    ''' Test by test_getBy* scripts '''
    success = False
    noSqlErrors = True
    if column == 'song_id':
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor(buffered=True)
        query = ("SELECT song_id, song_name, is_solo_release, band_id from song where {} = %s".format(column))
        try:
          cursor.execute(query, (value,))
        except mysql.connector.Error as err:
          noSqlErrors = False
        if noSqlErrors == True and cursor.rowcount == 1:
          row = cursor.fetchone()
          self.setSongID(row[0])
          self.setSongName(row[1])
          self.setSoloRelease(row[2])
          self.setBandID(row[3])
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
    if jsonStr != '':
      data = json.loads(jsonStr)
      self.__init__(data)
  
  def addToDatabase(self):
    ''' Adds the current object to the database '''
    ''' Only works on new objects '''
    ''' Test with test_SaveAndDeleteToDatabase() '''
    success = False
    noSqlErrors = True
    if self.getSongID() == '' and self.isSongNameAvailable():
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("INSERT INTO song (song_name, is_solo_release, band_id) "
                 "VALUES (%s, %s, %s)")
                 
        try:
          cursor.execute( query, (self.getSongName(), self.isSoloRelease('int'), self.getBandID()) )
        except mysql.connector.Error as err:
          noSqlErrors = False
        if noSqlErrors == True:
          query = ("SELECT song_id FROM song WHERE song_name = %s AND band_id = %s")
          try:
            cursor.execute( query, (self.getSongName(), self.getBandID()) )
          except mysql.connector.Error as err:
            noSqlErrors = False
          if noSqlErrors == True:
            self.setSongID(cursor.fetchone()[0])
            if self.getSongID() != '':
              cnx.commit()
              success = True             
        cursor.close()
        cnx.close()
    return success

  # Accessors  
  def getSongID(self):
    returnVal = ''
    if 'song_id' in self.data:
      returnVal = self.data['song_id']
    return returnVal
    
  def getSongName(self):
    returnVal = ''
    if 'song_name' in self.data:
      returnVal = self.data['song_name']
    return returnVal
    
  def isSoloRelease(self, type='bool'):
    returnVal = ''
    if 'is_solo_release' in self.data:
      returnVal = self.data['is_solo_release']
      if type == 'int':
        if returnVal == True:
          returnVal = 1
        else:
          returnVal = 0
    return returnVal
    
  def getBandID(self):
    returnVal = ''
    if 'band_id' in self.data:
      returnVal = self.data['band_id']
    return returnVal

  # Mutators
  # Test with test_Mutators()
  def setSongID(self, song_id):
    success = False
    if (1):
      self.data['song_id'] = song_id
      success = True
    return success
  
  def setSongName(self, songname):
    success = False
    if (1):
      self.data['song_name'] = songname
      success = True
    return success
      
  def setSoloRelease(self, boolean):
    success = False
    if type(boolean) == type(True):
      self.data['is_solo_release'] = boolean
      success = True
    elif type(boolean) == type(1): 
      if boolean == 1:
        self.data['is_solo_release'] = True
        success = True
      elif boolean == 0:
        self.data['is_solo_release'] = False
        success = True
    return success
    
  def setBandID(self, band_id):
    success = False
    if (1):
      self.data['band_id'] = band_id
      success = True
    return success
    
  ####

  def isSongNameAvailable(self):
    ''' Checks to see if the given songname is already in use '''
    ''' Test with test_isSongNameAvailable '''
    available = False
    noSqlErrors = True
    cnx = connectToDatabase()
    if cnx != False:
      cursor = cnx.cursor(buffered=True)
      query = ("SELECT * FROM song WHERE song_name = %s AND band_id = %s")
      try:
        cursor.execute(query, (self.getSongName(),self.getBandID()))
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
    if self.getSongID() != '':
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("DELETE FROM song WHERE song_id = %s")
        try:
          cursor.execute(query, (self.getSongID(),))
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
    if self.getSongID() != '':
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("UPDATE song SET song_name = %s, is_solo_release = %s, band_id = %s "
          "WHERE song_id = %s")
        try:
          cursor.execute(query, (
            self.getSongName(), 
            self.isSoloRelease('int'),
            self.getBandID(),
            self.getSongID()) 
          )
        except mysql.connector.Error as err:
          NoSqlErrors = False
        if NoSqlErrors == True:
          cnx.commit()
          self.getBy('song_id', self.getSongID())
          success = True
        cursor.close()
        cnx.close()
    return success
    