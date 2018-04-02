import unittest
from Band import Band

class TestBand(unittest.TestCase):

  data1 = {
    'band_id' : '',
    'band_name': 'Spinal Tap'
  }

  data2 = { 
    'band_name' : 'Prince',
    'is_solo_artist' : True
  }
  
  data3 = {
    'band_name' : 'Def Leppard'
  }
  
  data4 ={
    'band_name' : 'Metallica'
  }
  
  def test_createEmptyBand(self):
    object = Band()
    self.assertIsInstance(object, Band)
    self.assertEqual(object.getItem('band_id'), '')
    self.assertEqual(object.getItem('is_solo_artist'), '')
    self.assertEqual(object.getItem('band_name'), '')
    
  def test_createNonEmptyBand(self):
    object1 = Band(self.data1)
    self.assertEqual(object1.getItem('band_id'), '')
    self.assertEqual(object1.getItem('band_name'), 'Spinal Tap')
    self.assertFalse(object1.getItem('is_solo_artist'))
    
    object2 = Band(self.data2)
    self.assertEqual(object2.getItem('band_id'), '')
    self.assertEqual(object2.getItem('band_name'), 'Prince')
    self.assertTrue(object2.getItem('is_solo_artist'))
    
  def test_JSON(self):
    object1 = Band(self.data2)
    dataStr = object1.toJSON()
    
    object2 = Band()
    object2.fromJSON(dataStr)
    self.assertEqual(object2.getItem('band_name'), 'Prince')
    self.assertTrue(object2.getItem('is_solo_artist'))
    
  def test_mutators_and_accessors(self):
    object1 = Band(self.data3)
    object1.setItem('is_solo_artist', 1)

    object2 = Band(self.data2)
    object2.setItem('is_solo_artist', 0)
    
    self.assertEqual(object1.getItem('band_name'), 'Def Leppard')
    self.assertEqual(object2.getItem('band_name'), 'Prince')
    self.assertTrue(object1.getItem('is_solo_artist'))
    self.assertFalse(object2.getItem('is_solo_artist'))
    
  def test_getRow(self):
    object = Band()
    self.assertTrue(object.getRow(1))
    self.assertNotEqual(object.getItem('band_id'), '')
    self.assertEqual(object.getItem('band_name'), 'Metallica')

    
  def test_SaveAndDeleteFromDatabase(self):
    object1 = Band(self.data1)
    object1.addToDatabase()
    band_id = object1.getItem('band_id')

    object2 = Band()
    self.assertTrue(object2.getRow(band_id))
    self.assertEqual(object2.getItem('band_name'), 'Spinal Tap')
    object2.deleteFromDatabase()
    
  def test_notDuplicate(self):
    object1 = Band(self.data4)
    object2 = Band(self.data1)
    self.assertFalse(object1.notDuplicate())
    self.assertTrue(object2.notDuplicate())

  def test_saveToDatabase(self):
    object = Band()
    self.assertTrue(object.getRow(4))
    self.assertFalse(object.getItem('is_solo_artist'))
    self.assertTrue(object.setItem('is_solo_artist', 1))
    self.assertTrue(object.saveToDatabase())
    self.assertTrue(object.getItem('is_solo_artist'))
    self.assertTrue(object.setItem('is_solo_artist', 0))
    self.assertTrue(object.saveToDatabase())
    self.assertFalse(object.getItem('is_solo_artist'))   
    