import json
import unittest

from app import create_app
from app.api.v1.models.red_flags_model import records_list
from instance.config import app_config


class Test(unittest.TestCase):

    def setUp(self):
        """ Define test variables"""

        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.data = {
            "comment": "new corruption",
            "created_by": "2",
            "record_type": "intervention",
            "location": "10.0123, -34.034"
        }

    def tearDown(self):
        """Removes all initialised variables"""
        # self.app_context.pop()

    def test_it_creates_incident_records(self):
        """test if posts an incident record """

        response = self.client.post('api/v1/red-flags', json=self.data)

        self.assertEqual(response.status_code, 201)
        

    def test_if_no_comment(self):
        """ test if user leaves out comment"""

        response = self.client.post('api/v1/red-flags', json={
            "comment": "",
            "created_by": "333",
            "location": "'-34.397,150.644'",
            "record_type": "onlycomment"
        })

        self.assertEqual(400, response.status_code)
        self.assertEqual(response.get_json(), {
            "message": "Please fill all the required fields", "status": 400
        })

    def test_if_comment_has_special_chars(self):
        response = self.client.post('api/v1/red-flags', json={
            "comment": "#$%^&*@#$^",
            "created_by": "2",
            "record_type": "intervention",
            "location": "10.0123, -34.034"
        })

        self.assertEqual(400, response.status_code)
        self.assertEqual(response.get_json(), {
            "message": "A comment cannot contain special characters e.g $"
        })

    def test_if_invalid_location(self):
        response = self.client.post('api/v1/red-flags', json={
            "comment": "new corruption report",
            "created_by": "2",
            "record_type": "red-flag",
            "location": "10768687.0123, -367787684.034"
        })

        self.assertEqual(400, response.status_code)
        self.assertEqual(response.get_json(), {
            "message": "Please ensure comma separated lat and long and within appropriate ranges", "status": 400
        })

    def test_if_record_type_is_invalid(self):
        response = self.client.post('api/v1/red-flags', json={
            "comment": "new corruption report",
            "created_by": "2",
            "record_type": "invalid",
            "location": "10.0123, -34.034"
        })

        self.assertEqual(400, response.status_code)
        self.assertEqual(response.get_json(), {
            "message": "Record type can only be a red-flag or an intervention", "status": 400
        })

    def test_if_gets_all_records(self):
        """Test the get all records but empty endpoint"""
       
        response = self.client.post('api/v1/red-flags', json=self.data)
        self.assertEqual(201, response.status_code)

        response = self.client.get('api/v1/red-flags')
        self.assertEqual(200, response.status_code)
        

    def test_it_responds_empty_list(self):
        response = self.client.get('api/v1/red-flags')
        self.assertEqual(200, response.status_code)

    def test_get_single_record_by_id(self):
       
        response = self.client.post('api/v1/red-flags', json=self.data)

        response = self.client.get('api/v1/red-flags/1')
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response.get_json()['Record data'][0]['record_id'])

    def test_get_record_fails_given_non_existent_id(self):

        response = self.client.get('api/v1/red-flags/456')
        self.assertEqual(404, response.status_code)
        self.assertEqual(response.get_json(), {
            "message": "This record does not exist", "status": 404
        })

    def test_get_non_existent_record(self):
        response = self.client.get('api/v1/red-flags/1')
        self.assertEqual(404, response.status_code)
        self.assertEqual(response.get_json(), {
            "message": "This record does not exist", "status": 404
        })

    def test_delete_one_record_given_id(self):
        response = self.client.post('api/v1/red-flags', json=self.data)
        self.assertEqual(201, response.status_code)

        
        response = self.client.delete('api/v1/red-flags/1', json=self.data)
        self.assertEqual(200, response.status_code)

        
        response = self.client.get('api/v1/red-flags/1')
        self.assertEqual(404, response.status_code)
        self.assertEqual(response.get_json(), {
            "message": "This record does not exist", "status": 404
        })

    def test_delete_if_id_provided_doesnt_exist(self):
        response = self.client.delete('api/v1/red-flags/1')
        self.assertEqual(404, response.status_code)
        self.assertEqual(response.get_json(), {
            "message": "This record does not exist", "status": 404
        })

    def test_it_updates_incident_record_comment(self):
        
        self.client.post('api/v1/red-flags', json=self.data)       
        response = self.client.patch('api/v1/red-flags/1/comment', json={
            "comment": "new comment update"
        })
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            {"status": 200, "message": "Updated red-flag record's comment"}, response.get_json()['data'][0])

    def test_it_updates_non_existent_record_by_id(self):
        response = self.client.patch('api/v1/red-flags/190/comment', json={
            "comment": "new comment update"
        })
        self.assertEqual({"message": "This record does not exist",
                          "status": 404}, response.get_json())

    def test_it_updates_incident_record_location(self):

        self.client.post('api/v1/red-flags', json=self.data)

        response = self.client.patch('api/v1/red-flags/1/location', json={
            "location": "-4.8799074,194.7565664"
        })
        self.assertEqual(200, response.status_code)

    def test_it_updates_invalid_location(self):

        self.client.post('api/v1/red-flags', json=self.data)

        response = self.client.patch('api/v1/red-flags/1/location', json={
            "location": "67567567.8799074,78988785.7565664"
        })
        self.assertEqual(400, response.status_code)
        self.assertEqual(response.get_json(), {
            "message": "Please ensure comma separated lat and long and within appropriate ranges", "status": 400
        })
        

    def test_it_returns_if_location_id_is_null(self):

        response = self.client.patch('api/v1/red-flags/10000/location', json={
            "location": "-4.8799074,194.7565664"
        })
        self.assertEqual({"message": "This record does not exist", "status": 404}, response.get_json())


if __name__ == "__main__":
    unittest.main()
