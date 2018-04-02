import mysql.connector

SQL_USER = 'webapp'
SQL_PASS = 'centralSolutions123'
SQL_HOST = '18.222.66.236'
SQL_DATA = 'musicproject'

def connectToDatabase():
  ''' Connect to the Database '''
  try:
    cnx = mysql.connector.connect(
      user=SQL_USER, 
      password=SQL_PASS,
      host=SQL_HOST, 
      database=SQL_DATA
    )
  except mysql.connector.Error as err:
    cnx = False
  
  return cnx
