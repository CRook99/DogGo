import re


def validateEmail(email):
    return not (re.search(r"[^@]{1,64}@[^@]{1,253}\.[^@]{2,}", email) is None)
    # Regex expression to check whether submitted email follows conventions
    # [^@]{1,64} finds a recipient name of maximum 64 characters
    # @ finds the required @ symbol that separates the name and domain
    # [^@]{1,253} finds a domain of maximum 253 characters
    # \. finds the required . symbol that separates the domain and top-level domain
    # [^@]{2,} finds the top-level domain of minimum 2 characters


def validatePassword(password):
    valid = True
    if ((re.search(r"\d", password) is None) or (re.search(r"(?=.*[A-Z])", password) is None) or (re.search(r"^.{8,32}$", password) is None)):
        valid = False
    return valid


def validateTel(tel):
    tel = tel.replace(' ','') # Removes whitespace
    return not (re.search(r"^0[0-9]{10}$", tel) is None)


def matchPasswords(password, confirmPassword):
    return password == confirmPassword # Returns whether the first password and the confirmation password match


def validateDogName(name):
    return 1 <= len(name) <= 20 and name != None


def validateBreedName(breed):
    return 1 <= len(breed) <= 50 and breed != None


def validateAge(age):
    return 1 <= int(age) <= 20 and age != None


def validateSex(sex):
    return (sex == "M" or sex == "F") and sex != None


def validateLocation(location):
    if location == None:
        return False
    return 1 <= len(location) <= 50
