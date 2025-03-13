# password_validator.py

# Custom Password Validation Function

def password_check(passwd):
    """
    Validates a password based on the following rules:
    - At least 6 characters
    - No more than 20 characters
    - At least one digit
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one special symbol ($, @, #, %)
    
    Returns:
        list: Errors found in the password (empty list if valid)
    """
    special_symbols = {'$', '@', '#', '%'}
    errors = []

    if len(passwd) < 6:
        errors.append("Password should be at least 6 characters long.")
    
    if len(passwd) > 20:
        errors.append("Password should not be longer than 20 characters.")

    if not any(char.isdigit() for char in passwd):
        errors.append("Password should have at least one numeral.")

    if not any(char.isupper() for char in passwd):
        errors.append("Password should have at least one uppercase letter.")

    if not any(char.islower() for char in passwd):
        errors.append("Password should have at least one lowercase letter.")

    if not any(char in special_symbols for char in passwd):
        errors.append("Password should have at least one special symbol ($, @, #, %).")

    return errors

# Test
if __name__ == "__main__":
    password = "Geek12@"
    result = password_check(password)

    if not result:
        print("Password is valid")
    else:
        print("Invalid Password:\n" + "\n".join(result))
