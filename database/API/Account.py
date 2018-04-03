from DatabaseObject import DatabaseObject
import hashlib

class Account(DatabaseObject):
  
  def __init__(self, data=None):
    '''
    Creates an Object. If a dict is passed, pass it to the super(), then add the 
    table_name and the table_layout to it.
    Test with test_createObject()
    '''
    DatabaseObject.__init__(self, data)
    self.data['table_name'] = 'account'
    self.data['table_layout'] = {
      '0': 'account_id',
      '1': 'username',
      '2': 'firstname',
      '3': 'lastname',
      '4': 'lyric',
      '5': 'password'
    }
    self.data['unique_combos'] = [
      'username',
    ]
  
  def addPassword(self, passwordInText):
    success = False
    if self.setItem('password', self.hashPassword(passwordInText)):
      success = True
    return success
    
  def hashPassword(self, passwordInText):
    return hashlib.sha256( passwordInText.encode('utf-8') ).hexdigest()
  
  def checkPassword(self, passwordInText):
    success = False
    if self.getItem('password') == self.hashPassword(passwordInText):
      success = True
    return success     
        