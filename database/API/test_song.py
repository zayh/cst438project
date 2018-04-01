import unittest
from Song import Song

class TestSong(unittest.TestCase):

  def test_createEmptySong(self):
    object = Song()
    self.assertIsInstance(object, Song)
    self.assertEqual(object.getSongID(), '')
    self.assertEqual(object.getSongName(), '')
    self.assertEqual(object.getBandID(), '')
    self.assertFalse(object.isSoloRelease())
    
    
  def test_new(self):
    object = Song()
    object.new('Enter Sandman', False, 1)
    self.assertEqual(object.getSongID(), '')
    self.assertEqual(object.getSongName(), 'Enter Sandman')
    self.assertEqual(object.getBandID(), 1)
    self.assertFalse(object.isSoloRelease())
    
  def test_toJSON(self):
    object = Song()
    object.new('Enter Sandman', False, 1)
    self.assertEqual(object.toJSON(), 
      "{ song_id: , song_name: 'Enter Sandman', is_solo_release: False, band_id: 1 }"
    )
    
  def test_mutators_and_accessors(self):
    object1 = Song()
    self.assertTrue(object1.setSongName('Enter Sandman'))
    self.assertTrue(object1.setBandID(1))
    self.assertTrue(object1.setSoloRelease(True))
    
    self.assertEqual(object1.getSongName(), 'Enter Sandman')
    self.assertEqual(object1.getBandID(), 1)
    self.assertTrue(object1.isSoloRelease())
    
  def test_getBySongID(self):
    object = Song()
    self.assertTrue(object.getBy('song_id', 1))
    self.assertNotEqual(object.getSongID(), '')
    self.assertEqual(object.getSongName(), 'Sad But True')
    
  def test_getByError(self):
    object = Song()
    self.assertFalse(object.getBy('band_id', 1))
    self.assertEqual(object.getSongID(), '')
    
  def test_SaveAndDeleteFromDatabase(self):
    object1 = Song()
    self.assertTrue(object1.new('Enter Sandman', False, 1))
    self.assertTrue(object1.addToDatabase())
    self.assertNotEqual(object1.getSongID(), '')
    song_id = object1.getSongID()

    object2 = Song()
    self.assertTrue(object2.getBy('song_id', song_id))
    self.assertNotEqual(object2.getSongID(), '')
    self.assertTrue(object2.deleteFromDatabase())

    object3 = Song()
    self.assertFalse(object3.getBy('song_id', song_id))
    self.assertEqual(object3.getSongID(), '')
    
  def test_duplicateSongs(self):
    object1 = Song()
    self.assertTrue(object1.new('Enter Sandman', False, 1))
    self.assertTrue(object1.addToDatabase())
    self.assertNotEqual(object1.getSongID(), '')

    object2 = Song()
    self.assertTrue(object2.new('Enter Sandman', False, 1))
    self.assertFalse(object2.addToDatabase())
    self.assertEqual(object2.getSongID(), '')
    
    self.assertTrue(object1.deleteFromDatabase())

    
  def test_isSongNameAvailable(self):
    object = Song()
    self.assertFalse(object.isSongNameAvailable('Sad But True', 1))
    self.assertTrue(object.isSongNameAvailable('Enter Sandman', 1))

    