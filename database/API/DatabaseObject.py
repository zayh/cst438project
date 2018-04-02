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
      success = True
    return success
    
  def getRow(self, value):
    ''' 
    Populate the object from the database 
    Test with test_getRow  
    '''
    # Initialize local variables
    select_columns = ''
    success = False
    noSqlErrors = True
    table_name = self.getTable()
    table_layout = self.data['table_layout']
    table_index = table_layout['0']
    
    cnx = connectToDatabase()
    # Don't proceed if the connection failed
    if cnx != False:
      cursor = cnx.cursor(buffered=True)
      # Use table_layout to make the list of columns
      for key in table_layout:
        # if this isn't the first column, add a comma to the end
        if key != '0':
          select_columns += ','
        select_columns += table_layout[key]
      # Now the query can be built
      query = ("SELECT {} FROM {} WHERE {} = %s".format(select_columns, table_name, table_index))
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
          self.setItem(table_layout[key], row[int(key)])
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
    table_layout = self.getItem('table_layout')
    index_column = table_layout['0']
    
    if self.getItem(index_column) == '' and self.notDuplicate() == True:
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()

        columns = '('
        for key in table_layout:
          if key != '0':
            if key !='1':
              columns = columns + ','
            columns = columns + table_layout[key]
        columns = columns + ')'
        placeholder = '('
        for i in range (1, len(table_layout)):
          if i != 1:
            placeholder = placeholder + ','
          placeholder = placeholder + '%s'
        placeholder += ')'
        
        valueList = [ ]
        for key in table_layout:
          if key != '0':
            valueList.append(self.getItem(table_layout[key]))
        values = tuple(valueList)
        
        query = ("INSERT INTO {} {} VALUES {}".format(self.getTable(), columns, placeholder))

        try:
          cursor.execute( query, values )
        except mysql.connector.Error as err:
          noSqlErrors = False
        if noSqlErrors == True:
          cnx.commit()
          if self.getRow(cursor.lastrowid) == True:
            success = True
        cursor.close()
        cnx.close()
    return success
    
  def deleteFromDatabase(self):
    ''' Deletes the object from the database '''
    ''' Test with test_SaveAndDeleteFromDatabase '''
    table_layout = self.getItem('table_layout')
    index_column = table_layout['0']   
    success = False
    noSqlErrors = True
    if self.getItem(index_column) != '':
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        query = ("DELETE FROM {} WHERE {} = %s".format(self.getTable(),index_column))
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
    table_layout = self.getItem('table_layout')
    index_column = table_layout['0']
    success = False
    NoSqlErrors = True
    if self.getItem(index_column) != '':
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        
        placeholder = ''
        valueList = [ ]
        for key in table_layout:
          if key != '0':
            if key != '1':
              placeholder += ','
            placeholder += table_layout[key] + " = %s"
            valueList.append(self.getItem(table_layout[key]))
        valueList.append(self.getItem(index_column))
        values = tuple(valueList)
        query = ("UPDATE {} SET {} WHERE {} = %s".format(self.getTable(), placeholder, index_column))
        try:
          cursor.execute(query, values) 
        except mysql.connector.Error as err:
          NoSqlErrors = False
        if NoSqlErrors == True:
          cnx.commit()
          self.getRow(cursor.lastrowid)
          success = True
        cursor.close()
        cnx.close()
    return success
    
  def notDuplicate(self):
    ''' Checks to see if the given songname is already in use '''
    ''' Test with test_notDuplicate '''
    available = False
    noSqlErrors = True
    table_name = self.getTable()
    table_layout = self.getItem('table_layout')
    combos = self.getItem('unique_combos')
    
    cnx = connectToDatabase()
    if cnx != False:
      cursor = cnx.cursor(buffered=True)
      
      query = "SELECT * FROM " + table_name + " WHERE "
      query += combos[0] + " = %s"
      valueList = [ self.getItem(combos[0]) ]
      
      for i in range( 1, len(combos) ):
        query += " AND " + combos[i] + " = %s"
        valueList.append( self.getItem(combos[i]) )
      values = tuple(valueList)
      try:
        cursor.execute(query, values)
      except mysql.connector.Error as err:
        noSqlErrors = False
      if noSqlErrors == True and cursor.rowcount == 0:
        available = True
      cursor.close()
      cnx.close()
    return available
    
