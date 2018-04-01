import mysql.connector
import hashlib

class Favorite:
  
  def __init__(self):
    ''' Create an empty object '''
    ''' Test with test_createEmptyAccout '''
    self.favorite_id = ''
    self.account_id = ''
    self.album_id = ''
    
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
    
  def new(self, account_id, album_id):
    ''' Populate the current object '''
    ''' Test with test_new '''
    success = False
  
    self.account_id = account_id
    self.album_id = album_id
    success = True
      
    return success
    
    
  def getBy(self, column, value):
    ''' Populate the object from the database, using favorite_id '''
    ''' Test by test_getBy* scripts '''
    success = False
    if column == 'favorite_id':
      cnx = self.connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor(buffered=True)
        query = ("SELECT * from favorite where {} = %s".format(column))
        cursor.execute(query, (value,))
        if cursor.rowcount == 1:
          row = cursor.fetchone()
          self.favorite_id = row[0]
          self.account_id = row[1]
          self.album_id = row[2]
          success = True
        cursor.close()
        cnx.close()
    return success
  
  def toJSON(self):
    ''' Returns a JSON string of the object. '''
    ''' Test with test_toJSON '''
    jsonStr = "{{ favorite_id: {}, account_id: {}, album_id: {} }}".format(self.favorite_id, 
      self.account_id, self.album_id)
    return jsonStr
  
  def addToDatabase(self):
    ''' Adds the current object to the database '''
    ''' Only works on new objects '''
    ''' Test with test_SaveAndDeleteToDatabase() '''
    success = False
    noErrors = True
    if self.getFavoriteID() == '' and self.notDuplicateFavorite(self.account_id, self.album_id) == True:
      cnx = self.connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("INSERT INTO favorite (account_id, album_id) "
                 "VALUES (%s, %s)")
                 
        try:
          cursor.execute( query, (self.account_id, self.album_id) )
        except mysql.connector.Error as err:
          noErrors = False
        
        if noErrors == True:
          query = ("SELECT favorite_id FROM favorite WHERE account_id = %s AND album_id = %s")
          cursor.execute( query, (self.account_id, self.album_id))
          self.setFavoriteID(cursor.fetchone()[0])
          if self.getFavoriteID() != '':
            cnx.commit()
            success = True

        cursor.close()
        cnx.close()

    return success

  # Accessors  
  def getFavoriteID(self):
    return self.favorite_id
    
  def getAccountID(self):
    return self.account_id
    
  def getAlbumID(self):
    return self.album_id

  # Mutators
  # Test with test_Mutators()
  def setFavoriteID(self, favorite_id):
    success = False
    if (1):
      self.favorite_id = favorite_id
      success = True
    return success
  
  def setAccountID(self, account_id):
    success = False
    if (1):
      self.account_id = account_id
      success = True
    return success
    
  def setAlbumID(self, album_id):
    success = False
    if (1):
      self.album_id = album_id
      success = True
    return success
    
  ####

  def notDuplicateFavorite(self, account_id, album_id):
    ''' Checks to see if the user has commented already '''
    ''' Test with test_notDuplicateComment '''
    notDuplicate = False
    cnx = self.connectToDatabase()
    if cnx != False:
      cursor = cnx.cursor(buffered=True)
      query = ("SELECT * FROM favorite WHERE account_id = %s AND album_id = %s")
      cursor.execute(query, (account_id,album_id))
      if cursor.rowcount < 1:
        notDuplicate = True
      cursor.close()
      cnx.close()

    return notDuplicate
    
    
  def deleteFromDatabase(self):
    ''' Deletes the object from the database '''
    ''' Test with test_SaveAndDeleteFromDatabase '''
    success = False
    if self.getFavoriteID() != '':
      cnx = self.connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("DELETE FROM favorite WHERE favorite_id = %s")
        cursor.execute(query, (self.getFavoriteID(),))
        cnx.commit()
        cursor.close()
        cnx.close()
        success = True
    return success
  
  def saveToDatabase(self):
    ''' Saves current object to the database, using the primary index '''
    success = False
    NoSqlErrors = True
    if self.getFavoriteID() != '':
      cnx = self.connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("UPDATE favorite SET account_id = %s, album_id = %s "
          "WHERE favorite_id = %s")
        try:
          cursor.execute(query, 
            (self.getAccountID(), self.getAlbumID(), self.getFavoriteID()) 
          )
        except mysql.connector.Error as err:
          NoSqlErrors = False
        if NoSqlErrors == True:
          cnx.commit()
          self.getBy('favorite_id', self.getFavoriteID())
          success = True
        cursor.close()
        cnx.close()
    return success
    