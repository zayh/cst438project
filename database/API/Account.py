from settings import *
import json
import hashlib

class Account:
  
  def __init__(self, username='', firstname='', lastname='', lyric=''):
    ''' Create an object '''
    ''' Test with test_create '''
    self.data = { 
      'account_id': '',
      'username'  : username,
      'firstname' : firstname,
      'lastname'  : lastname,
      'lyric'     : lyric,
    }

  def getBy(self, column, value):
    ''' Populate the object from the database, using either account_id or username '''
    ''' Test by test_getBy* scripts '''
    success = False
    NoSqlErrors = True
    if column == 'username' or column == 'account_id':
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor(buffered=True)
        query = ("SELECT * from account WHERE {} = %s".format(column))
        try:
          cursor.execute(query, (value,))
        except mysql.connector.Error as err:
          NoSqlErrors = False
        if NoSqlErrors == True and cursor.rowcount == 1:
          row = cursor.fetchone()
          self.setAccountID(row[0]) 
          self.setUsername(row[1])
          self.setFirstname(row[2]) 
          self.setLastname(row[3])  
          self.setLyric(row[4])
          self.setPassword(row[5])
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
    ''' Takes a jsonStr and populates data '''
    success = False
    data = json.loads(jsonStr)
    if self.setAccountID(data['account_id']) == True:
      if self.setUsername(data['username']) == True:
        if self.setFirstname(data['firstname']) == True:
          if self.setLastname(data['lastname']) == True:
            if self.setLyric(data['lyric']) == True:
              if self.setPassword(data['password']) == True:
                success = True
    return success
  
  def addToDatabase(self):
    ''' Adds the current object to the database '''
    ''' Only works on new objects '''
    ''' Test with test_SaveAndDeleteToDatabase() '''
    success = False
    NoSqlErrors = True
    if self.getAccountID() == '' and self.getPassword() != '':
      cnx = connectToDatabase() 
      if cnx != False:
        cursor = cnx.cursor()
        query = ("INSERT INTO account " 
          "(username, firstname, lastname, lyric, password) "
          "VALUES(%s, %s, %s, %s, %s)"
        )
        try: 
          cursor.execute(query, 
            (self.getUsername(),
            self.getFirstname(),
            self.getLastname(),
            self.getLyric(),
            self.getPassword())
          )
        except mysql.connector.Error as err:
          NoSqlErrors = False
        if NoSqlErrors == True:
          cnx.commit()
          success = True
          self.getBy('username', self.getUsername())
        cursor.close()
        cnx.close()
    return success

  # Accessors  
  def getAccountID(self):
    return self.data['account_id']
    
  def getUsername(self):
    return self.data['username']
    
  def getFirstname(self):
    return self.data['firstname']
    
  def getLastname(self):
    return self.data['lastname']
    
  def getLyric(self):
    return self.data['lyric']
    
  def getPassword(self):
    returnValue = ''
    if 'password' in self.data:
      returnValue = self.data['password']
    return returnValue

  # Mutators
  # Test with test_Mutators()
  def setAccountID(self, account_id):
    success = False
    if (1):
      self.data['account_id'] = account_id
      success = True
    return success
  
  def setUsername(self, username):
    success = False
    if (1):
      self.data['username'] = username
      success = True
    return success
      
  def setFirstname(self, firstname):
    success = False
    if (1):
      self.data['firstname'] = firstname
      success = True
    return success
      
  def setLastname(self, lastname):
    success = False
    if (1):
      self.data['lastname'] = lastname
      success = True
    return success
  
  def setLyric(self, lyric):
    success = False
    if (1):
      self.data['lyric'] = lyric
      success = True
    return success
     
  def setPassword(self, password ):
    success = False
    if (1):
      self.data['password'] = password
      success = True
    return success
  
  def addPassword(self, passwordInText):
    success = False
    if (1):
      self.setPassword(self.hashPassword(passwordInText))
      success = True
    return success
    
  def hashPassword(self, passwordInText):
    return hashlib.sha256( passwordInText.encode('utf-8') ).hexdigest()
  ####
  
  def checkPassword(self, passwordInText):
    if self.getPassword() == self.hashPassword(passwordInText):
      return True
    else:
      return False

  def isUsernameAvailable(self):
    ''' Checks to see if the given username is already in use '''
    ''' Test with test_isUsernameAvailable '''
    available = False
    NoSqlErrors = True
    cnx = connectToDatabase()
    if cnx != False:
      cursor = cnx.cursor(buffered=True)
      query = ("SELECT username FROM account where username = %s")
      try:
        cursor.execute(query,(self.getUsername(),))
      except mysql.connector.Error as err:
        NoSqlErrors = False
      if NoSqlErrors == True and cursor.rowcount == 0:
        available = True        
      cursor.close()
      cnx.close()
    return available
    
  def deleteFromDatabase(self):
    ''' Deletes the object from the database '''
    ''' Test with test_SaveAndDeleteFromDatabase '''
    success = False
    NoSqlErrors = True
    if self.getAccountID() != '':
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("DELETE FROM account WHERE account_id = %s")
        try:
          cursor.execute(query, (self.getAccountID(),))
        except mysql.connector.Error as err:
          NoSqlErrors = False
        if NoSqlErrors == True:
          cnx.commit()
          success = True
        cursor.close()
        cnx.close()
    return success
 
  def saveToDatabase(self):
    ''' Saves current object to the database, using account_id '''
    success = False
    NoSqlErrors = True
    if self.getAccountID() != '':
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("UPDATE account SET username = %s, firstname = %s, lastname = %s, lyric = %s, password = %s "
          "WHERE account_id = %s")
        try:
          cursor.execute(query, 
            (self.getUsername(), 
            self.getFirstname(), 
            self.getLastname(), 
            self.getLyric(),
            self.getPassword(),
            self.getAccountID(),) 
          )
        except mysql.connector.Error as err:
          NoSqlErrors = False
        if NoSqlErrors == True:
          cnx.commit()
          self.getBy('account_id', self.getAccountID())
          success = True
        cursor.close()
        cnx.close()
    return success
        
        