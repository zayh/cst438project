import unittest
from Rating import Rating

class TestRating(unittest.TestCase):

  def test_createEmptyRating(self):
    object = Rating()
    self.assertIsInstance(object, Rating)
    self.assertEqual(object.getRatingID(), '')
    self.assertEqual(object.getAccountID(), '')
    self.assertEqual(object.getAlbumID(), '')
    self.assertEqual(object.getRating(), '')
    self.assertEqual(object.getComment(), '')
    self.assertEqual(object.getDate(), '')
    
    
  def test_new(self):
    object = Rating()
    object.new(3, 2, 4, "I don't actually own this album", '2018-03-02')
    self.assertEqual(object.getRatingID(), '')
    self.assertEqual(object.getDate(), '2018-03-02')
    self.assertEqual(object.getAccountID(), 3)
    self.assertEqual(object.getAlbumID(), 2)
    self.assertEqual(object.getRating(), 4)
    self.assertEqual(object.getComment(), "I don't actually own this album")
    
  def test_toJSON(self):
    object = Rating()
    object.new(3, 2, 4, "I don't actually own this album", '2018-03-02')
    self.assertEqual(object.toJSON(), 
      "{ rating_id: , account_id: 3, album_id: 2, rating: 4, comment: 'I don\'t actually own this album', "
      "date: '2018-03-02' }" 
    )
    
  def test_mutators_and_accessors(self):
    object1 = Rating()
    self.assertTrue(object1.setComment("I don't actually own this album"))
    self.assertTrue(object1.setDate('2018-03-02'))
    self.assertTrue(object1.setAccountID(3))
    self.assertTrue(object1.setAlbumID(2))
    self.assertTrue(object1.setRating(4))
    
    self.assertEqual(object1.getComment(), "I don't actually own this album")
    self.assertEqual(object1.getDate(), '2018-03-02')
    self.assertEqual(object1.getAccountID(), 3)
    self.assertEqual(object1.getAlbumID(), 2)
    self.assertEqual(object1.getRating(), 4)
    
  def test_getByRatingID(self):
    object = Rating()
    self.assertTrue(object.getBy('rating_id', 4))
    self.assertNotEqual(object.getRatingID(), '')
#    self.assertEqual(object.getDate(), '2018-03-31')
    
  def test_getByError(self):
    object = Rating()
    self.assertFalse(object.getBy('account_id', '2'))
    self.assertEqual(object.getRatingID(), '')
    
  def test_SaveAndDeleteFromDatabase(self):
    object1 = Rating()
    self.assertTrue(object1.new(34, 2, 4, "I don't actually own this album", '2018-03-02'))
    self.assertTrue(object1.addToDatabase())
    self.assertNotEqual(object1.getRatingID(), '')
    rating_id = object1.getRatingID()

    object2 = Rating()
    self.assertTrue(object2.getBy('rating_id', rating_id))
    self.assertNotEqual(object2.getRatingID(), '')
    self.assertTrue(object2.deleteFromDatabase())

    object3 = Rating()
    self.assertFalse(object3.getBy('rating_id', rating_id))
    self.assertEqual(object3.getRatingID(), '')
    
  def test_duplicateRatings(self):
    object1 = Rating()
    self.assertTrue(object1.new(34, 2, 4, "I don't actually own this album", '2018-03-02'))
    self.assertTrue(object1.addToDatabase())
    self.assertNotEqual(object1.getRatingID(), '')

    object2 = Rating()
    self.assertTrue(object1.new(34, 2, 1, "I hate this album", '2017-03-02'))
    self.assertFalse(object2.addToDatabase())
    self.assertEqual(object2.getRatingID(), '')
    
    self.assertTrue(object1.deleteFromDatabase())

  def test_saveToDatabase(self):
    object1 = Rating()
    self.assertTrue(object1.getBy('rating_id', 4))
    self.assertEqual(object1.getRating(), 5)
    self.assertTrue(object1.setRating(1))
    self.assertTrue(object1.saveToDatabase())
    
    object2 = Rating()
    self.assertTrue(object2.getBy('rating_id', 4))
    self.assertEqual(object2.getRating(), 1)
    self.assertTrue(object2.setRating(5))
    self.assertTrue(object2.saveToDatabase())
    