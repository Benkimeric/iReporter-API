# valid sign up data
sign_up_data = {
        "first_name": "Benkim",
        "last_name": "Eric",
        "other_names": "Kimeu",
        "phone_number": "+254727423939",
        "user_name": "benk",
        "email": "benk@benkim.com",
        "password": "qwerty12"
}

sign_up_data_2 = {
        "first_name": "Benkim",
        "last_name": "Eric",
        "other_names": "Kimeu",
        "phone_number": "+254727423966",
        "user_name": "benk2",
        "email": "benk2@benkim.com",
        "password": "qwerty122"
}

admin_sign_in = {
    "user_name": "admin",
    "password": "admin@123"
}

# valid sign in data from valid sign up
sign_in_data = {
        "user_name": "benk",
        "password": "qwerty12"
}

sign_in_data_2 = {
        "user_name": "benk2",
        "password": "qwerty122"
}

# valid incident data
new_incident_data = {
    "comment": "new corruption",
    "record_type": "intervention",
    "location": "10.0123, -34.034"
}

# invalid comment data
invalid_comment = {
    "comment": "@#$@#",
    "record_type": "intervention",
    "location": "10.0123, -34.034"
}

invalid_location = {
    "comment": "new corruption",
    "record_type": "intervention",
    "location": "1345670.0123, -32345674.034"
}

invalid_type = {
    "comment": "new corruption",
    "record_type": "invalid",
    "location": "10.0123, -34.034"
}

edit_comment_data = {
    "comment": "New edited comment",
}

edit_location_data = {
    "location": "34.4656, 56.3243",
}
invalid_comment_data = {
    "comment": "@#$@#",
}

invalid_location_data = {
    "location": "invalid",
}
admin_status_change = {
    "status": "resolved"
}
