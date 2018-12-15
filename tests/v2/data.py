# valid sign up data
sign_up_data = {
        "first_name": "Benkim",
        "last_name": "Eric",
        "other_names": "Kimeu",
        "phone_number": "0727423939",
        "user_name": "benk",
        "email": "benkimeric@gmail.com",
        "password": "Us7cgsTsben$",
        "confirm_password": "Us7cgsTsben$"
}

# valid sign in data from valid sign up
sign_in_data = {
        "user_name": "benk",
        "password": "Us7cgsTsben$"
}

# sign in data with wrong username
invalid_username = {
        "user_name": "invalid",
        "password": "Us7cgsTsben$"
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
        "phone_number": "0727423939",
        "user_name": "benk",
        "email": "invalid",
        "password": "Us7cgsTsben$",
        "confirm_password": "Us7cgsTsben$"
}
# invalid username
wrong_username = {
        "first_name": "Benkim",
        "last_name": "Eric",
        "other_names": "Kimeu",
        "phone_number": "0727423939",
        "user_name": "  ",
        "email": "benkimeric@gmail.com",
        "password": "Us7cgsTsben$",
        "confirm_password": "Us7cgsTsben$"
}

# wrong phone
sign_up_invalid_phone = {
        "first_name": "Benkim",
        "last_name": "Eric",
        "other_names": "Kimeu",
        "phone_number": "+5464",
        "user_name": "benk",
        "email": "benkimeric@gmail.com",
        "password": "Us7cgsTsben$",
        "confirm_password": "Us7cgsTsben$"
}

invalid_f_name = {
        "first_name": "1234",
        "last_name": "Eric",
        "other_names": "Kimeu",
        "phone_number": "0727423939",
        "user_name": "benk",
        "email": "benkimeric@gmail.com",
        "password": "Us7cgsTsben$",
        "confirm_password": "Us7cgsTsben$"
}

invalid_l_name = {
        "first_name": "Benkim",
        "last_name": "343",
        "other_names": "Eric",
        "phone_number": "0727423939",
        "user_name": "benk",
        "email": "benkimeric@gmail.com",
        "password": "Us7cgsTsben$",
        "confirm_password": "Us7cgsTsben$"
}

invalid_o_name = {
        "first_name": "Benkim",
        "last_name": "Eric",
        "other_names": "#$565",
        "phone_number": "0727423939",
        "user_name": "benk",
        "email": "benkimeric@gmail.com",
        "password": "Us7cgsTsben$",
        "confirm_password": "Us7cgsTsben$"
}

existing_phone = {
        "first_name": "Benkim",
        "last_name": "Eric",
        "other_names": "Kimeu",
        "phone_number": "0727423939",
        "user_name": "newusername",
        "email": "alexkimeu1999@gmail.com",
        "password": "Us7cgsTsben$",
        "confirm_password": "Us7cgsTsben$"
}

existing_email = {
        "first_name": "Benkim",
        "last_name": "Eric",
        "other_names": "Kimeu",
        "phone_number": "0727423939",
        "user_name": "bena",
        "email": "benkimeric@gmail.com",
        "password": "Us7cgsTsben$",
        "confirm_password": "Us7cgsTsben$"
}

password_data = {
        "first_name": "Benkim",
        "last_name": "Eric",
        "other_names": "Kimeu",
        "phone_number": "0727423939",
        "user_name": "benk",
        "email": "benkimeric@gmail.com",
        "password": "invalid",
        "confirm_password": "invalid"
}

sign_with_no_match_password = {
        "first_name": "Benkim",
        "last_name": "Eric",
        "other_names": "Kimeu",
        "phone_number": "0727423939",
        "user_name": "benk",
        "email": "benkimeric@gmail.com",
        "password": "Us7cgsTsben$",
        "confirm_password": "noMatch@123Y$"
}
