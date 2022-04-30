import re


def validateEmail(email):
    '''
        Regex expression to check whether submitted email follows conventions
        [^@]{1,64} finds a recipient name of maximum 64 characters
        @ finds the required @ symbol that separates the name and domain
        [^@]{1,253} finds a domain of maximum 253 characters
        \. finds the required . symbol that separates the domain and top-level domain
        [^@]{2,} finds the top-level domain of minimum 2 characters
    '''

    return not (re.search(r"[^@]{1,64}@[^@]{1,253}\.[^@]{2,}", email) is None)





def validatePassword(password):
    valid = True

    '''
    First expression decides if a digit is present
    Second expression decides if an uppercase character is present
    Third expression decides if the password is between 8-32 characters long
    '''

    if (re.search(r"\d", password) is None) or (re.search(r"(?=.*[A-Z])", password) is None) or (re.search(r"^.{8,32}$", password) is None):
        valid = False
    return valid




def validateTel(tel):
    tel = tel.replace(' ','') # Removes whitespace
    return not (re.search(r"^0[0-9]{10}$", tel) is None)


def matchPasswords(password, confirmPassword):
    return password == confirmPassword

    # Returns whether the first password and the confirmation password match


def validateName(name):
    return 1 <= len(name) <= 20 and name != None


def validateAge(age):
    try:
        age = int(age)
    except:
        return False

    # Returns false if input is not an integer

    return 1 <= int(age) <= 20


def validateSex(sex):
    return (sex == "M" or sex == "F") and sex != None


def validateBreed(breed):
    return 1 <= len(breed) <= 50 and breed != None


def validateLocation(location):
    if location == None:
        return False
    return 1 <= len(location) <= 50
