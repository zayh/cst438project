from settings import *
import json

class Band:
  
  def __init__(self, data=None):
    ''' Create an object '''
    ''' Test with test_createAccout '''
    self.data = { }
    if data is not None:
      for key in data:
        self.data[key] = data[key]

  def getBy(self, column, value):
    ''' Populate the object from the database, using either band_id or band_name '''
    ''' Test by test_getBy* scripts '''
    success = False
    NoSqlErrors = True
    if column == 'band_name' or column == 'band_id':
      cnx = connectToDatabase()
      if cnx != False:
        query = ("SELECT * from band where {} = %s".format(column))
        cursor = cnx.cursor(buffered=True)
        try:
          cursor.execute(query, (value,))
        except mysql.connector.Error as err:
          NoSqlErrors = False
        if NoSqlErrors == True:
          if cursor.rowcount == 1:
            row = cursor.fetchone()
            self.setBandID(row[0])
            self.setSoloArtist(row[1])
            self.setBandName(row[2])
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
    ''' Takes a jsonStr and converts it into an object '''
    success = False
    data = json.loads(jsonStr)
    self.__init__(data)
    success = True
    return success
  
  def addToDatabase(self):
    ''' Adds the current object to the database '''
    ''' Only works on new objects '''
    ''' Test with test_SaveAndDeleteToDatabase() '''
    success = False
    NoSqlErrors = True
    if self.getBandID() == '' and self.isBandNameAvailable() == True:
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("INSERT INTO band (band_name, is_solo_artist) VALUES (%s, %s)")
        try:
          cursor.execute( query, (self.getBandName(), self.isSoloArtist('int')) )
        except mysql.connector.Error as err:
          NoSqlErrors = False
        if NoSqlErrors == True:
          cnx.commit()
          success = True
        cursor.close()
        cnx.close()
    return success

  # Accessors  
  def getBandID(self):
    returnVal = ''
    if 'band_id' in self.data:
      returnVal = self.data['band_id']
    return returnVal
    
  def getBandName(self):
    returnVal = ''
    if 'band_name' in self.data:
      returnVal = self.data['band_name']
    return returnVal
    
  def isSoloArtist(self, outputFormat='bool'):
    returnVal = ''
    if 'is_solo_artist' in self.data:
      returnVal = self.data['is_solo_artist']
    if outputFormat == 'int':
      if returnVal == True:
        returnVal = 1
      else:
        returnVal = 0
    return returnVal

  # Mutators
  # Test with test_Mutators()
  def setBandID(self, band_id):
    success = False
    if (1):
      self.data['band_id'] = band_id
      success = True
    return success
  
  def setBandName(self, bandname):
    success = False
    if (1):
      self.data['band_name'] = bandname
      success =  True
    return success
      
  def setSoloArtist(self, boolean):
    success = False;
    if type(boolean) == type(int):
      if boolean == 1:
        self.data['is_solo_artist'] = True;
        success = True
      elif boolean == 0:
        self.data['is_solo_artist'] = False;
        sucess = True
    elif type(boolean) == type(True):  
      self.data['is_solo_artist'] = boolean
      success = True
    return success
  
  ####

  def isBandNameAvailable(self):
    ''' Checks to see if the given bandname is already in use '''
    ''' Test with test_isBandNameAvailable '''
    available = False
    noSqlErrors = True
    cnx = connectToDatabase()
    if cnx != False:
      cursor = cnx.cursor(buffered=True)
      query = ("SELECT * FROM band WHERE band_name = %s")
      try:
        cursor.execute(query, (self.getBandName(),))
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
    if self.getBandID() != '':
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("DELETE FROM band WHERE band_id = %s")
        try:
          cursor.execute(query, (self.getBandID(),))
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
    if self.getBandID() != '':
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("UPDATE band SET band_name = %s, is_solo_artist = %s "
          "WHERE band_id = %s")
        try:
          cursor.execute(query, 
            (self.getBandName(), self.isSoloArtist('int'), self.getBandID()) 
          )
        except mysql.connector.Error as err:
          noSqlErrors = False
        if noSqlErrors == True:
          cnx.commit()
          self.getBy('band_id', self.getBandID())
          success = True
        cursor.close()
        cnx.close()
    return success
    