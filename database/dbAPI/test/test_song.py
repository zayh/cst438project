import unittest
from ..Tables import Song

class TestSong(unittest.TestCase):

  data1 = {
    'song_id' : '',
    'song_name' : 'Enter Sandman',
    'is_solo_release' : 0,
    'band_id' : 1,
  }
  
  data2 = {
    'song_name' : 'Sad But True',
    'band_id' : 1
  }

  def test_createEmptySong(self):
    object = Song()
    self.assertIsInstance(object, Song)
    self.assertEqual(object.getItem('song_id'), '')
    self.assertEqual(object.getItem('song_name'), '')
    self.assertEqual(object.getItem('band_id'), '')
    self.assertFalse(object.getItem('is_solo_release'))
    
    
  def test_new(self):
    object = Song(self.data1)
    self.assertEqual(object.getItem('song_id'), '')
    self.assertEqual(object.getItem('song_name'), 'Enter Sandman')
    self.assertEqual(object.getItem('band_id'), 1)
    self.assertFalse(object.getItem('is_solo_release'))
    
  def test_JSON(self):
    object1 = Song(self.data1)
    jsonStr = object1.toJSON()
    
    object2 = Song()
    self.assertEqual(object2.getItem('song_name'), '')
    self.assertEqual(object2.getItem('band_id'), '')
    object2.fromJSON(jsonStr)
    self.assertEqual(object2.getItem('song_name'), 'Enter Sandman')
    self.assertEqual(object2.getItem('band_id'), 1)    
    
    
  def test_mutators_and_accessors(self):
    object1 = Song()
    self.assertTrue(object1.setItem('song_name', 'Enter Sandman'))
    self.assertTrue(object1.setItem('band_id', 1))
    self.assertTrue(object1.setItem('is_solo_release', 1))
    
    self.assertEqual(object1.getItem('song_name'), 'Enter Sandman')
    self.assertEqual(object1.getItem('band_id'), 1)
    self.assertTrue(object1.getItem('is_solo_release'))
    
  def test_getRow(self):
    object = Song()
    self.assertTrue(object.getRow(1))
    self.assertNotEqual(object.getItem('song_id'), '')
    self.assertEqual(object.getItem('song_name'), 'Sad But True')
    
  def test_SaveAndDeleteFromDatabase(self):
    object1 = Song(self.data1)
    self.assertTrue(object1.addToDatabase())
    self.assertNotEqual(object1.getItem('song_id'), '')
    song_id = object1.getItem('song_id')

    object2 = Song()
    self.assertTrue(object2.getRow( song_id))
    self.assertNotEqual(object2.getItem('song_id'), '')
    self.assertTrue(object2.deleteFromDatabase())

    object3 = Song()
    self.assertFalse(object3.getRow( song_id))
    self.assertEqual(object3.getItem('song_id'), '')
    
  def test_duplicateSongs(self):
    object1 = Song(self.data1)
    self.assertTrue(object1.addToDatabase())
    self.assertNotEqual(object1.getItem('song_id'), '')

    object2 = Song(self.data1)
    self.assertFalse(object2.addToDatabase())
    self.assertEqual(object2.getItem('song_id'), '')
    
    self.assertTrue(object1.deleteFromDatabase())

    
  def test_notDuplicate(self):
    object1 = Song(self.data2)
    object2 = Song(self.data1)
    self.assertFalse(object1.notDuplicate())
    self.assertTrue(object2.notDuplicate())

  def test_saveToDatabase(self):
    object = Song()
    self.assertTrue(object.getRow( 7))
    self.assertFalse(object.getItem('is_solo_release'))
    self.assertTrue(object.setItem('is_solo_release', 1))
    self.assertTrue(object.saveToDatabase())
    self.assertTrue(object.getItem('is_solo_release'))
    self.assertTrue(object.setItem('is_solo_release', 0))
    self.assertTrue(object.saveToDatabase())
    self.assertFalse(object.getItem('is_solo_release'))  
    