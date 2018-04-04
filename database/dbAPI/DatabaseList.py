import dbAPI.DatabaseObject
from dbAPI.Tables import *
from dbAPI.settings import *
import json

class DatabaseList:

  def __init__(self, table_name=None):
    self.data = {
      'table_name': table_name,
      'classes': {
        'account' : Account,
        'album': Album,
        'band' : Band,
        'favorite': Favorite,
        'map_song_to_album' : MapSongToAlbum,
        'rating' : Rating,
        'song' : Song,
        'wishlist' : Wishlist
      },
      'row_data' : [ ]
    }
    
  def getTable(self):
    returnVal = ''
    if 'table_name' in self.data:
      returnVal = self.data['table_name']
    return returnVal
    
  def setTable(self, table_name):
    success = False
    if (1):
      self.data['table_name'] = table_name
      success = True
    return success    
    
  def clearRows(self):
    ''' Empties the contents of self.data['row_data'] '''
    self.data['row_data'].clear()
    
  def loadRows(self, cursor):
    success = False
    if (1):
      for row in cursor:
          obj = self.data['classes'][self.getTable()]()
          obj.loadRow(row)
          self.data['row_data'].append(obj)        
    success = True
    return success
  
  def searchTable(self, columns, values):
    ''' Takes the name of the table, and a tuple of columns and a tuple of values '''
    ''' Loads row_data with the output ''' 
    success = False
    noSqlErrors = True
    self.clearRows()
    table_name = self.getTable()
    cnx = connectToDatabase()
    
    if cnx != False:
      cursor = cnx.cursor()
      
      columnStr = ''
      for i in range(0, len(columns)):
        if i != 0:
          columnStr += ' AND '
        columnStr += columns[i] + ' = %s'
      
      query = ("SELECT * from {} where {}".format(table_name,columnStr))
      try:
        cursor.execute(query, values)
      except mysql.connector.Error as err:
        noSqlErrors = False
      if noSqlErrors == True and self.loadRows(cursor):
        success = True
      cursor.close()
      cnx.close()     
    return success    
    
  def toJSON(self):
    returnVal = '['
    i = 1
    for obj in self.data['row_data']:
      returnVal += obj.toJSON()
      if i < len(self.data['row_data']):
        i += 1
        returnVal += ', '
    returnVal += ']'
    return returnVal
      

