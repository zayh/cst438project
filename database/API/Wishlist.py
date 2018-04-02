from settings import *
import json

class Wishlist:
  
  def __init__(self, data=None):
    ''' Create an empty object '''
    ''' Test with test_createEmptyAccout '''
    self.data = {}
    if data is not None:
      for key in data:
        self.data[key] = data[key]


  def getBy(self, column, value):
    ''' Populate the object from the database, using wishlist_id '''
    ''' Test by test_getBy* scripts '''
    success = False
    noSqlErrors = True
    if column == 'wishlist_id':
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor(buffered=True)
        query = ("SELECT * from wishlist where {} = %s".format(column))
        try:
          cursor.execute(query, (value,))
        except mysql.connector.Error as err:
          noSqlErrors = False
        if noSqlErrors == True and cursor.rowcount == 1:
          row = cursor.fetchone()
          self.setWishlistID(row[0])
          self.setAccountID(row[1])
          self.setAlbumID(row[2])
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
    if self.getWishlistID() == '' and self.notDuplicateWishlist() == True:
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("INSERT INTO wishlist (account_id, album_id) "
                 "VALUES (%s, %s)")
                 
        try:
          cursor.execute( query, (self.getAccountID(), self.getAlbumID()) )
        except mysql.connector.Error as err:
          noSqlErrors = False
        
        if noSqlErrors == True:
          query = ("SELECT wishlist_id FROM wishlist WHERE account_id = %s AND album_id = %s")
          try:
            cursor.execute( query, (self.getAccountID(), self.getAlbumID()) )
          except mysql.connector.Error as err:
            noSqlErrors = False
          if noSqlErrors == True:
            self.setWishlistID(cursor.fetchone()[0])
            if self.getWishlistID() != '':
              cnx.commit()
              success = True
        cursor.close()
        cnx.close()
    return success

  # Accessors  
  def getWishlistID(self):
    returnVal = ''
    if 'wishlist_id' in self.data:
      returnVal = self.data['wishlist_id']
    return returnVal
    
  def getAccountID(self):
    returnVal = ''
    if 'account_id' in self.data:
      returnVal = self.data['account_id']
    return returnVal
    
  def getAlbumID(self):
    returnVal = ''
    if 'album_id' in self.data:
      returnVal = self.data['album_id']
    return returnVal

  # Mutators
  # Test with test_Mutators()
  def setWishlistID(self, wishlist_id):
    success = False
    if (1):
      self.data['wishlist_id'] = wishlist_id
      success = True
    return success
  
  def setAccountID(self, account_id):
    success = False
    if (1):
      self.data['account_id'] = account_id
      success = True
    return success
    
  def setAlbumID(self, album_id):
    success = False
    if (1):
      self.data['album_id'] = album_id
      success = True
    return success
    
  ####

  def notDuplicateWishlist(self):
    ''' Checks to see if the user has commented already '''
    ''' Test with test_notDuplicateComment '''
    notDuplicate = False
    noSqlErrors = True
    cnx = connectToDatabase()
    if cnx != False:
      cursor = cnx.cursor(buffered=True)
      query = ("SELECT * FROM wishlist WHERE account_id = %s AND album_id = %s")
      try:
        cursor.execute(query, (self.getAccountID(), self.getAlbumID()) )
      except mysql.connector.Error as err:
        noSqlErrors = False
      if noSqlErrors == True and cursor.rowcount == 0:
        notDuplicate = True
      cursor.close()
      cnx.close()
    return notDuplicate
    
    
  def deleteFromDatabase(self):
    ''' Deletes the object from the database '''
    ''' Test with test_SaveAndDeleteFromDatabase '''
    success = False
    noSqlErrors = True
    if self.getWishlistID() != '':
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("DELETE FROM wishlist WHERE wishlist_id = %s")
        try:
          cursor.execute(query, (self.getWishlistID(),))
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
    if self.getWishlistID() != '':
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("UPDATE wishlist SET account_id = %s, album_id = %s "
          "WHERE wishlist_id = %s")
        try:
          cursor.execute(query, 
            (self.getAccountID(), self.getAlbumID(), self.getWishlistID()) 
          )
        except mysql.connector.Error as err:
          NoSqlErrors = False
        if NoSqlErrors == True:
          cnx.commit()
          self.getBy('wishlist_id', self.getWishlistID())
          success = True
        cursor.close()
        cnx.close()
    return success
  