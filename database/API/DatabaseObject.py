from settings import *
import json

class DatabaseObject:

  def __init__(self, data=None):
    ''' Create an empty object '''
    ''' If passed an non empty dict, populate self.data '''
    self.data = {}
    if data is not None:
      for key in data:
        self.data[key] = data[key]  
        
  def toJSON(self):
    ''' Returns a JSON string of the object. '''
    ''' Test with test_JSON '''
    jsonStr = json.dumps(self.data)
    return jsonStr
  
  def fromJSON(self, jsonStr):
    ''' Takes a JSON string and populates self.data '''
    ''' Test with test_JSON '''
    if jsonStr != '':
      data = json.loads(jsonStr)
      self.__init__(data)
      
  def getTable(self):
    ''' Return the name of the table '''
    returnVal = ''
    if 'table_name' in self.data:
      returnVal = self.data['table_name']
    return returnVal
      
  def getItem(self, column):
    ''' Accessor for most data '''
    returnVal = ''
    if column in self.data:
      returnVal = self.data[column]
    return returnVal

  def setItem(self, column, value):
    ''' Mutator for most data '''
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
    select_columns = '' # Will be set to all columns
    success = False     # Return Value at the end
    noSqlErrors = True  # Keeps track of any SQL errors
    table_name = self.getTable() # Name of the table
    table_layout = self.data['table_layout'] # Dict of the table_layout
    table_index = table_layout['0'] # The first column is the primary key
    # Connect to Database. Imported from settings.py
    cnx = connectToDatabase()
    # Don't proceed if the connection failed
    if cnx != False:
      cursor = cnx.cursor(buffered=True)
      # Use table_layout to make the list of columns
      for key in table_layout:
        # if this isn't the first column, add a comma to each column
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
      # Only 1 row should be returned as well
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
    success = False # Return Value for the end of the method
    noSqlErrors = True # Keep track of any SQL errors
    table_name = self.getTable() # Store the name of the table
    table_layout = self.getItem('table_layout') # The layout is needed
    index_column = table_layout['0'] # First column is the primary key
    # Proceed if index_column is empty and this is not a duplicate
    if self.getItem(index_column) == '' and self.notDuplicate() == True:
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        # Building the columns here for the query statement
        columns = '('
        for key in table_layout:
          if key != '0':
            if key !='1':
              columns = columns + ','
            columns = columns + table_layout[key]
        columns = columns + ')'
        # Now the appropriate %s entries are created
        placeholder = '('
        for i in range (1, len(table_layout)):
          if i != 1:
            placeholder = placeholder + ','
          placeholder = placeholder + '%s'
        placeholder += ')'
        # The values to be inserted must be in a tuple. 
        # A list is built, then converted into a tuple.
        valueList = [ ]
        for key in table_layout:
          if key != '0':
            valueList.append(self.getItem(table_layout[key]))
        values = tuple(valueList)
        # table_name, columns, and placeholder are inserted into query
        query = ("INSERT INTO {} {} VALUES {}".format(table_name, columns, placeholder))
        # Try to update the database
        try:
          cursor.execute( query, values )
        # Catch any mysql errors
        except mysql.connector.Error as err:
          noSqlErrors = False
        # Proceed if we are clear
        if noSqlErrors == True:
          cnx.commit()
          # Now that the object is in the database, populate the object 
          if self.getRow(cursor.lastrowid) == True:
            success = True
        cursor.close()
        cnx.close()
    return success
    
  def deleteFromDatabase(self):
    ''' Deletes the object from the database '''
    ''' Test with test_SaveAndDeleteFromDatabase '''
    # To delete from the database, we must build the SQL command
    table_name = self.getTable() 
    table_layout = self.getItem('table_layout')
    index_column = table_layout['0'] # The primary key 
    success = False # Return Value for the end fo the method 
    noSqlErrors = True # Keep track of any SQL errors
    # We can only delete something if we have a ID for it
    if self.getItem(index_column) != '':
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        # use table_name and the primary key to build the query
        query = ("DELETE FROM {} WHERE {} = %s".format(table_name,index_column))
        # Execute the delete
        try:
          cursor.execute(query, (self.getItem(index_column),))
        except mysql.connector.Error as err:
          noSqlErrors = False
        # If we didn't error, clean up and report success
        if noSqlErrors == True:
          cnx.commit()
          success = True
        cursor.close()
        cnx.close()
    return success
    
  def saveToDatabase(self):
    ''' Saves current object to the database, using the primary index '''
    # To update the database, we must build a tuple to pass to the SQL cursor
    table_name = self.getTable() # Store the table name
    table_layout = self.getItem('table_layout') # Need the column names
    index_column = table_layout['0'] # primary key is here
    success = False # Return value for the end of the fuction
    NoSqlErrors = True # Keep track of SQL errors
    # Can't update unless we have a primary key value
    if self.getItem(index_column) != '':
      cnx = connectToDatabase()
      if cnx != False:
        cursor = cnx.cursor()
        
        placeholder = '' # Initialize the 'column = %s' string
        valueList = [ ] # the Values we are setting
        # Step through each column in the object, and map the values
        for key in table_layout:
          if key != '0':
            if key != '1':
              placeholder += ','
            placeholder += table_layout[key] + " = %s"
            valueList.append(self.getItem(table_layout[key]))
        valueList.append(self.getItem(index_column))
        # Convert valueList to a tuple
        values = tuple(valueList)
        query = ("UPDATE {} SET {} WHERE {} = %s".format(table_name, placeholder, index_column))
        # Execute the update
        try:
          cursor.execute(query, values) 
        # Catch any errors
        except mysql.connector.Error as err:
          NoSqlErrors = False
        # If no error, commit the change and report success = True
        if NoSqlErrors == True:
          cnx.commit()
          success = True
        cursor.close()
        cnx.close()
    return success
    
  def notDuplicate(self):
    ''' Checks to see if object contains data in columns that cannot be duplicated '''
    ''' Test with test_notDuplicate '''
    available = False
    noSqlErrors = True
    table_name = self.getTable()
    table_layout = self.getItem('table_layout')
    # Each class defines column combos that cannot be duplicated
    combos = self.getItem('unique_combos')
    
    cnx = connectToDatabase()
    if cnx != False:
      cursor = cnx.cursor(buffered=True)
      # query and values must be created to pass to execute.
      # query is a string and values must be a tuple
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
      # If we don't get any errors and MYSQL doesn't report any matches
      # we do not have a duplicate, and report available = True
      if noSqlErrors == True and cursor.rowcount == 0:
        available = True
      cursor.close()
      cnx.close()
    return available
    
