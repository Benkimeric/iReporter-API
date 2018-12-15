# valid sign up data
sign_up_data = {
        "first_name": "Benkim",
        "last_name": "Eric",
        "other_names": "Kimeu",
        "phone_number": "0727423912",
        "user_name": "larry",
        "email": "benkimeric@gmail.com",
        "password": "Us7cgsTsben$",
        "confirm_password": "Us7cgsTsben$"
}

sign_up_data_2 = {
        "first_name": "Benkim",
        "last_name": "Eric",
        "other_names": "Kimeu",
        "phone_number": "0727423916",
        "user_name": "benk2",
        "email": "alexkimeu1999@gmail.com",
        "password": "Us7cgsTsben$",
        "confirm_password": "Us7cgsTsben$"
}

admin_sign_in = {
    "user_name": "admin",
    "password": "admin@123"
}

# valid sign in data from valid sign up
sign_in_data = {
        "user_name": "larry",
        "password": "Us7cgsTsben$"
}

sign_in_data_2 = {
        "user_name": "benk2",
        "password": "Us7cgsTsben$"
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

invalid_status = {
    "status": "simply invalid"
}
