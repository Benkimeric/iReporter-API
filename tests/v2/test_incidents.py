import unittest
from flask import json
from app.api.v2.models.db_model import Database
from db_config import db_connection, create_super_admin
from app import create_app, create_tables
from .incidents_data import (sign_up_data, sign_in_data, new_incident_data,
                             invalid_comment, invalid_location, invalid_type,
                             sign_up_data_2, edit_comment_data,
                             edit_location_data, invalid_comment_data,
                             invalid_location_data, admin_sign_in,
                             admin_status_change
                             )


class IncidentsTests(unittest.TestCase):
    """contains test cases for red-flags and interventions"""

    def setUp(self):
        """ Define tests variables"""

        self.app = create_app(config_name='testing')
        create_super_admin()
        self.client = self.app.test_client()

        # sign up a user
        self.signup = self.client.post(
            "api/v2/auth/signup",
            data=json.dumps(sign_up_data),
            content_type='application/json')
        # login the user
        self.login_response = self.client.post('/api/v2/auth/login',
                                               data=json.dumps(sign_in_data),
                                               content_type='application/json')
        self.login_result = json.loads(self.login_response.data)
        self.token = self.login_result['token']

        # login the admin
        self.response_admin = self.client.post('/api/v2/auth/login',
                                               data=json.dumps(admin_sign_in),
                                               content_type='application/json')
        self.assertEqual(200, self.response_admin.status_code)
        self.admin_result = json.loads(self.response_admin.data)

        self.admin_token = self.admin_result['token']

    def tearDown(self):
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS users")
        cursor.execute("DROP TABLE IF EXISTS incidents")
        connection.commit()

    def test_can_create_incident(self):
        """test that with valid data can create an incident record"""

        response = self.client.post('/api/v2/interventions',
                                    data=json.dumps(new_incident_data),
                                    headers={'Authorization': 'Bearer ' +
                                             self.token, 'content-type':
                                             'application/json'})
        result = json.loads(response.data)
        self.assertEqual(result['status'], 201)
        self.assertEqual(response.status_code, 201)

    def test_throws_error_on_invalid_comment(self):
        """test for when invalid comment data is provided"""

        response = self.client.post('/api/v2/interventions',
                                    data=json.dumps(invalid_comment),
                                    headers={'Authorization': 'Bearer ' +
                                             self.token, 'content-type':
                                             'application/json'})
        result = json.loads(response.data)
        self.assertEqual(result['message'], 'A comment cannot contain '
                         'special characters e.g $'
                         )
        self.assertEqual(response.status_code, 400)

    def test_throws_error_on_invalid_location(self):
        """test for when invalid location data is provided"""

        response = self.client.post('/api/v2/interventions',
                                    data=json.dumps(invalid_location),
                                    headers={'Authorization': 'Bearer ' +
                                             self.token, 'content-type':
                                             'application/json'})
        result = json.loads(response.data)
        self.assertEqual(result['message'], "Please ensure comma separated "
                         "lat and long and "
                         "within appropriate ranges"
                         )
        self.assertEqual(response.status_code, 400)

    def test_throws_error_on_invalid_record_type(self):
        """test for when invalid location data is provided"""

        response = self.client.post('/api/v2/interventions',
                                    data=json.dumps(invalid_type),
                                    headers={'Authorization': 'Bearer ' +
                                             self.token, 'content-type':
                                             'application/json'})
        result = json.loads(response.data)
        self.assertEqual(result['message'], "Record type can only be a "
                         "red-flag or an intervention"
                         )
        self.assertEqual(response.status_code, 400)

    def test_gets_all_incidents(self):
        """test that can fetch all the incident records"""
        # post 1
        self.client.post('/api/v2/interventions',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})
        # post 2
        self.client.post('/api/v2/interventions',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})
        # fetch
        response = self.client.get('/api/v2/interventions',
                                   headers={'Authorization': 'Bearer ' +
                                            self.token, 'content-type':
                                            'application/json'})
        # assert
        self.assertEqual(response.status_code, 200)

    def test_getting_empty_list(self):
        """test that can return message on empty list"""
        # fetch empty
        response = self.client.get('/api/v2/interventions',
                                   headers={'Authorization': 'Bearer ' +
                                            self.token, 'content-type':
                                            'application/json'})
        # assert
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data)
        self.assertEqual(result['message'],
                         'No Intervention records available')

    def test_gets_a_single(self):
        """test that can fetch a single the incident record"""
        # post 1
        self.client.post('/api/v2/interventions',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})
        # post 2
        self.client.post('/api/v2/interventions',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})
        # fetch second record
        response = self.client.get('/api/v2/interventions/2',
                                   headers={'Authorization': 'Bearer ' +
                                            self.token, 'content-type':
                                            'application/json'})
        # assert
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result['status'], 200)

    def test_get_incident_by_a_non_digit_id(self):
        """test returns message when incident id is not digit"""

        # fetch
        response = self.client.get('/api/v2/interventions/fhgfhg',
                                   headers={'Authorization': 'Bearer ' +
                                            self.token, 'content-type':
                                            'application/json'})
        # assert
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertEqual(result['message'],
                         'intervention ID fhgfhg is invalid')

    def test_get_non_existent_record(self):
        """test returns message if record doesnt exist"""
        # post 1
        self.client.post('/api/v2/interventions',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})
        # fetch non-existent record
        response = self.client.get('/api/v2/interventions/2000',
                                   headers={'Authorization': 'Bearer ' +
                                            self.token, 'content-type':
                                            'application/json'})
        # assert
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data)
        self.assertEqual(result['message'],
                         'This intervention record does not exist'
                         )

    def test_deletes_a_record(self):
        """test can delete a record"""
        # post 1
        self.client.post('/api/v2/interventions',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})
        # delete the record
        response = self.client.delete('/api/v2/interventions/1',
                                      headers={'Authorization': 'Bearer ' +
                                               self.token, 'content-type':
                                               'application/json'})
        # assert
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result['message'],
                         'intervention has been deleted'
                         )

    def test_gives_error_on_wrong_input_for_id_on_delete(self):
        """test it gives an error on entering a non digit id"""
        # post 1
        self.client.post('/api/v2/interventions',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})
        # enter non digit id and delete
        response = self.client.delete('/api/v2/interventions/s',
                                      headers={'Authorization': 'Bearer ' +
                                               self.token, 'content-type':
                                               'application/json'})
        # assert
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertEqual(result['message'],
                         'intervention ID s is invalid'
                         )

    def test_cant_delete_others_incident(self):
        """test if a user tries to delete other persons record"""
        # post 1 by user 1
        self.client.post('/api/v2/interventions',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})
        # signup user 2
        response = self.client.post("api/v2/auth/signup",
                                    data=json.dumps(sign_up_data_2),
                                    content_type='application/json')

        # get the token
        sign_up_result = json.loads(response.data)
        token2 = sign_up_result['data'][0]['token']
        # delete the record
        response = self.client.delete('/api/v2/interventions/1',
                                      headers={'Authorization': 'Bearer ' +
                                               token2, 'content-type':
                                               'application/json'})
        # assert
        self.assertEqual(response.status_code, 403)
        result = json.loads(response.data)
        self.assertEqual(result['message'],
                         'You can not delete other peoples records!'
                         )

    def test_can_edit_comment(self):
        """test can update a comment"""
        # post 1
        self.client.post('/api/v2/interventions',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})
        # patch the record
        response = self.client.patch('/api/v2/interventions/1/comment',
                                     data=json.dumps(edit_comment_data),
                                     headers={'Authorization': 'Bearer ' +
                                              self.token, 'content-type':
                                              'application/json'})
        # assert
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result['message'],
                         'Updated intervention records comment'
                         )

    def test_cannot_edit_others_comment(self):
        """test cant edit others comment"""
        # post 1 by user 1
        self.client.post('/api/v2/interventions',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})
        # signup user 2
        response = self.client.post("api/v2/auth/signup",
                                    data=json.dumps(sign_up_data_2),
                                    content_type='application/json')

        # get the token
        sign_up_result = json.loads(response.data)
        token2 = sign_up_result['data'][0]['token']
        # patch the record
        response = self.client.patch('/api/v2/interventions/1/comment',
                                     data=json.dumps(edit_comment_data),
                                     headers={'Authorization': 'Bearer ' +
                                              token2, 'content-type':
                                              'application/json'})
        # assert
        self.assertEqual(response.status_code, 403)
        result = json.loads(response.data)
        self.assertEqual(result['message'],
                         'You can not edit other peoples records!'
                         )

    def test_can_edit_location(self):
        """test can update a location"""
        # post 1
        self.client.post('/api/v2/interventions',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})
        # patch the record
        response = self.client.patch('/api/v2/interventions/1/location',
                                     data=json.dumps(edit_location_data),
                                     headers={'Authorization': 'Bearer ' +
                                              self.token, 'content-type':
                                              'application/json'})
        # assert
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result['message'],
                         'Updated intervention records location'
                         )

    def test_cannot_edit_others_location(self):
        """test cant edit others location"""
        # post 1 by user 1
        self.client.post('/api/v2/interventions',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})
        # signup user 2
        response = self.client.post("api/v2/auth/signup",
                                    data=json.dumps(sign_up_data_2),
                                    content_type='application/json')

        # get the token
        sign_up_result = json.loads(response.data)
        token2 = sign_up_result['data'][0]['token']
        # patch the record
        response = self.client.patch('/api/v2/interventions/1/location',
                                     data=json.dumps(edit_location_data),
                                     headers={'Authorization': 'Bearer ' +
                                              token2, 'content-type':
                                              'application/json'})
        # assert
        self.assertEqual(response.status_code, 403)
        result = json.loads(response.data)
        self.assertEqual(result['message'],
                         'You can not edit other peoples records!'
                         )

    def test_throws_error_on_patch_invalid_comment(self):
        """test cant edit comment with wrong data"""
        # post 1
        self.client.post('/api/v2/interventions',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})
        # patch the record
        response = self.client.patch('/api/v2/interventions/1/comment',
                                     data=json.dumps(invalid_comment_data),
                                     headers={'Authorization': 'Bearer ' +
                                              self.token, 'content-type':
                                              'application/json'})
        # assert
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertEqual(result['message'],
                         'A comment cannot contain special characters e.g $'
                         )

    def test_throws_error_on_patch_invalid_location(self):
        """test cant edit location with wrong data"""
        # post 1
        self.client.post('/api/v2/interventions',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})
        # patch the record
        response = self.client.patch('/api/v2/interventions/1/location',
                                     data=json.dumps(invalid_location_data),
                                     headers={'Authorization': 'Bearer ' +
                                              self.token, 'content-type':
                                              'application/json'})
        # assert
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertEqual(result['message'],
                         'Please ensure comma separated lat and long and '
                         'within appropriate ranges'
                         )

    def test_admin_can_change_status(self):
        """test that admin can change status"""
        # post 1
        self.client.post('/api/v2/interventions',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})

        # admin patch
        response = self.client.patch('/api/v2/interventions/1/status',
                                     data=json.dumps(admin_status_change),
                                     headers={'Authorization': 'Bearer ' +
                                              self.admin_token, 'content-type':
                                              'application/json'})
        # assert
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result['message'],
                         'Updated intervention record status'
                         )

    def test_comment_cant_be_edited_by_user_after_admin_status_change(self):
        """test user can't change status after status change"""
        # post 1
        self.client.post('/api/v2/interventions',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})

        # admin patch
        response = self.client.patch('/api/v2/interventions/1/status',
                                     data=json.dumps(admin_status_change),
                                     headers={'Authorization': 'Bearer ' +
                                              self.admin_token, 'content-type':
                                              'application/json'})
        # user patch
        response = self.client.patch('/api/v2/interventions/1/comment',
                                     data=json.dumps(edit_comment_data),
                                     headers={'Authorization': 'Bearer ' +
                                              self.token, 'content-type':
                                              'application/json'})
        # assert
        self.assertEqual(response.status_code, 403)
        result = json.loads(response.data)
        self.assertEqual(result['message'],
                         'You can not edit this record, it is already resolved'
                         )

    def test_location_cant_be_edited_by_user_after_admin_status_change(self):
        """test user can't change status after status change"""
        # post 1
        self.client.post('/api/v2/interventions',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})

        # admin patch
        response = self.client.patch('/api/v2/interventions/1/status',
                                     data=json.dumps(admin_status_change),
                                     headers={'Authorization': 'Bearer ' +
                                              self.admin_token, 'content-type':
                                              'application/json'})
        # user patch
        response = self.client.patch('/api/v2/interventions/1/location',
                                     data=json.dumps(edit_location_data),
                                     headers={'Authorization': 'Bearer ' +
                                              self.token, 'content-type':
                                              'application/json'})
        # assert
        self.assertEqual(response.status_code, 403)
        result = json.loads(response.data)
        self.assertEqual(result['message'],
                         'You can not edit this record, it is already resolved'
                         )

    def test_cant_delete_after_admin_status_change(self):
        """test user can't delete incident after status change"""
        # post 1
        self.client.post('/api/v2/interventions',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})

        # admin patch
        response = self.client.patch('/api/v2/interventions/1/status',
                                     data=json.dumps(admin_status_change),
                                     headers={'Authorization': 'Bearer ' +
                                              self.admin_token, 'content-type':
                                              'application/json'})
        # user delete
        response = self.client.delete('/api/v2/interventions/1/',
                                      headers={'Authorization': 'Bearer ' +
                                               self.token, 'content-type':
                                               'application/json'})
        # assert
        self.assertEqual(response.status_code, 403)
        result = json.loads(response.data)
        self.assertEqual(result['message'],
                         'You can not delete this record, '
                         'it is already resolved'
                         )

    def test_edit_comment_on_non_digit_id(self):
        """test throws error on non digit ID"""
        # post 1
        self.client.post('/api/v2/interventions',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})
        # enter non digit id and patch
        response = self.client.patch('/api/v2/interventions/s/comment',
                                     data=json.dumps(edit_comment_data),
                                     headers={'Authorization': 'Bearer ' +
                                              self.token, 'content-type':
                                              'application/json'})
        # assert
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertEqual(result['message'],
                         'intervention ID s is invalid'
                         )

    def test_edit_comment_on_non_digit_id(self):
        """test throws error on non digit ID"""
        # post 1
        self.client.post('/api/v2/interventions',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})
        # enter non digit id and patch
        response = self.client.patch('/api/v2/interventions/s/location',
                                     data=json.dumps(edit_location_data),
                                     headers={'Authorization': 'Bearer ' +
                                              self.token, 'content-type':
                                              'application/json'})
        # assert
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertEqual(result['message'],
                         'intervention ID s is invalid'
                         )
