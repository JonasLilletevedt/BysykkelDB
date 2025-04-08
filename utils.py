# Checks if username is valid
# name should only contain letters
def check_valid_name(name):
    if len(name) == 0:
        return False
    letters = "abcdefghijklmnopqrstuvwxyz"
    for c in name.lower():
        if c not in letters:
            return False
    return True

# Checks if phonenumber is valid
# phonenumber should be exactly 9 digits and only contain digits
def check_phone_number(phone_number):
    phone_number = str(phone_number)

    if len(phone_number) != 8:
        return False
    
    digits = "0123456789"
    for d in phone_number:
        if d not in digits:
            return False
    return True


# Checks if email is valid
# email should contain '@'
def check_valid_email(email):
    return '@' in email
