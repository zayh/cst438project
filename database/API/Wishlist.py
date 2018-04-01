import mysql.connector
import hashlib

class Wishlist:
  
  def __init__(self):
    ''' Create an empty object '''
    ''' Test with test_createEmptyAccout '''
    self.wishlist_id = ''
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
    ''' Populate the object from the database, using wishlist_id '''
    ''' Test by test_getBy* scripts '''
    success = False
    if column == 'wishlist_id':
      cnx = self.connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor(buffered=True)
        query = ("SELECT * from wishlist where {} = %s".format(column))
        cursor.execute(query, (value,))
        if cursor.rowcount == 1:
          row = cursor.fetchone()
          self.wishlist_id = row[0]
          self.account_id = row[1]
          self.album_id = row[2]
          success = True
        cursor.close()
        cnx.close()
    return success
  
  def toJSON(self):
    ''' Returns a JSON string of the object. '''
    ''' Test with test_toJSON '''
    jsonStr = "{{ wishlist_id: {}, account_id: {}, album_id: {} }}".format(self.wishlist_id, 
      self.account_id, self.album_id)
    return jsonStr
  
  def addToDatabase(self):
    ''' Adds the current object to the database '''
    ''' Only works on new objects '''
    ''' Test with test_SaveAndDeleteToDatabase() '''
    success = False
    noErrors = True
    if self.getWishlistID() == '' and self.notDuplicateWishlist(self.account_id, self.album_id) == True:
      cnx = self.connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("INSERT INTO wishlist (account_id, album_id) "
                 "VALUES (%s, %s)")
                 
        try:
          cursor.execute( query, (self.account_id, self.album_id) )
        except mysql.connector.Error as err:
          noErrors = False
        
        if noErrors == True:
          query = ("SELECT wishlist_id FROM wishlist WHERE account_id = %s AND album_id = %s")
          cursor.execute( query, (self.account_id, self.album_id))
          self.setWishlistID(cursor.fetchone()[0])
          if self.getWishlistID() != '':
            cnx.commit()
            success = True

        cursor.close()
        cnx.close()

    return success

  # Accessors  
  def getWishlistID(self):
    return self.wishlist_id
    
  def getAccountID(self):
    return self.account_id
    
  def getAlbumID(self):
    return self.album_id

  # Mutators
  # Test with test_Mutators()
  def setWishlistID(self, wishlist_id):
    success = False
    if (1):
      self.wishlist_id = wishlist_id
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

  def notDuplicateWishlist(self, account_id, album_id):
    ''' Checks to see if the user has commented already '''
    ''' Test with test_notDuplicateComment '''
    notDuplicate = False
    cnx = self.connectToDatabase()
    if cnx != False:
      cursor = cnx.cursor(buffered=True)
      query = ("SELECT * FROM wishlist WHERE account_id = %s AND album_id = %s")
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
    if self.getWishlistID() != '':
      cnx = self.connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("DELETE FROM wishlist WHERE wishlist_id = %s")
        cursor.execute(query, (self.getWishlistID(),))
        cnx.commit()
        cursor.close()
        cnx.close()
        success = True
    return success
  