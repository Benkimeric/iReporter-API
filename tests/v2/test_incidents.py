import unittest
from flask import json
from app.api.v2.models.db_model import Database
from db_config import db_connection, create_super_admin
from app import create_app, create_tables
from .incidents_data import *


class IncidentsTests(unittest.TestCase):
    """contains test cases for red-flags and interventions"""

    def setUp(self):
        """ Define tests variables"""

        self.app = create_app(config_name='testing')
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
        self.token = self.login_result['data'][0]['token']

        # login the admin
        self.response_admin = self.client.post('/api/v2/auth/login',
                                               data=json.dumps(admin_sign_in),
                                               content_type='application/json')
        self.assertEqual(200, self.response_admin.status_code)
        self.admin_result = json.loads(self.response_admin.data)

        self.admin_token = self.admin_result['data'][0]['token']

    def tearDown(self):
        """to destroy tabbles after each test"""
        connection = db_connection()
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS users CASCADE")
        cursor.execute("DROP TABLE IF EXISTS incidents CASCADE")
        connection.commit()

    def test_can_create_incident(self):
        """test that with valid data can create an incident record"""

        response = self.client.post('/api/v2/intervention',
                                    data=json.dumps(new_incident_data),
                                    headers={'Authorization': 'Bearer ' +
                                             self.token, 'content-type':
                                             'application/json'})
        result = json.loads(response.data)
        self.assertEqual(result['status'], 201)
        self.assertEqual(response.status_code, 201)

    def test_throws_error_on_invalid_comment(self):
        """test for when invalid comment data is provided"""

        response = self.client.post('/api/v2/intervention',
                                    data=json.dumps(invalid_comment),
                                    headers={'Authorization': 'Bearer ' +
                                             self.token, 'content-type':
                                             'application/json'})
        result = json.loads(response.data)
        self.assertEqual(result['message'],
                         'A comment cannot contain special characters e.g $ '
                         'or empty space'
                         )
        self.assertEqual(response.status_code, 400)

    def test_throws_error_on_invalid_location(self):
        """test for when invalid location data is provided"""

        response = self.client.post('/api/v2/intervention',
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

        response = self.client.post('/api/v2/intervention',
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
        # post 1 incident
        self.client.post('/api/v2/intervention',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})
        # post 2nd incident
        self.client.post('/api/v2/intervention',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})
        # fetch all
        response = self.client.get('/api/v2/intervention',
                                   headers={'Authorization': 'Bearer ' +
                                            self.token, 'content-type':
                                            'application/json'})
        # assert
        self.assertEqual(response.status_code, 200)

    def test_getting_empty_list(self):
        """test that can return message on empty list"""
        # fetch empty database
        response = self.client.get('/api/v2/intervention',
                                   headers={'Authorization': 'Bearer ' +
                                            self.token, 'content-type':
                                            'application/json'})
        # assert
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data)
        self.assertEqual(result['message'],
                         'No intervention records available')

    def test_gets_a_single(self):
        """test that can fetch a single the incident record"""
        # post 1 incident
        self.client.post('/api/v2/intervention',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})
        # post 2nd incident
        self.client.post('/api/v2/intervention',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})
        # fetch second record
        response = self.client.get('/api/v2/intervention/2',
                                   headers={'Authorization': 'Bearer ' +
                                            self.token, 'content-type':
                                            'application/json'})
        # assert
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result['status'], 200)

    def test_get_incident_by_a_non_digit_id(self):
        """test returns message when incident id is not digit"""

        # fetch using non digit id
        response = self.client.get('/api/v2/intervention/fhgfhg',
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
        # post 1 incident
        self.client.post('/api/v2/intervention',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})
        # fetch non-existent record
        response = self.client.get('/api/v2/intervention/2000',
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
        # post 1 incident
        self.client.post('/api/v2/intervention',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})
        # delete the record
        response = self.client.delete('/api/v2/intervention/1',
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
        # post 1 incident
        self.client.post('/api/v2/intervention',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})
        # enter non digit id and delete
        response = self.client.delete('/api/v2/intervention/s',
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
        # post a record by user 1
        self.client.post('/api/v2/intervention',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})
        # signup user 2
        response = self.client.post("api/v2/auth/signup",
                                    data=json.dumps(sign_up_data_2),
                                    content_type='application/json')

        # login the user 2 to get the token
        login_response = self.client.post('/api/v2/auth/login',
                                          data=json.dumps(sign_in_data_2),
                                          content_type='application/json')
        login_result = json.loads(login_response.data)
        token2 = login_result['data'][0]['token']

        # delete the record by user 2
        response = self.client.delete('/api/v2/intervention/1',
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
        # post 1 record
        self.client.post('/api/v2/intervention',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})
        # patch the record by the same user
        response = self.client.patch('/api/v2/intervention/1/comment',
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
        # post 1 record by user 1
        self.client.post('/api/v2/intervention',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})
        # signup user 2
        response = self.client.post("api/v2/auth/signup",
                                    data=json.dumps(sign_up_data_2),
                                    content_type='application/json')

        # login the user 2 to get the token
        login_response = self.client.post('/api/v2/auth/login',
                                          data=json.dumps(sign_in_data_2),
                                          content_type='application/json')
        login_result = json.loads(login_response.data)
        token2 = login_result['data'][0]['token']
        # patch the record by user 2
        response = self.client.patch('/api/v2/intervention/1/comment',
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
        # post 1 incident record
        self.client.post('/api/v2/intervention',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})
        # patch the record
        response = self.client.patch('/api/v2/intervention/1/location',
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
        self.client.post('/api/v2/intervention',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})
        # signup user 2
        response = self.client.post("api/v2/auth/signup",
                                    data=json.dumps(sign_up_data_2),
                                    content_type='application/json')
        print(response.data)
        # login the user 2 to get the token
        login_response = self.client.post('/api/v2/auth/login',
                                          data=json.dumps(sign_in_data_2),
                                          content_type='application/json')
        login_result = json.loads(login_response.data)
        print(login_result)
        token2 = login_result['data'][0]['token']
        # patch the record
        response = self.client.patch('/api/v2/intervention/1/location',
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
        # post 1 record by user
        self.client.post('/api/v2/intervention',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})
        # patch the record
        response = self.client.patch('/api/v2/intervention/1/comment',
                                     data=json.dumps(invalid_comment_data),
                                     headers={'Authorization': 'Bearer ' +
                                              self.token, 'content-type':
                                              'application/json'})
        # assert
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertEqual(result['message'],
                         'A comment cannot contain special characters e.g $ '
                         'or empty space'
                         )

    def test_throws_error_on_patch_invalid_location(self):
        """test cant edit location with wrong data"""
        # post 1 record by user
        self.client.post('/api/v2/intervention',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})
        # patch the record
        response = self.client.patch('/api/v2/intervention/1/location',
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
        # post 1 incident
        self.client.post('/api/v2/intervention',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})

        # admin patch
        response = self.client.patch('/api/v2/intervention/1/status',
                                     data=json.dumps(admin_status_change),
                                     headers={'Authorization': 'Bearer ' +
                                              self.admin_token, 'content-type':
                                              'application/json'})
        # assert
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result['status'], 200)

    def test_comment_cant_be_edited_by_user_after_admin_status_change(self):
        """test user can't change status after status change"""
        # post 1 by user
        self.client.post('/api/v2/intervention',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})

        # admin patch
        response1 = self.client.patch('/api/v2/intervention/1/status',
                                      data=json.dumps(admin_status_change),
                                      headers={'Authorization': 'Bearer ' +
                                               self.admin_token,
                                               'content-type':
                                               'application/json'})
        # user patch
        response = self.client.patch('/api/v2/intervention/1/comment',
                                     data=json.dumps(edit_comment_data),
                                     headers={'Authorization': 'Bearer ' +
                                              self.token, 'content-type':
                                              'application/json'})
        print(response.data)
        # assert
        self.assertEqual(response.status_code, 403)
        result = json.loads(response.data)
        self.assertEqual(result['message'],
                         'You can not edit this record, it is already resolved'
                         )

    def test_location_cant_be_edited_by_user_after_admin_status_change(self):
        """test user can't change status after status change"""
        # post 1 record by user
        self.client.post('/api/v2/intervention',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})

        # admin patch
        response = self.client.patch('/api/v2/intervention/1/status',
                                     data=json.dumps(admin_status_change),
                                     headers={'Authorization': 'Bearer ' +
                                              self.admin_token, 'content-type':
                                              'application/json'})
        # user patch
        response = self.client.patch('/api/v2/intervention/1/location',
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
        # post 1 record by user
        self.client.post('/api/v2/intervention',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})

        # admin patch
        response = self.client.patch('/api/v2/intervention/1/status',
                                     data=json.dumps(admin_status_change),
                                     headers={'Authorization': 'Bearer ' +
                                              self.admin_token, 'content-type':
                                              'application/json'})
        # user try to delete the record
        response = self.client.delete('/api/v2/intervention/1/',
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
        # post 1 record by user
        self.client.post('/api/v2/intervention',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})
        # enter non digit id and patch
        response = self.client.patch('/api/v2/intervention/s/comment',
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

    def test_edit_location_on_non_digit_id(self):
        """test throws error on non digit ID"""
        # post 1 record by user
        self.client.post('/api/v2/intervention',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})
        # enter non digit id and patch
        response = self.client.patch('/api/v2/intervention/s/location',
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

    def test_returns_error_on_deleting_non_existent(self):
        """test for deleting a record which is non existent"""
        # delete a non existent
        response = self.client.delete('/api/v2/intervention/333',
                                      headers={'Authorization': 'Bearer ' +
                                               self.token, 'content-type':
                                               'application/json'})
        # assert
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data)
        self.assertEqual(result['message'],
                         'This intervention record does not exist'
                         )

    def test_returns_error_on_updating_non_existent_incident_comment(self):
        """test for editing record comment which is non existent"""
        # patch non existent record
        response = self.client.patch('/api/v2/intervention/333/comment',
                                     data=json.dumps(edit_comment_data),
                                     headers={'Authorization': 'Bearer ' +
                                              self.token, 'content-type':
                                              'application/json'})
        # assert
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data)
        self.assertEqual(result['message'],
                         'This intervention record does not exist'
                         )

    def test_returns_error_on_updating_non_existent_incident_location(self):
        """test for editing record comment which is non existent"""
        # update a record not available
        response = self.client.patch('/api/v2/intervention/333/location',
                                     data=json.dumps(edit_location_data),
                                     headers={'Authorization': 'Bearer ' +
                                              self.token, 'content-type':
                                              'application/json'})
        # assert
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data)
        self.assertEqual(result['message'],
                         'This intervention record does not exist'
                         )

    def test_admin_cannot_change_status_to_invalid(self):
        """test that admin cannot change status to invalid one"""
        # post 1 record by user
        self.client.post('/api/v2/intervention',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})

        # admin try to patch the record
        response = self.client.patch('/api/v2/intervention/1/status',
                                     data=json.dumps(invalid_status),
                                     headers={'Authorization': 'Bearer ' +
                                              self.admin_token, 'content-type':
                                              'application/json'})
        # assert
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertEqual(result['message'],
                         'Status can only be resolved, rejected or an '
                         'under investigation'
                         )

    def test_admin_cannot_change_status_for_non_existent(self):
        """test throws error on status change for non existent record"""

        # admin patch
        response = self.client.patch('/api/v2/intervention/333/status',
                                     data=json.dumps(admin_status_change),
                                     headers={'Authorization': 'Bearer ' +
                                              self.admin_token, 'content-type':
                                              'application/json'})
        # assert
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data)
        self.assertEqual(result['message'],
                         'This intervention record does not exist')

    def test_non_admin_cannot_change_status(self):
        """test throws error on status change for non existent record"""
        # post 1 record by user
        self.client.post('/api/v2/intervention',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})

        # normal user patch
        response = self.client.patch('/api/v2/intervention/1/status',
                                     data=json.dumps(admin_status_change),
                                     headers={'Authorization': 'Bearer ' +
                                              self.token, 'content-type':
                                              'application/json'})
        # assert
        self.assertEqual(response.status_code, 403)
        result = json.loads(response.data)
        self.assertEqual(result['message'],
                         'This action is only allowed to admins')

    def test_throws_error_on_patch_invalid_comment_id(self):
        """test cant edit comment with invalid id"""
        # post 1 incident record
        self.client.post('/api/v2/intervention',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})
        # patch the record
        response = self.client.patch('/api/v2/intervention/fhgfhg/comment',
                                     data=json.dumps(invalid_comment_data),
                                     headers={'Authorization': 'Bearer ' +
                                              self.token, 'content-type':
                                              'application/json'})
        # assert
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertEqual(result['message'],
                         'intervention ID fhgfhg is invalid')

    def test_throws_error_on_invalid_id_for_status(self):
        """test for invalid id entered to change status"""
        # admin patchusing invalid ID
        response = self.client.patch('/api/v2/intervention/hgfgf/status',
                                     data=json.dumps(invalid_status),
                                     headers={'Authorization': 'Bearer ' +
                                              self.admin_token, 'content-type':
                                              'application/json'})
        # assert
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertEqual(result['message'],
                         'intervention ID hgfgf is invalid')

    def test_can_make_admin(self):
        """test that admin can promote user to admin"""
        response = self.client.patch('/api/v2/makeadmin/1',
                                     headers={'Authorization': 'Bearer ' +
                                              self.admin_token, 'content-type':
                                              'application/json'})
        result = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(result['message'], 'Successfully promoted user '
                         'with ID 1 to admin')

    def test_when_id_is_invalid(self):
        """test that cant promote nonexistent user"""
        response = self.client.patch('/api/v2/makeadmin/333',
                                     headers={'Authorization': 'Bearer ' +
                                              self.admin_token, 'content-type':
                                              'application/json'})
        result = json.loads(response.data)
        self.assertEqual(404, response.status_code)
        self.assertEqual(result['message'], 'This user does not exist'
                         )

    def test_when_id_is_non_digit(self):
        """test that cant promote nonexistent user"""
        response = self.client.patch('/api/v2/makeadmin/invalid',
                                     headers={'Authorization': 'Bearer ' +
                                              self.admin_token, 'content-type':
                                              'application/json'})
        result = json.loads(response.data)
        self.assertEqual(400, response.status_code)
        self.assertEqual(result['message'], 'ID invalid is invalid')

    def test_when_post_with_invalid_type(self):
        """test throws error on invalid type"""

        response = self.client.post('/api/v2/interv',
                                    data=json.dumps(new_incident_data),
                                    headers={'Authorization': 'Bearer ' +
                                             self.token, 'content-type':
                                             'application/json'})
        result = json.loads(response.data)
        self.assertEqual(result['status'], 400)
        self.assertEqual(response.status_code, 400)

    def test_get_all_with_invalid_type(self):
        """test throws error on invalid type"""

        response = self.client.get('/api/v2/invalid',
                                   headers={'Authorization': 'Bearer ' +
                                            self.token, 'content-type':
                                            'application/json'})
        result = json.loads(response.data)
        self.assertEqual(result['status'], 400)
        self.assertEqual(response.status_code, 400)

    def test_get_one_with_invalid_type(self):
        """test throws error on invalid type"""

        response = self.client.get('/api/v2/invalid/1',
                                   headers={'Authorization': 'Bearer ' +
                                            self.token, 'content-type':
                                            'application/json'})
        result = json.loads(response.data)
        self.assertEqual(result['status'], 400)
        self.assertEqual(response.status_code, 400)

    def test_when_patch_comment_with_invalid_type(self):
        """test throws error on invalid type"""

        response = self.client.get('/api/v2/invalid/comment',
                                   data=json.dumps(edit_comment_data),
                                   headers={'Authorization': 'Bearer ' +
                                            self.token, 'content-type':
                                            'application/json'})
        result = json.loads(response.data)
        self.assertEqual(result['status'], 400)
        self.assertEqual(response.status_code, 400)

    def test_when_patch_location_with_invalid_type(self):
        """test throws error on invalid type"""

        response = self.client.get('/api/v2/invalid/location',
                                   data=json.dumps(edit_location_data),
                                   headers={'Authorization': 'Bearer ' +
                                            self.token, 'content-type':
                                            'application/json'})
        result = json.loads(response.data)
        self.assertEqual(result['status'], 400)
        self.assertEqual(response.status_code, 400)

    def test_change_status_with_invalid_url(self):
        """test that admin can't change change status with invalid url"""
        # post 1 incident record
        self.client.post('/api/v2/intervention',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.token, 'content-type':
                                  'application/json'})

        # admin patch
        response = self.client.patch('/api/v2/notreal/1/status',
                                     data=json.dumps(admin_status_change),
                                     headers={'Authorization': 'Bearer ' +
                                              self.admin_token, 'content-type':
                                              'application/json'})
        # assert
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertEqual(result['status'], 400)

    def test_delete_with_invalid_url(self):
        """test can't delete with invalid url"""
        response = self.client.delete('/api/v2/invalid/1',
                                      data=json.dumps(edit_location_data),
                                      headers={'Authorization': 'Bearer ' +
                                               self.token, 'content-type':
                                               'application/json'})
        result = json.loads(response.data)
        self.assertEqual(result['status'], 400)
        self.assertEqual(response.status_code, 400)

    def test_make_admin_normal_user(self):
        """test that normal user cannot promote another user"""
        response = self.client.patch('/api/v2/makeadmin/1',
                                     headers={'Authorization': 'Bearer ' +
                                              self.token, 'content-type':
                                              'application/json'})
        result = json.loads(response.data)
        self.assertEqual(403, response.status_code)
        self.assertEqual(result['message'],
                         'This action is only allowed to admins')

    def test_gets_all_users(self):
        """test that can fetch all the user records"""
        self.client.post(
            "api/v2/auth/signup",
            data=json.dumps(sign_up_data),
            content_type='application/json')
        # fetch
        response = self.client.get('/api/v2/users',
                                   headers={'Authorization': 'Bearer ' +
                                            self.admin_token, 'content-type':
                                            'application/json'})
        result = json.loads(response.data)
        self.assertEqual(result['status'], 200)
        self.assertEqual(response.status_code, 200)

    def test_gets_users_one(self):
        """test that can fetch all the user records"""
        # fetch
        response = self.client.get('/api/v2/users/profile',
                                   headers={'Authorization': 'Bearer ' +
                                            self.admin_token, 'content-type':
                                            'application/json'})
        result = json.loads(response.data)
        self.assertEqual(result['status'], 200)
        self.assertEqual(response.status_code, 200)

    def test_count(self):
        """test can return record count"""
        response = self.client.get('/api/v2/user/red-flag/draft',
                                   headers={'Authorization': 'Bearer ' +
                                            self.admin_token, 'content-type':
                                            'application/json'})
        result = json.loads(response.data)
        self.assertEqual(result['status'], 200)
        self.assertEqual(response.status_code, 200)

    def test_get_empty_user_records(self):
        """test getting user records"""
        response = self.client.get('/api/v2/user/red-flag',
                                   headers={'Authorization': 'Bearer ' +
                                            self.admin_token, 'content-type':
                                            'application/json'})
        result = json.loads(response.data)
        self.assertEqual(result['status'], 404)
        self.assertEqual(response.status_code, 404)

    def test_get_user_records(self):
        """test getting user records"""
        self.client.post('/api/v2/intervention',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.admin_token, 'content-type':
                                  'application/json'})

        response = self.client.get('/api/v2/user/intervention',
                                   headers={'Authorization': 'Bearer ' +
                                            self.admin_token, 'content-type':
                                            'application/json'})
        result = json.loads(response.data)
        self.assertEqual(result['status'], 200)
        self.assertEqual(response.status_code, 200)

    def test_admin_cant_change_own_record_status(self):
        """test that admin can change status"""
        # post 1 incident
        self.client.post('/api/v2/intervention',
                         data=json.dumps(new_incident_data),
                         headers={'Authorization': 'Bearer ' +
                                  self.admin_token, 'content-type':
                                  'application/json'})

        # admin patch
        response = self.client.patch('/api/v2/intervention/1/status',
                                     data=json.dumps(admin_status_change),
                                     headers={'Authorization': 'Bearer ' +
                                              self.admin_token, 'content-type':
                                              'application/json'})
        # assert
        self.assertEqual(response.status_code, 403)
        result = json.loads(response.data)
        self.assertEqual(result['status'], 403)
