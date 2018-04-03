import unittest
from Account import Account

class TestAccount(unittest.TestCase):
  # Test data for the test cases below
  data1 = {
    'account_id' : '',
    'username'  : 'bobdylan',
    'firstname' : 'Bob',
    'lastname'  : 'Dylan',
    'lyric'     : 'kiss this guy'
  }
  
  data2 = {
    'username'   : 'jay'
  }

  def test_createEmptyAccout(self):
    # Create an empty object. Test to see that the object is of the right type and all
    # columns are empty
    object = Account()
    self.assertIsInstance(object, Account)
    self.assertEqual(object.getItem('account_id'), '')
    self.assertEqual(object.getItem('username'), '')
    self.assertEqual(object.getItem('firstname'), '')
    self.assertEqual(object.getItem('lastname'), '')
    self.assertEqual(object.getItem('lyric'), '')
    self.assertEqual(object.getItem('password'), '')
    
  def test_populatedAccount(self):
    # Test the non empty constructor
    object = Account(self.data1)
    self.assertEqual(object.getItem('account_id'), '')
    self.assertEqual(object.getItem('username'), 'bobdylan')
    self.assertEqual(object.getItem('firstname'), 'Bob')
    self.assertEqual(object.getItem('lastname'), 'Dylan')
    self.assertEqual(object.getItem('lyric'), 'kiss this guy')
    
  def testSetPassword(self):
    # Test the password functions by adding a password then checking it.
    object = Account(self.data1)
    self.assertTrue(object.addPassword('wh4tD1D#eS47?'))
    self.assertTrue(object.checkPassword('wh4tD1D#eS47?'))
    # Wrong password! should be False!!
    self.assertFalse(object.checkPassword('wh4tD1D#eS47'))
    
  def test_JSON(self):
    # Outputs the object as a JSON String
    object1 = Account(self.data1)
    jsonStr = object1.toJSON()
    # Then populates a new object with it
    object2 = Account()
    self.assertEqual(object2.getItem('username'), '')
    self.assertEqual(object2.getItem('firstname'), '')
    self.assertEqual(object2.getItem('lastname'), '')
    self.assertEqual(object2.getItem('lyric'), '')
    object2.fromJSON(jsonStr)
    self.assertEqual(object2.getItem('username'), 'bobdylan')
    self.assertEqual(object2.getItem('firstname'), 'Bob')
    self.assertEqual(object2.getItem('lastname'), 'Dylan')
    self.assertEqual(object2.getItem('lyric'), 'kiss this guy')   
    
  def test_mutators(self):
    # Check that mutators and accessors function
    # (These are inherited from the parent class now)
    object = Account()
    object.setItem('username','mcarrey')
    object.setItem('firstname','Mariah')
    object.setItem('lastname','Carrey')
    object.setItem('lyric',"what's my line?")
    object.addPassword("$$doGC4#,")
    
    self.assertEqual(object.getItem('username'), 'mcarrey')
    self.assertEqual(object.getItem('firstname'), 'Mariah')
    self.assertEqual(object.getItem('lastname'), 'Carrey')
    self.assertEqual(object.getItem('lyric'), "what's my line?")
    self.assertEqual(object.getItem('password'), '1b4257b066734e33fb4bff2290025237ee187a52b4e335970a2a13054259946b')
    
  def test_getRow(self):
    # getRow() populates the object by using the primary key
    object = Account()
    self.assertTrue(object.getRow(3))
    self.assertNotEqual(object.getItem('account_id'), '')
    self.assertEqual(object.getItem('username'), 'jay')
    
  def test_SaveAndDeleteFromDatabase(self):
    object1 = Account(self.data1)
    self.assertTrue(object1.addPassword('wh4tD1D#eS47'))
    self.assertTrue(object1.addToDatabase())
    account_id = object1.getItem('account_id')

    object2 = Account()
    self.assertTrue(object2.getRow(account_id))
    self.assertEqual(object2.getItem('username'), 'bobdylan')
    self.assertTrue(object2.deleteFromDatabase())

    object3 = Account()
    self.assertFalse(object3.getRow(account_id))
    self.assertEqual(object3.getItem('account_id'), '')
    
  def test_isUsernameAvailable(self):
    object1 = Account(self.data1)
    object2 = Account(self.data2)
    self.assertTrue(object1.notDuplicate())
    self.assertFalse(object2.notDuplicate())
    
  def test_saveToDatabase(self):
    object = Account()
    self.assertTrue(object.getRow(3))
    self.assertEqual(object.getItem('lyric'), 'pour some sugar on me')
    self.assertTrue(object.setItem('lyric','we are the champions'))
    self.assertTrue(object.saveToDatabase())
    self.assertEqual(object.getItem('lyric'), 'we are the champions')
    self.assertTrue(object.setItem('lyric','pour some sugar on me'))
    self.assertTrue(object.saveToDatabase())
    self.assertEqual(object.getItem('lyric'), 'pour some sugar on me')

    