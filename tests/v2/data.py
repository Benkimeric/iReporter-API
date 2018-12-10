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

# valid sign in data from valid sign up
sign_in_data = {
        "user_name": "benk",
        "password": "qwerty12"
}

# sign in data with wrong username
invalid_username = {
        "user_name": "invalid",
        "password": "qwerty12"
}

# sign in data with wrong password
wrong_phone = {
        "user_name": "benk",
        "password": "wrong"
}


# wrong email
sign_up_data_fake_email = {
        "first_name": "Benkim",
        "last_name": "Eric",
        "other_names": "Kimeu",
        "phone_number": "+254727423949",
        "user_name": "benk",
        "email": "invalid",
        "password": "qwerty12"
}

# wrong phone
sign_up_invalid_phone = {
        "first_name": "Benkim",
        "last_name": "Eric",
        "other_names": "Kimeu",
        "phone_number": "+5464",
        "user_name": "benk",
        "email": "valid@gmail.com",
        "password": "qwerty12"
}

invalid_f_name = {
        "first_name": "1234",
        "last_name": "Eric",
        "other_names": "Kimeu",
        "phone_number": "+254727423949",
        "user_name": "benk",
        "email": "valid@gmail.com",
        "password": "qwerty12"
}

invalid_l_name = {
        "first_name": "Benkim",
        "last_name": "343",
        "other_names": "Eric",
        "phone_number": "+254727423949",
        "user_name": "benk",
        "email": "valid@gmail.com",
        "password": "qwerty12"
}

invalid_o_name = {
        "first_name": "Benkim",
        "last_name": "Eric",
        "other_names": "#$565",
        "phone_number": "+254727423949",
        "user_name": "benk",
        "email": "valid@gmail.com",
        "password": "qwerty12"
}

existing_phone = {
        "first_name": "Benkim",
        "last_name": "Eric",
        "other_names": "Kimeu",
        "phone_number": "+254727423939",
        "user_name": "newusername",
        "email": "newmail@benkim.com",
        "password": "qwerty12"
}

existing_email = {
        "first_name": "Benkim",
        "last_name": "Eric",
        "other_names": "Kimeu",
        "phone_number": "+254727423239",
        "user_name": "bena",
        "email": "benk@benkim.com",
        "password": "qwerty12"
}
