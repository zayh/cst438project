import mysql.connector
import hashlib

class Band:
  
  def __init__(self):
    ''' Create an empty object '''
    ''' Test with test_createEmptyAccout '''
    self.band_id = ''
    self.band_name = ''
    self.is_solo_artist = False
    
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
    
  def new(self, band_name):
    ''' Populate the current object '''
    ''' Test with test_new '''
    if self.isBandNameAvailable(band_name):
      self.band_name = band_name
    
  def getBy(self, column, value):
    ''' Populate the object from the database, using either band_id or band_name '''
    ''' Test by test_getBy* scripts '''
    success = False
    if column == 'band_name' or column == 'band_id':
      cnx = self.connectToDatabase()
      if cnx == False:
        success = False
      else:
        cursor = cnx.cursor(buffered=True)
        query = ("SELECT * from band where {} = %s".format(column))
        cursor.execute(query, (value,))
        if cursor.rowcount == 1:
          row = cursor.fetchone()
          self.band_id = row[0]
          self.band_name = row[2]
          if row[1] == 0:
            self.setSoloArtist(False)
          else:
            self.setSoloArtist(True)
          success = True
        cursor.close()
        cnx.close()
    else:
      success = False
    return success
  
  def toJSON(self):
    ''' Returns a JSON string of the object. '''
    ''' Test with test_toJSON '''
    jsonStr = "{{ band_id: {}, band_name: '{}', is_solo_artist: '{}' }}".format(self.band_id, 
      self.band_name, self.is_solo_artist)
    return jsonStr
  
  def addToDatabase(self):
    ''' Adds the current object to the database '''
    ''' Only works on new objects '''
    ''' Test with test_SaveAndDeleteToDatabase() '''
    success = False
    if self.getBandID() == '':
      cnx = self.connectToDatabase()
      if cnx != False:
        if self.isSoloArtist() == True:
          soloArtist = 1
        else:
          soloArtist = 0
        cursor = cnx.cursor()
        query = ("INSERT INTO band (band_name, is_solo_artist) VALUES (%s, %s)")
        cursor.execute( query, (self.band_name, soloArtist) )
        cnx.commit()
        cursor.close()
        cnx.close()
    else:
      success = False
    return success

  # Accessors  
  def getBandID(self):
    return self.band_id
    
  def getBandName(self):
    return self.band_name
    
  def isSoloArtist(self):
    return self.is_solo_artist

  # Mutators
  # Test with test_Mutators()
  def setBandName(self, bandname):
    if self.isBandNameAvailable(bandname):
      self.band_name = bandname
      return True
    else:
      return False
      
  def setSoloArtist(self, boolean):
    self.is_solo_artist = boolean
  
  ####

  def isBandNameAvailable(self, bandname):
    ''' Checks to see if the given bandname is already in use '''
    ''' Test with test_isBandNameAvailable '''
    available = False
    cnx = self.connectToDatabase()
    if cnx != False:
      cursor = cnx.cursor(buffered=True)
      query = ("SELECT * FROM band WHERE band_name = %s")
      cursor.execute(query, (bandname,))
      if cursor.rowcount < 1:
        available = True
      cursor.close()
      cnx.close()
    return available
    
  def deleteFromDatabase(self):
    ''' Deletes the object from the database '''
    ''' Test with test_SaveAndDeleteFromDatabase '''
    success = False
    if self.getBandID() != '':
      cnx = self.connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("DELETE FROM band WHERE band_id = %s")
        cursor.execute(query, (self.getBandID(),))
        cnx.commit()
        cursor.close()
        cnx.close()
        success = True
    return success
  