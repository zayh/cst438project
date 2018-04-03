import unittest
from Rating2 import Rating

class TestRating(unittest.TestCase):
  # Test data for the test cases below
  data1 = {
    'rating_id': '',
    'account_id': 3,
    'album_id': 2,
    'rating': 4,
    'date': '2018-03-02',
    'rating_id': '',
    'comment': 'I don\'t actually own this album',
  }

  data2 = {
    'account_id': 34, 
    'album_id': 2, 
    'rating': 4, 
    'comment': "I don't actually own this album", 
    'date': '2018-03-02'
  }
  
  data3 = {
    'account_id': 34, 
    'album_id': 2, 
    'rating': 1, 
    'comment': "I hate this album", 
    'date': '2017-03-02'
  }
  def test_createEmptyRating(self):
    # Create an empty object. Test to see that the object is of the right type and all
    # columns are empty
    object = Rating()
    self.assertIsInstance(object, Rating)
    self.assertEqual(object.getItem('rating_id'), '')
    self.assertEqual(object.getItem('account_id'), '')
    self.assertEqual(object.getItem('album_id'), '')
    self.assertEqual(object.getItem('rating'), '')
    self.assertEqual(object.getItem('comment'), '')
    self.assertEqual(object.getItem('date'), '')
    
  def test_new(self):
    # Test the non empty constructor
    object = Rating(self.data1)
    self.assertEqual(object.getItem('rating_id'), '')
    self.assertEqual(object.getItem('date'), '2018-03-02')
    self.assertEqual(object.getItem('account_id'), 3)
    self.assertEqual(object.getItem('album_id'), 2)
    self.assertEqual(object.getItem('rating'), 4)
    self.assertEqual(object.getItem('comment'), "I don't actually own this album")
    
  def test_JSON(self):
    # Outputs the object as a JSON String
    object1 = Rating(self.data1)
    jsonStr = object1.toJSON()
    # Then populates a new object with it
    object2 = Rating()
    self.assertEqual(object2.getItem('account_id'), '')
    self.assertEqual(object2.getItem('album_id'), '')
    self.assertEqual(object2.getItem('rating'), '')
    object2.fromJSON(jsonStr)
    self.assertEqual(object2.getItem('account_id'), 3)
    self.assertEqual(object2.getItem('album_id'), 2)
    self.assertEqual(object2.getItem('rating'), 4)    
    
    
  def test_mutators_and_accessors(self):
    # Check that mutators and accessors function
    # (These are inherited from the parent class now)
    object1 = Rating()
    self.assertTrue(object1.setItem('comment',"I don't actually own this album"))
    self.assertTrue(object1.setItem('date','2018-03-02'))
    self.assertTrue(object1.setItem('account_id',3))
    self.assertTrue(object1.setItem('album_id',2))
    self.assertTrue(object1.setItem('rating',4))
    
    self.assertEqual(object1.getItem('comment'), "I don't actually own this album")
    self.assertEqual(object1.getItem('date'), '2018-03-02')
    self.assertEqual(object1.getItem('account_id'), 3)
    self.assertEqual(object1.getItem('album_id'), 2)
    self.assertEqual(object1.getItem('rating'), 4)
    
  def test_getByRatingID(self):
    # getRow() populates the object by using the primary key
    object = Rating()
    self.assertTrue(object.getRow(4))
    self.assertNotEqual(object.getItem('rating_id'), '')
    #self.assertEqual(object.getItem('date'), '2018-3-31' )
    
  def test_SaveAndDeleteFromDatabase(self):
    object1 = Rating(self.data2)
    self.assertTrue(object1.addToDatabase())
    self.assertNotEqual(object1.getItem('rating_id'), '')
    rating_id = object1.getItem('rating_id')

    object2 = Rating()
    self.assertTrue(object2.getRow(rating_id))
    self.assertNotEqual(object2.getItem('rating_id'), '')
    self.assertTrue(object2.deleteFromDatabase())

    object3 = Rating()
    self.assertFalse(object3.getRow(rating_id))
    self.assertEqual(object3.getItem('rating_id'), '')
    
  def test_duplicateRatings(self):
    object1 = Rating(self.data2)
    self.assertTrue(object1.addToDatabase())
    self.assertNotEqual(object1.getItem('rating_id'), '')

    object2 = Rating(self.data3)
    self.assertFalse(object2.addToDatabase())
    self.assertEqual(object2.getItem('rating_id'), '')
    
    self.assertTrue(object1.deleteFromDatabase())

  def test_saveToDatabase(self):
    object1 = Rating()
    self.assertTrue(object1.getRow(4))
    self.assertEqual(object1.getItem('rating'), 5)
    self.assertTrue(object1.setItem('rating',1))
    self.assertTrue(object1.saveToDatabase())
    
    object2 = Rating()
    self.assertTrue(object2.getRow(4))
    self.assertEqual(object2.getItem('rating'), 1)
    self.assertTrue(object2.setItem('rating',5))
    self.assertTrue(object2.saveToDatabase())
    