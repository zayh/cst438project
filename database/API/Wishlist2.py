from settings import *
import json

class Wishlist(DatabaseObject):
  
  def __init__(self, data=None):
    DatabaseObject.__init__(self, data)
    self.data['table_name'] = 'wishlist'
    self.data['table_layout'] = {
      '0': 'wishlist_id',
      '1': 'account_id',
      '2': 'album_id'
    }

  def notDuplicate(self):
    ''' Checks to see if the user has commented already '''
    ''' Test with test_notDuplicateComment '''
    notDuplicate = False
    noSqlErrors = True
    cnx = connectToDatabase()
    if cnx != False:
      cursor = cnx.cursor(buffered=True)
      query = ("SELECT * FROM wishlist WHERE account_id = %s AND album_id = %s")
      try:
        cursor.execute(query, (self.getItem('account_id'), self.getItem('album_id')) )
      except mysql.connector.Error as err:
        noSqlErrors = False
      if noSqlErrors == True and cursor.rowcount == 0:
        notDuplicate = True
      cursor.close()
      cnx.close()
    return notDuplicate
    
  