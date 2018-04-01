import mysql.connector
import hashlib

class Rating:
  
  def __init__(self):
    ''' Create an empty object '''
    ''' Test with test_createEmptyAccout '''
    self.rating_id = ''
    self.account_id = ''
    self.date = ''
    self.rating = ''
    self.comment = ''
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
    
  def new(self, account_id, album_id, rating, comment, date):
    ''' Populate the current object '''
    ''' Test with test_new '''
    success = False
  
    self.account_id = account_id
    self.album_id = album_id
    self.date = date
    self.rating = rating
    self.comment = comment
    success = True
      
    return success
    
    
  def getBy(self, column, value):
    ''' Populate the object from the database, using rating_id '''
    ''' Test by test_getBy* scripts '''
    success = False
    if column == 'rating_id':
      cnx = self.connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor(buffered=True)
        query = ("SELECT * from rating where {} = %s".format(column))
        cursor.execute(query, (value,))
        if cursor.rowcount == 1:
          row = cursor.fetchone()
          self.rating_id = row[0]
          self.account_id = row[1]
          self.album_id = row[2]
          self.rating = row[3]
          self.comment = row[4]
          self.date = row[5]
          success = True
        cursor.close()
        cnx.close()
    return success
  
  def toJSON(self):
    ''' Returns a JSON string of the object. '''
    ''' Test with test_toJSON '''
    jsonStr = "{{ rating_id: {}, account_id: {}, album_id: {}, rating: {}, comment: '{}', date: '{}' }}".format(self.rating_id, 
      self.account_id, self.album_id, self.rating, self.comment, self.date)
    return jsonStr
  
  def addToDatabase(self):
    ''' Adds the current object to the database '''
    ''' Only works on new objects '''
    ''' Test with test_SaveAndDeleteToDatabase() '''
    success = False
    noErrors = True
    if self.getRatingID() == '' and self.notDuplicateComment(self.account_id, self.album_id) == True:
      cnx = self.connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("INSERT INTO rating (account_id, date, rating, comment, album_id) "
                 "VALUES (%s, %s, %s, %s, %s)")
                 
        try:
          cursor.execute( query, (self.account_id, self.date, self.rating, self.comment, self.album_id) )
        except mysql.connector.Error as err:
          noErrors = False
        
        if noErrors == True:
          query = ("SELECT rating_id FROM rating WHERE account_id = %s AND album_id = %s")
          cursor.execute( query, (self.account_id, self.album_id))
          self.setRatingID(cursor.fetchone()[0])
          if self.getRatingID() != '':
            cnx.commit()
            success = True

        cursor.close()
        cnx.close()

    return success

  # Accessors  
  def getRatingID(self):
    return self.rating_id
    
  def getAccountID(self):
    return self.account_id
    
  def getDate(self):
    return self.date
    
  def getRating(self):
    return self.rating
  
  def getComment(self):
    return self.comment
    
  def getAlbumID(self):
    return self.album_id

  # Mutators
  # Test with test_Mutators()
  def setRatingID(self, rating_id):
    success = False
    if (1):
      self.rating_id = rating_id
      success = True
    return success
  
  def setAccountID(self, account_id):
    success = False
    if (1):
      self.account_id = account_id
      success = True
    return success
      
  def setDate(self, date):
    success = False
    if (1):
      self.date = date
      success = True
    return success
  
  def setRating(self, rating):
    success = False
    if (1):
      self.rating = rating
      success = True
    return success
    
  def setComment(self, url):
    success = False
    if (1):
      self.comment = url
      success = True
    return success
    
  def setAlbumID(self, album_id):
    success = False
    if (1):
      self.album_id = album_id
      success = True
    return success
    
  ####

  def notDuplicateComment(self, account_id, album_id):
    ''' Checks to see if the user has commented already '''
    ''' Test with test_notDuplicateComment '''
    notDuplicateComment = False
    cnx = self.connectToDatabase()
    if cnx != False:
      cursor = cnx.cursor(buffered=True)
      query = ("SELECT * FROM rating WHERE account_id = %s AND album_id = %s")
      cursor.execute(query, (account_id,album_id))
      if cursor.rowcount < 1:
        notDuplicateComment = True
      cursor.close()
      cnx.close()

    return notDuplicateComment
    
  def deleteFromDatabase(self):
    ''' Deletes the object from the database '''
    ''' Test with test_SaveAndDeleteFromDatabase '''
    success = False
    if self.getRatingID() != '':
      cnx = self.connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("DELETE FROM rating WHERE rating_id = %s")
        cursor.execute(query, (self.getRatingID(),))
        cnx.commit()
        cursor.close()
        cnx.close()
        success = True
    return success
    
  def saveToDatabase(self):
    ''' Saves current object to the database, using the primary index '''
    success = False
    NoSqlErrors = True
    if self.getRatingID() != '':
      cnx = self.connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("UPDATE rating SET account_id = %s, album_id = %s, rating = %s, comment = %s, date = %s "
          "WHERE rating_id = %s")
        try:
          cursor.execute(query, 
            (self.getAccountID(), self.getAlbumID(), 
            self.getRating(), self.getComment(), 
            self.getDate(), self.getRatingID()) 
          )
        except mysql.connector.Error as err:
          NoSqlErrors = False
        if NoSqlErrors == True:
          cnx.commit()
          self.getBy('rating_id', self.getRatingID())
          success = True
        cursor.close()
        cnx.close()
    return success
  