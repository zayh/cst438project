from settings import *
import json

class DatabaseObject:

  def __init__(self, data=None):
    ''' Create an empty object '''
    ''' Test with test_createAccout '''
    self.data = {}
    if data is not None:
      for key in data:
        self.data[key] = data[key]
        
  def toJSON(self):
    ''' Returns a JSON string of the object. '''
    ''' Test with test_toJSON '''
    jsonStr = json.dumps(self.data)
    return jsonStr
  
  def fromJSON(self, jsonStr):
    if jsonStr != '':
      data = json.loads(jsonStr)
      self.__init__(data)
      
  def getTable(self):
    returnVal = ''
    if 'table_name' in self.data:
      returnVal = self.data['table_name']
    return returnVal
      
  def getItem(self, column):
    returnVal = ''
    if column in self.data:
      returnVal = self.data[column]
    return returnVal

  def setItem(self, column, value):
    success = False
    if (1):
      self.data[column] = value
      sucess = True
    return success
    
  def getBy(self, column, value):
    ''' 
    Populate the object from the database 
    Only unique indexes will function. 
    If more than 1 row is returned, the object will not be populated
    Test by test_getBy* scripts 
    '''
    
    # Initialize local variables
    select_columns = ''
    success = False
    noSqlErrors = True
    
    cnx = connectToDatabase()
    # Don't proceed if the connection failed
    if cnx != False:
      cursor = cnx.cursor(buffered=True)
      # Use table_layout to make the list of columns
      for key in self.data['table_layout']:
        # is this isn't the first column, add a comma to the end
        if key != '0':
          select_columns = select_columns + ','
        select_columns = select_columns + self.data['table_layout'][key]
      # Now the query can be built
      query = ("SELECT ", select_columns, " from ", self.data['table_name'], " where {} = %s".format(column))
      try:
        cursor.execute(query, (value,))
      # Catch any mysql errors
      except mysql.connector.Error as err:
        noSqlErrors = False
      # Only proceed if there have been no errors
      # Only 1 row returned is allowed as well
      if noSqlErrors == True and cursor.rowcount == 1:
        row = cursor.fetchone()
        # Step through table_layout and assign the data retrieved to self.data using setItem()
        for key in table_layout:
          self.setItem(self.data['table_layout'][key], row[key])
        success = True
      cursor.close()
      cnx.close()
    return success
    
  def addToDatabase(self):
    ''' Adds the current object to the database '''
    ''' Only works on new objects '''
    ''' Test with test_SaveAndDeleteToDatabase() '''
    success = False
    noSqlErrors = True
    table_layout = getItem('table_layout')
    index_column = table_layout['0']
    
    if self.getItem(index_column) == '' and self.notDuplicate() == True:
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()

        columns = '('
        for key in table_layout:
          if key != '0':
            if key !='1':
              columns = colums + ','
            columns = columns + table_layout[key]
        columns = columns + ')'
        placeholder = '('
        for (i = 1; i < length(table_layout); i++):
          if i != 1:
            placeholder = placeholder + ','
          placeholder = placeholder + '%s'
          
        values = ( )
        for key in table_layout:
          if key != '0':
            values.add(self.getItem(table_layout[key]))
        
        query = ("INSERT INTO " self.getTable() " " columns " VALUES " placeholder)
        try:
          cursor.execute( query, values )
        except mysql.connector.Error as err:
          noSqlErrors = False
        if noSqlErrors == True:
          if self.getBy(index_column, cursor.lastrowid) == True
            cnx.commit()
            success = True
        cursor.close()
        cnx.close()
    return success
    
  def deleteFromDatabase(self):
    ''' Deletes the object from the database '''
    ''' Test with test_SaveAndDeleteFromDatabase '''
    table_layout = getItem('table_layout')
    index_column = table_layout['0']   
    success = False
    noSqlErrors = True
    if self.getItem(index_column) != '':
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("DELETE FROM " self.getTable() " WHERE " index_column " = %s")
        try:
          cursor.execute(query, (self.getItem(index_column),))
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
    table_layout = getItem('table_layout')
    index_column = table_layout['0']
    success = False
    NoSqlErrors = True
    if self.getItem(index_column) != '':
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        
        placeholder = ''
        values = ( )
        for key in table_layout:
          if key != '0':
            if key != '1':
              placeholder = placeholder + ','
            placeholder = placeholder + table_layout[key] + " = %s"
            values.add(getItem(table_layout[key])
        
        query = ("UPDATE " self.getTable " SET " placeholder " WHERE " index_column " = %s")
        try:
          cursor.execute(query, values) 
        except mysql.connector.Error as err:
          NoSqlErrors = False
        if NoSqlErrors == True:
          cnx.commit()
          self.getBy(index_column, cursor.lastrowid)
          success = True
        cursor.close()
        cnx.close()
    return success
    
    def notDuplicate(self):
      pass
      