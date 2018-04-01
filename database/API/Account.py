import mysql.connector
import hashlib

class Account:
  
  def __init__(self):
    ''' Create an empty object '''
    ''' Test with test_createEmptyAccout '''
    self.account_id = ''
    self.username = ''
    self.firstname = ''
    self.lastname = ''
    self.lyric = ''
    self.password = ''
    
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
    
  def new(self, username, firstname, lastname, lyric, passwordInText):
    ''' Populate the current object '''
    ''' Test with test_new '''
    self.username = username
    self.firstname = firstname
    self.lastname = lastname
    self.lyric = lyric
    # Encode, hash, and store the password        
    self.password = hashlib.sha256( passwordInText.encode('utf-8') ).hexdigest()
    
  def getBy(self, column, value):
    ''' Populate the object from the database, using either account_id or username '''
    ''' Test by test_getBy* scripts '''
    if column == 'username' or column == 'account_id':
      cnx = self.connectToDatabase()
      if (cnx == False):
        returnValue = False
      else:
        cursor = cnx.cursor(buffered=True)
        query = ("SELECT * from account WHERE {} = %s".format(column))
        cursor.execute(query, (value,))
      
        if cursor.rowcount != 1:
          cursor.close()
          returnValue = False
        else:
          row = cursor.fetchone()
          self.account_id = row[0] 
          self.username = row [1] 
          self.firstname = row [2] 
          self.lastname = row [3]  
          self.lyric = row[4]
          self.password = row[5]
          returnValue = True
        
        cursor.close()
        cnx.close()
    else:
      returnValue = False
      
    return returnValue  
  
  def toJSON(self):
    ''' Returns a JSON string of the object. '''
    ''' Test with test_toJSON '''
    jsonStr = "{{ account_id: {}, username: '{}', firstname: '{}', lastname: '{}', lyric: '{}' }}".format(self.account_id, 
      self.username, self.firstname, self.lastname, self.lyric)
    return jsonStr
  
  def addToDatabase(self):
    ''' Adds the current object to the database '''
    ''' Only works on new objects '''
    ''' Test with test_SaveAndDeleteToDatabase() '''
    isAdded = False
    if self.getAccountID() == '':
      cnx = self.connectToDatabase() 
      if cnx == False:
        isAdded = False
      else:
        cursor = cnx.cursor()
        query = ("INSERT INTO account " 
          "(username, firstname, lastname, lyric, password) "
          "VALUES(%s, %s, %s, %s, %s)"
        )
        cursor.execute(query, 
          (self.username,
          self.firstname,
          self.lastname,
          self.lyric,
          self.password)
        )
        cnx.commit()
        cursor.close()
        cnx.close()
        self.getBy('username', self.username)
        isAdded = True
    else:
      isAdded = False
    return isAdded

  # Accessors  
  def getAccountID(self):
    return self.account_id
    
  def getUsername(self):
    return self.username
    
  def getFirstname(self):
    return self.firstname
    
  def getLastname(self):
    return self.lastname
    
  def getLyric(self):
    return self.lyric
    
  def getPassword(self):
    return self.password

  # Mutators
  # Test with test_Mutators()
  def setUsername(self, username):
    if self.isUsernameAvailable(username):
      self.username = username
      return True
    else:
      return False
      
  def setFirstname(self, firstname):
    if True:
      self.firstname = firstname
      return True
    else:
      return False
      
  def setLastname(self, lastname):
    if True:
      self.lastname = lastname
      return True
    else:
      return False
  
  def setLyric(self, lyric):
    if True:
      self.lyric = lyric
      return True
    else:
      return False
     
  def setPassword(self, passwordInText):
    if True:
      self.password = hashlib.sha256( passwordInText.encode('utf-8') ).hexdigest()
      return True
    else:
      return False
  
  ####
  
  def checkPassword(self, passwordInText):
    if self.password == hashlib.sha256( passwordInText.encode('utf-8') ).hexdigest():
      return True
    else:
      return False

  def isUsernameAvailable(self, username):
    ''' Checks to see if the given username is already in use '''
    ''' Test with test_isUsernameAvailable '''
    available = False;
    cnx = self.connectToDatabase()
    if cnx == False:
      available = False
    else:
      cursor = cnx.cursor(buffered=True)
      query = ("SELECT username FROM account where username = %s")
      cursor.execute(query,(username,))
      if cursor.rowcount > 0:
        available = False
      else:
        available = True
      
      cursor.close()
      cnx.close()
    return available
    
  def deleteFromDatabase(self):
    ''' Deletes the object from the database '''
    ''' Test with test_SaveAndDeleteFromDatabase '''
    success = False
    if self.getAccountID != '':
      cnx = self.connectToDatabase()
      if cnx == False:
        success = False
      else:
        cursor = cnx.cursor()
        query = ("DELETE FROM account WHERE account_id = %s")
        cursor.execute(query, (self.account_id,))
        cnx.commit()
        success = True
        cursor.close()
        cnx.close()
    else:
      success = False
    return success
  