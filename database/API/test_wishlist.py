import unittest
from Wishlist import Wishlist

class TestWishlist(unittest.TestCase):

  data1 = {
    'wishlist_id' : '',
    'account_id': 1,
    'album_id': 2,
  }
  
  data2 = {
    'account_id': 34,
    'album_id' : 2
  }

  def test_createEmptyWishlist(self):
    object = Wishlist()
    self.assertIsInstance(object, Wishlist)
    self.assertEqual(object.getItem('wishlist_id'), '')
    self.assertEqual(object.getItem('account_id'), '')
    self.assertEqual(object.getItem('album_id'), '')
    
  def test_new(self):
    object = Wishlist(self.data1);
    self.assertEqual(object.getItem('wishlist_id'), '')
    self.assertEqual(object.getItem('account_id'), 1)
    self.assertEqual(object.getItem('album_id'), 2)
    
  def test_toJSON(self):
    object1 = Wishlist(self.data1)
    jsonStr = object1.toJSON()
    
    object2 = Wishlist()
    self.assertEqual(object2.getItem('account_id'), '')
    self.assertEqual(object2.getItem('album_id'), '')
    object2.fromJSON(jsonStr)
    self.assertEqual(object2.getItem('account_id'), 1)
    self.assertEqual(object2.getItem('album_id'), 2)
    
  def test_mutators_and_accessors(self):
    object1 = Wishlist()
    self.assertTrue(object1.setItem('account_id',1))
    self.assertTrue(object1.setItem('album_id',2))
    self.assertEqual(object1.getItem('account_id'), 1)
    self.assertEqual(object1.getItem('album_id'), 2)
    
  def test_getRow(self):
    object = Wishlist()
    self.assertTrue(object.getRow(1))
    self.assertNotEqual(object.getItem('wishlist_id'), '')
    self.assertEqual(object.getItem('account_id'), 3)
    self.assertEqual(object.getItem('album_id'), 2)

    
  def test_SaveAndDeleteFromDatabase(self):
    object1 = Wishlist(self.data2)
    self.assertTrue(object1.addToDatabase())
    self.assertNotEqual(object1.getItem('wishlist_id'), '')
    wishlist_id = object1.getItem('wishlist_id')

    object2 = Wishlist()
    self.assertTrue(object2.getRow(wishlist_id))
    self.assertNotEqual(object2.getItem('wishlist_id'), '')
    self.assertTrue(object2.deleteFromDatabase())

    object3 = Wishlist()
    self.assertFalse(object3.getRow(wishlist_id))
    self.assertEqual(object3.getItem('wishlist_id'), '')
    
  def test_duplicateWishlists(self):
    object1 = Wishlist(self.data2)
    self.assertTrue(object1.addToDatabase())
    self.assertNotEqual(object1.getItem('wishlist_id'), '')

    object2 = Wishlist(self.data2)
    self.assertFalse(object2.addToDatabase())
    self.assertEqual(object2.getItem('wishlist_id'), '')
    
    self.assertTrue(object1.deleteFromDatabase())

  def test_saveToDatabase(self):
    object1 = Wishlist()
    self.assertTrue(object1.getRow(1))
    self.assertEqual(object1.getItem('album_id'), 2)
    self.assertTrue(object1.setItem('album_id',48))
    self.assertTrue(object1.saveToDatabase())
    
    object2 = Wishlist()
    self.assertTrue(object2.getRow(1))
    self.assertEqual(object2.getItem('album_id'), 48)
    self.assertTrue(object2.setItem('album_id',2))
    self.assertTrue(object2.saveToDatabase())
       
    