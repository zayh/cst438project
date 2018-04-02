import unittest
from Favorite import Favorite

class TestFavorite(unittest.TestCase):

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
    object = Favorite()
    self.assertIsInstance(object, Favorite)
    self.assertEqual(object.getItem('favorite_id'), '')
    self.assertEqual(object.getItem('account_id'), '')
    self.assertEqual(object.getItem('album_id'), '')
    
  def test_new(self):
    object = Favorite(self.data1);
    self.assertEqual(object.getItem('favorite_id'), '')
    self.assertEqual(object.getItem('account_id'), 3)
    self.assertEqual(object.getItem('album_id'), 2)
    
  def test_JSON(self):
    object1 = Favorite(self.data1)
    jsonStr = object1.toJSON()
    
    object2 = Favorite()
    self.assertEqual(object2.getItem('account_id'), '')
    self.assertEqual(object2.getItem('album_id'), '')
    
    object2.fromJSON(jsonStr)
    self.assertEqual(object2.getItem('account_id'), 3)
    self.assertEqual(object2.getItem('album_id'), 2)  
    
  def test_mutators_and_accessors(self):
    object1 = Favorite()
    self.assertTrue(object1.setItem('account_id',3))
    self.assertTrue(object1.setItem('album_id',2))
    self.assertEqual(object1.getItem('account_id'), 3)
    self.assertEqual(object1.getItem('album_id'), 2)
    
  def test_getByFavoriteID(self):
    object = Favorite()
    self.assertTrue(object.getRow(1))
    self.assertNotEqual(object.getItem('favorite_id'), '')
    self.assertEqual(object.getItem('account_id'), 3)
    self.assertEqual(object.getItem('album_id'), 2)
    
  def test_getByError(self):
    object = Favorite()
    self.assertFalse(object.getRow(3))
    self.assertEqual(object.getItem('favorite_id'), '')
    
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
       
    
    