from settings import *
import json

class Rating:
  
  def __init__(self, data=None):
    ''' Create an empty object '''
    ''' Test with test_createEmptyAccout '''
    self.data = {}
    if data is not None:
      for key in data:
        self.data[key] = data[key]    
    
  def getBy(self, column, value):
    ''' Populate the object from the database, using rating_id '''
    ''' Test by test_getBy* scripts '''
    success = False
    noSqlErrors = True
    if column == 'rating_id':
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor(buffered=True)
        query = ("SELECT * from rating where {} = %s".format(column))
        try:
          cursor.execute(query, (value,))
        except mysql.connector.Error as err:
          noSqlErrors = False
        if noSqlErrors == True and cursor.rowcount == 1:
          row = cursor.fetchone()
          self.setRatingID(row[0])
          self.setAccountID(row[1])
          self.setAlbumID(row[2])
          self.setRating(row[3])
          self.setComment(row[4])
          self.setDate(row[5])
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
      self.__init__(json.loads(jsonStr))    
  
  def addToDatabase(self):
    ''' Adds the current object to the database '''
    ''' Only works on new objects '''
    ''' Test with test_SaveAndDeleteToDatabase() '''
    success = False
    noSqlErrors = True
    if self.getRatingID() == '' and self.notDuplicateComment() == True:
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("INSERT INTO rating (account_id, date, rating, comment, album_id) "
                 "VALUES (%s, %s, %s, %s, %s)")      
        try:
          cursor.execute( query, (
            self.getAccountID(), 
            self.getDate(), 
            self.getRating(), 
            self.getComment(), 
            self.getAlbumID() ) 
          )
        except mysql.connector.Error as err:
          noSqlErrors = False
        if noSqlErrors == True:
          query = ("SELECT rating_id FROM rating WHERE account_id = %s AND album_id = %s")
          try:
            cursor.execute( query, (self.getAccountID(), self.getAlbumID()) )
          except mysql.connector.Error as err:
            noSqlErrors = False
          if noSqlErrors == True and self.setRatingID(cursor.fetchone()[0]):
            if self.getRatingID() != '':
              cnx.commit()
              success = True
        cursor.close()
        cnx.close()
    return success

  # Accessors  
  def getRatingID(self):
    returnVal = ''
    if 'rating_id' in self.data:
      returnVal = self.data['rating_id']
    return returnVal
    
  def getAccountID(self):
    returnVal = ''
    if 'account_id' in self.data:
      returnVal = self.data['account_id']
    return returnVal
    
  def getDate(self):
    returnVal = ''
    if 'date' in self.data:
      returnVal = self.data['date']
    return returnVal
    
  def getRating(self):
    returnVal = ''
    if 'rating' in self.data:
      returnVal = self.data['rating']
    return returnVal
  
  def getComment(self):
    returnVal = ''
    if 'comment' in self.data:
      returnVal = self.data['comment']
    return returnVal
    
  def getAlbumID(self):
    returnVal = ''
    if 'album_id' in self.data:
      returnVal = self.data['album_id']
    return returnVal

  # Mutators
  # Test with test_Mutators()
  def setRatingID(self, rating_id):
    success = False
    if (1):
      self.data['rating_id'] = rating_id
      success = True
    return success
  
  def setAccountID(self, account_id):
    success = False
    if (1):
      self.data['account_id'] = account_id
      success = True
    return success
      
  def setDate(self, date):
    success = False
    if (1):
      self.data['date'] = date
      success = True
    return success
  
  def setRating(self, rating):
    success = False
    if (1):
      self.data['rating'] = rating
      success = True
    return success
    
  def setComment(self, url):
    success = False
    if (1):
      self.data['comment'] = url
      success = True
    return success
    
  def setAlbumID(self, album_id):
    success = False
    if (1):
      self.data['album_id'] = album_id
      success = True
    return success
    
  ####

  def notDuplicateComment(self):
    ''' Checks to see if the user has commented already '''
    ''' Test with test_notDuplicateComment '''
    notDuplicateComment = False
    noSqlErrors = True
    cnx = connectToDatabase()
    if cnx != False:
      cursor = cnx.cursor(buffered=True)
      query = ("SELECT * FROM rating WHERE account_id = %s AND album_id = %s")
      try:
        cursor.execute(query, (self.getAccountID(),self.getAlbumID()))
      except mysql.connector.Error as err:
        noSqlErrors = False
      if noSqlErrors == True and cursor.rowcount == 0:
        notDuplicateComment = True
      cursor.close()
      cnx.close()
    return notDuplicateComment
    
  def deleteFromDatabase(self):
    ''' Deletes the object from the database '''
    ''' Test with test_SaveAndDeleteFromDatabase '''
    success = False
    noSqlErrors = True
    if self.getRatingID() != '':
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("DELETE FROM rating WHERE rating_id = %s")
        try:
          cursor.execute(query, (self.getRatingID(),))
        except mysql.connector.Error as err:
          noSqlErrors = True
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
    if self.getRatingID() != '':
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("UPDATE rating SET account_id = %s, album_id = %s, rating = %s, comment = %s, date = %s "
          "WHERE rating_id = %s")
        try:
          cursor.execute(query, (
            self.getAccountID(), 
            self.getAlbumID(), 
            self.getRating(), 
            self.getComment(), 
            self.getDate(), 
            self.getRatingID() ) 
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
  