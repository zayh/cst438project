import unittest
from Favorite import Favorite

class TestFavorite(unittest.TestCase):

  def test_createEmptyFavorite(self):
    object = Favorite()
    self.assertIsInstance(object, Favorite)
    self.assertEqual(object.getFavoriteID(), '')
    self.assertEqual(object.getAccountID(), '')
    self.assertEqual(object.getAlbumID(), '')
    
  def test_new(self):
    object = Favorite()
    object.new(3, 2);
    self.assertEqual(object.getFavoriteID(), '')
    self.assertEqual(object.getAccountID(), 3)
    self.assertEqual(object.getAlbumID(), 2)
    
  def test_toJSON(self):
    object = Favorite()
    object.new(3, 2)
    self.assertEqual(object.toJSON(), 
      "{ favorite_id: , account_id: 3, album_id: 2 }" 
    )
    
  def test_mutators_and_accessors(self):
    object1 = Favorite()
    self.assertTrue(object1.setAccountID(3))
    self.assertTrue(object1.setAlbumID(2))
    self.assertEqual(object1.getAccountID(), 3)
    self.assertEqual(object1.getAlbumID(), 2)
    
  def test_getByFavoriteID(self):
    object = Favorite()
    self.assertTrue(object.getBy('favorite_id', 1))
    self.assertNotEqual(object.getFavoriteID(), '')
    self.assertEqual(object.getAccountID(), 3)
    self.assertEqual(object.getAlbumID(), 2)
    
  def test_getByError(self):
    object = Favorite()
    self.assertFalse(object.getBy('account_id', 3))
    self.assertEqual(object.getFavoriteID(), '')
    
  def test_SaveAndDeleteFromDatabase(self):
    object1 = Favorite()
    self.assertTrue(object1.new(34, 2))
    self.assertTrue(object1.addToDatabase())
    self.assertNotEqual(object1.getFavoriteID(), '')
    favorite_id = object1.getFavoriteID()

    object2 = Favorite()
    self.assertTrue(object2.getBy('favorite_id', favorite_id))
    self.assertNotEqual(object2.getFavoriteID(), '')
    self.assertTrue(object2.deleteFromDatabase())

    object3 = Favorite()
    self.assertFalse(object3.getBy('favorite_id', favorite_id))
    self.assertEqual(object3.getFavoriteID(), '')
    
  def test_duplicateFavorites(self):
    object1 = Favorite()
    self.assertTrue(object1.new(34, 2))
    self.assertTrue(object1.addToDatabase())
    self.assertNotEqual(object1.getFavoriteID(), '')

    object2 = Favorite()
    self.assertTrue(object1.new(34, 2))
    self.assertFalse(object2.addToDatabase())
    self.assertEqual(object2.getFavoriteID(), '')
    
    self.assertTrue(object1.deleteFromDatabase())

    