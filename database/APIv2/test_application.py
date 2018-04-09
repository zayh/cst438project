import unittest
import requests
import json

class TestDBAPIRequests(unittest.TestCase):

    base_url = 'http://18.219.102.221/api/'
    headers = {'Content-Type': 'application/json'}

    # Define test data here. Each value is a test value
    db_tables = {
        'account': {
            'username' : 'testname',
            'firstname': 'Test First Name',
            'lastname' : 'Test Last Name',
            'password' : 'weakpassword',
        },
        'album': {
            'album_name' : 'test album 1',
            'band_id' : '',
            'release_date' : '1999-04-14',
        },
        'band': {
            'band_name' : 'test band 1',
        },
        'favorite': {
            'account_id' : '',
            'album_id' : '',         
        },
        'rating' : {
            'account_id' : '',
            'rating_date' : '2018-04-14',
            'album_id' : '',
            'rating': 3,
            'comment' : 'this is a test',
        },
        'song' : {
            'song_name' : 'test song',
            'album_id' : '',
            'band_id' : '',
            'track_number' : 7,
        },
        'wishlist' : {
            'account_id': '',
            'album_id': '',
        },
    }

    def test_get(self):
        # Check each table, sending a GET to each.
        # Test for status_code 200 "OK"
        for table in self.db_tables:
            url = self.base_url + table
            response = requests.get(url, headers=self.headers)
            self.assertEqual(response.status_code, 200)           
            
            
    def test_put_and_delete(self):
        # Create Test Band. Insert it. Check that it went in. Then delete it.
        
        url = self.base_url + 'band'
        band_name = self.db_tables['band']['band_name']
        
        response = requests.post(url, headers=self.headers, json=self.db_tables['band'])
        self.assertEqual(response.status_code, 201)
        return_data = response.json()
        self.assertEqual(return_data['band_name'], band_name)
        band_id = return_data['band_id']
        url += '/{}'.format(band_id)
        response = requests.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_create_and_delete_all(self):
        # Create everything: account, band, album, song, rating, favorit, and wishlist.
        # Then delete the band and account. Everything should clear.
        # Foreign Keys require things to be done in an order.
        url = self.base_url
        # Initize vars we'll fill later
        account_id = ''
        band_id = ''
        rating_id = ''
        
        # Create the user
        response = requests.post(url + 'account', headers=self.headers, json=self.db_tables['account'])
        # Check that we got a 201 "OK"
        self.assertEqual(response.status_code, 201)
        # Save the account_id for later
        account_id = response.json()['account_id']
        # Now make the band
        response = requests.post(url + 'band', headers=self.headers, json=self.db_tables['band'])
        # Check for "OK"
        self.assertEqual(response.status_code, 201)
        # Save the band_id for later
        band_id = response.json()['band_id']
        # Now lets add an album
        self.db_tables['album']['band_id'] = band_id
        response = requests.post(url + 'album', headers=self.headers, json=self.db_tables['album'])
        # Save album_id
        album_id = response.json()['album_id']
        # Now lets add a song
        # Stuff the band_id and album_id into the song dictionary firstname
        self.db_tables['song']['band_id'] = band_id
        self.db_tables['song']['album_id'] = album_id
        response = requests.post(url + 'song', headers=self.headers, json=self.db_tables['song'])
        self.assertEqual(response.status_code, 201)
        # Now lets have the user put it on their wishlist
        self.db_tables['wishlist']['account_id'] = account_id
        self.db_tables['wishlist']['album_id'] = album_id
        response = requests.post(url + 'wishlist', headers=self.headers, json=self.db_tables['wishlist'])
        self.assertEqual(response.status_code, 201)
        # Now lets have the user rate the album
        self.db_tables['rating']['account_id'] = account_id
        self.db_tables['rating']['album_id'] = album_id
        response = requests.post(url + 'rating', headers=self.headers, json=self.db_tables['rating'])
        self.assertEqual(response.status_code, 201)
        # Save the rating_id
        rating_id = response.json()['rating_id']
        # Now lets GET the rating we just made
        response = requests.get(url + 'rating/' + str(rating_id), headers=self.headers)
        self.assertEqual(response.status_code, 200)
        # Let's make sure
        self.assertEqual(response.json()['rating_date'], self.db_tables['rating']['rating_date'])
        
        # Now let's clean up
        response = requests.delete(url + 'account/' + str(account_id))
        self.assertEqual(response.status_code, 204)
        response = requests.delete(url + 'band/' + str(band_id))
        self.assertEqual(response.status_code, 204)
            
    def test_searching(self):
        # Add a band
        create_band = requests.post(self.base_url + 'band', headers=self.headers, json=self.db_tables['band'])
        new_band_id = create_band.json()['band_id']
        
        # Search for the band by name
        
        filters = [dict(name='band_name', op='eq', val='test band 1')]
        params = dict(q=json.dumps(dict(filters=filters)))

        find_band = requests.get(self.base_url + 'band', params=params, headers=self.headers)
        self.assertEqual(find_band.status_code, 200)
        self.assertEqual(new_band_id, find_band.json()['objects'][0]['band_id'])

        # Now delete it
        response = requests.delete(self.base_url + 'band/' + str(new_band_id))
        self.assertEqual(response.status_code, 204)
        
    def test_editing(self):
        # Add a band
        create_band = requests.post(self.base_url + 'band', headers=self.headers, json=self.db_tables['band'])
        new_band_id = create_band.json()['band_id']
        
        updates = {'band_name' : 'test band 2'}
        
        # Now change the name
        edit_band = requests.put(self.base_url + 'band/' + str(new_band_id), headers=self.headers, json=updates)
        self.assertEqual(edit_band.status_code, 200)
        
        # Just in case, get the band and check the name
        check_band = requests.get(self.base_url + 'band/' + str(new_band_id), headers=self.headers)
        self.assertEqual(check_band.status_code,200)
        self.assertEqual(check_band.json()['band_name'], updates['band_name'])
        
        # Now clean up
        delete_band = requests.delete(self.base_url + 'band/' + str(new_band_id))
        self.assertEqual(delete_band.status_code, 204)
        
if __name__ == '__main__':
    unittest.main()
    