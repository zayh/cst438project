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
    self.assertEqual(object.getWishlistID(), '')
    self.assertEqual(object.getAccountID(), '')
    self.assertEqual(object.getAlbumID(), '')
    
  def test_new(self):
    object = Wishlist(self.data1);
    self.assertEqual(object.getWishlistID(), '')
    self.assertEqual(object.getAccountID(), 1)
    self.assertEqual(object.getAlbumID(), 2)
    
  def test_toJSON(self):
    object = Wishlist(self.data1)
    self.assertEqual(object.toJSON(), 
      '{"wishlist_id": "", "account_id": 1, "album_id": 2}' 
    )
    
  def test_mutators_and_accessors(self):
    object1 = Wishlist()
    self.assertTrue(object1.setAccountID(1))
    self.assertTrue(object1.setAlbumID(2))
    self.assertEqual(object1.getAccountID(), 1)
    self.assertEqual(object1.getAlbumID(), 2)
    
  def test_getByWishlistID(self):
    object = Wishlist()
    self.assertTrue(object.getBy('wishlist_id', 1))
    self.assertNotEqual(object.getWishlistID(), '')
    self.assertEqual(object.getAccountID(), 3)
    self.assertEqual(object.getAlbumID(), 2)

    
  def test_getByError(self):
    object = Wishlist()
    self.assertFalse(object.getBy('account_id', 3))
    self.assertEqual(object.getWishlistID(), '')
    
  def test_SaveAndDeleteFromDatabase(self):
    object1 = Wishlist(self.data2)
    self.assertTrue(object1.addToDatabase())
    self.assertNotEqual(object1.getWishlistID(), '')
    wishlist_id = object1.getWishlistID()

    object2 = Wishlist()
    self.assertTrue(object2.getBy('wishlist_id', wishlist_id))
    self.assertNotEqual(object2.getWishlistID(), '')
    self.assertTrue(object2.deleteFromDatabase())

    object3 = Wishlist()
    self.assertFalse(object3.getBy('wishlist_id', wishlist_id))
    self.assertEqual(object3.getWishlistID(), '')
    
  def test_duplicateWishlists(self):
    object1 = Wishlist(self.data2)
    self.assertTrue(object1.addToDatabase())
    self.assertNotEqual(object1.getWishlistID(), '')

    object2 = Wishlist(self.data2)
    self.assertFalse(object2.addToDatabase())
    self.assertEqual(object2.getWishlistID(), '')
    
    self.assertTrue(object1.deleteFromDatabase())

  def test_saveToDatabase(self):
    object1 = Wishlist()
    self.assertTrue(object1.getBy('wishlist_id', 1))
    self.assertEqual(object1.getAlbumID(), 2)
    self.assertTrue(object1.setAlbumID(48))
    self.assertTrue(object1.saveToDatabase())
    
    object2 = Wishlist()
    self.assertTrue(object2.getBy('wishlist_id', 1))
    self.assertEqual(object2.getAlbumID(), 48)
    self.assertTrue(object2.setAlbumID(2))
    self.assertTrue(object2.saveToDatabase())
       
    