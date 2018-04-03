import unittest
from Favorite import Favorite

class TestFavorite(unittest.TestCase):
  # Test data for the test cases below
  data1 = {
    'favorite_id' : '',
    'account_id' : 3,
    'album_id' : 2,
  }
  
  data2 = {
    'favorite_id' : '',
    'account_id' : 34,
    'album_id' : 2,
  }

  def test_createEmptyFavorite(self):
    # Create an empty object. Test to see that the object is of the right type and all
    # columns are empty
    object = Favorite()
    self.assertIsInstance(object, Favorite)
    self.assertEqual(object.getItem('favorite_id'), '')
    self.assertEqual(object.getItem('account_id'), '')
    self.assertEqual(object.getItem('album_id'), '')
    
  def test_new(self):
    # Test the non empty constructor 
    object = Favorite(self.data1);
    self.assertEqual(object.getItem('favorite_id'), '')
    self.assertEqual(object.getItem('account_id'), 3)
    self.assertEqual(object.getItem('album_id'), 2)
    
  def test_JSON(self):
    # Outputs the object as a JSON String
    object1 = Favorite(self.data1)
    jsonStr = object1.toJSON()
    
    object2 = Favorite()
    self.assertEqual(object2.getItem('account_id'), '')
    self.assertEqual(object2.getItem('album_id'), '')
    # Then populates a new object with it
    object2.fromJSON(jsonStr)
    self.assertEqual(object2.getItem('account_id'), 3)
    self.assertEqual(object2.getItem('album_id'), 2)  
    
  def test_mutators_and_accessors(self):
    # Check that mutators and accessors function
    # (These are inherited from the parent class now)
    object1 = Favorite()
    self.assertTrue(object1.setItem('account_id',3))
    self.assertTrue(object1.setItem('album_id',2))
    self.assertEqual(object1.getItem('account_id'), 3)
    self.assertEqual(object1.getItem('album_id'), 2)
    
  def test_getByFavoriteID(self):
    # getRow() populates the object by using the primary key
    object = Favorite()
    self.assertTrue(object.getRow(1))
    self.assertNotEqual(object.getItem('favorite_id'), '')
    self.assertEqual(object.getItem('account_id'), 3)
    self.assertEqual(object.getItem('album_id'), 2)
    
  def test_SaveAndDeleteFromDatabase(self):
    object1 = Favorite(self.data2)
    self.assertTrue(object1.addToDatabase())
    self.assertNotEqual(object1.getItem('favorite_id'), '')
    favorite_id = object1.getItem('favorite_id')

    object2 = Favorite()
    self.assertTrue(object2.getRow(favorite_id))
    self.assertNotEqual(object2.getItem('favorite_id'), '')
    self.assertTrue(object2.deleteFromDatabase())

    object3 = Favorite()
    self.assertFalse(object3.getRow(favorite_id))
    self.assertEqual(object3.getItem('favorite_id'), '')
    
  def test_duplicateFavorites(self):
    object1 = Favorite(self.data2)
    self.assertTrue(object1.addToDatabase())
    self.assertNotEqual(object1.getItem('favorite_id'), '')

    object2 = Favorite(self.data2)
    self.assertFalse(object2.addToDatabase())
    self.assertEqual(object2.getItem('favorite_id'), '')
    
    self.assertTrue(object1.deleteFromDatabase())

  def test_saveToDatabase(self):
    object1 = Favorite()
    self.assertTrue(object1.getRow(1))
    self.assertEqual(object1.getItem('album_id'), 2)
    self.assertTrue(object1.setItem('album_id',48))
    self.assertTrue(object1.saveToDatabase())
    
    object2 = Favorite()
    self.assertTrue(object2.getRow(1))
    self.assertEqual(object2.getItem('album_id'), 48)
    self.assertTrue(object2.setItem('album_id',2))
    self.assertTrue(object2.saveToDatabase())
       
    
    