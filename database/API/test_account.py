import unittest
from Account import Account

class TestAccount(unittest.TestCase):

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
    object = Account()
    self.assertIsInstance(object, Account)
    self.assertEqual(object.getAccountID(), '')
    self.assertEqual(object.getUsername(), '')
    self.assertEqual(object.getFirstname(), '')
    self.assertEqual(object.getLastname(), '')
    self.assertEqual(object.getLyric(), '')
    self.assertEqual(object.getPassword(), '')
    
  def test_populatedAccount(self):
    object = Account(self.data1)
    self.assertEqual(object.getAccountID(), '')
    self.assertEqual(object.getUsername(), 'bobdylan')
    self.assertEqual(object.getFirstname(), 'Bob')
    self.assertEqual(object.getLastname(), 'Dylan')
    self.assertEqual(object.getLyric(), 'kiss this guy')
    
  def testSetPassword(self):
    object = Account(self.data1)
    self.assertTrue(object.addPassword('wh4tD1D#eS47?'))
    self.assertTrue(object.checkPassword('wh4tD1D#eS47?'))
    self.assertFalse(object.checkPassword('wh4tD1D#eS47'))
    
  def test_toJSON(self):
    object = Account(self.data1)
    self.assertTrue(object.addPassword('wh4tD1D#eS47?'))
    self.assertEqual(object.toJSON(), '{"account_id": "", "username": "bobdylan", "firstname": "Bob", "lastname": "Dylan", "lyric": "kiss this guy", "password": "b3e79af50eedc2409663b385c4f194a23699834e4363508953996e195715dd2c"}')
    
  def test_mutators(self):
    object = Account()
    object.setUsername('mcarrey')
    object.setFirstname('Mariah')
    object.setLastname('Carrey')
    object.setLyric("what's my line?")
    object.addPassword("$$doGC4#,")
    
    self.assertEqual(object.getUsername(), 'mcarrey')
    self.assertEqual(object.getFirstname(), 'Mariah')
    self.assertEqual(object.getLastname(), 'Carrey')
    self.assertEqual(object.getLyric(), "what's my line?")
    self.assertEqual(object.getPassword(), '1b4257b066734e33fb4bff2290025237ee187a52b4e335970a2a13054259946b')
    
  def test_getByUsername(self):
    object = Account()
    self.assertTrue(object.getBy('username','jay'))
    self.assertNotEqual(object.getAccountID(), '')
    self.assertEqual(object.getAccountID(), 3)
    
  def test_getByAccountID(self):
    object = Account()
    self.assertTrue(object.getBy('account_id', 3))
    self.assertNotEqual(object.getAccountID(), '')
    self.assertEqual(object.getUsername(), 'jay')
    
  def test_getByError(self):
    object = Account()
    self.assertFalse(object.getBy('firstname', 'Jason'))
    self.assertEqual(object.getAccountID(), '')
    
  def test_SaveAndDeleteFromDatabase(self):
    object1 = Account(self.data1)
    self.assertFalse(object1.addToDatabase())
    self.assertTrue(object1.addPassword('wh4tD1D#eS47'))
    self.assertTrue(object1.addToDatabase())

    object2 = Account()
    self.assertTrue(object2.getBy('username', 'bobdylan'))
    self.assertNotEqual(object2.getAccountID, '')
    self.assertTrue(object2.deleteFromDatabase())

    object3 = Account()
    self.assertFalse(object3.getBy('username', 'bobdylan'))
    self.assertEqual(object3.getAccountID(), '')
    
  def test_isUsernameAvailable(self):
    object1 = Account(self.data1)
    object2 = Account(self.data2)
    self.assertTrue(object1.isUsernameAvailable())
    self.assertFalse(object2.isUsernameAvailable())
    
  def test_saveToDatabase(self):
    object = Account()
    self.assertTrue(object.getBy('account_id', 3))
    self.assertEqual(object.getLyric(), 'pour some sugar on me')
    self.assertTrue(object.setLyric('we are the champions'))
    self.assertTrue(object.saveToDatabase())
    self.assertEqual(object.getLyric(), 'we are the champions')
    self.assertTrue(object.setLyric('pour some sugar on me'))
    self.assertTrue(object.saveToDatabase())
    self.assertEqual(object.getLyric(), 'pour some sugar on me')

    