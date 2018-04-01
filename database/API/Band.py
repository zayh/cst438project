from settings import *
import json

class Band:
  
  def __init__(self, name='', solo=False):
    ''' Create an empty object '''
    ''' Test with test_createEmptyAccout '''
    self.data = { 
                  'band_id': '',
                  'band_name': name,
                  'is_solo_artist': solo
                }

  def getBy(self, column, value):
    ''' Populate the object from the database, using either band_id or band_name '''
    ''' Test by test_getBy* scripts '''
    success = False
    if column == 'band_name' or column == 'band_id':
      cnx = connectToDatabase()
      if cnx == False:
        success = False
      else:
        cursor = cnx.cursor(buffered=True)
        query = ("SELECT * from band where {} = %s".format(column))
        cursor.execute(query, (value,))
        if cursor.rowcount == 1:
          row = cursor.fetchone()
          self.setBandID(row[0])
          self.setSoloArtist(row[1])
          self.setBandName(row[2])
          success = True
        cursor.close()
        cnx.close()
    else:
      success = False
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
    if self.setBandID(data['band_id']) == True:
      if self.setBandName(data['band_name']) == True:
        if self.setSoloArtist(data['is_solo_artist']) == True:
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
    return self.data['band_id']
    
  def getBandName(self):
    return self.data['band_name']
    
  def isSoloArtist(self, outputFormat='bool'):
    outputValue = self.data['is_solo_artist']
    if outputFormat == 'int':
      if outputValue == True:
        outputValue = 1
      else:
        outputValue = 0
    return outputValue

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
    if (1) == True:
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
    cnx = connectToDatabase()
    if cnx != False:
      cursor = cnx.cursor(buffered=True)
      query = ("SELECT * FROM band WHERE band_name = %s")
      cursor.execute(query, (self.getBandName(),))
      if cursor.rowcount < 1:
        available = True
      cursor.close()
      cnx.close()
    return available
    
  def deleteFromDatabase(self):
    ''' Deletes the object from the database '''
    ''' Test with test_SaveAndDeleteFromDatabase '''
    success = False
    NoSqlErrors = True
    if self.getBandID() != '':
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("DELETE FROM band WHERE band_id = %s")
        try:
          cursor.execute(query, (self.getBandID(),))
        except mysql.connector.Error as err:
          NoSqlErrors = False
        if NoSqlErrors == True:
          cnx.commit()
          success = True
        cursor.close()
        cnx.close()
    return success
  
  def saveToDatabase(self):
    ''' Saves current object to the database, using the primary index '''
    success = False
    NoSqlErrors = True
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
          NoSqlErrors = False
        if NoSqlErrors == True:
          cnx.commit()
          self.getBy('band_id', self.getBandID())
          success = True
        cursor.close()
        cnx.close()
    return success