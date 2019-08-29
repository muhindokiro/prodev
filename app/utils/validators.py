import re

# class Validate():
#     """
#     Class with Functions to validate inputs
#     """
def validate_email(email):
    """
    Function to validate an email address
    """
    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
        return False
    return True

def check_space(mystring):
    """
    Function for validating whitespaces/blanks
    """
    if mystring and mystring.strip():
        return True
    else:
        return False

def validate_username(username):
    """
    Function to validate a username
    """
    if not re.match(r"^[A-Za-z\.\+_-]*$", username):
        return False
    return True

def validate_age(age):
    """
    Function to validate a user's age
    """
    if not len(str(age)) == 2:
        return False
    return True

def validate_education(education):
    """
    Function to validate the user's education
    """
    # qualification = 'Diploma Certificate Degree '
    qualification = r'\b' + 'Diploma' + r'\b' 
    qualification2 = r'\b' + 'Certificate' + r'\b' 
    qualification3 = r'\b' + 'Degree' + r'\b'
    if not re.findall(qualification,education):
        if not re.findall(qualification2,education):
            if not re.findall(qualification3,education):
                return False
            return True
        return True
    return True

def check_password(password):
    """
    Method for checking the user's password
    """
    if re.match(r"[A-Za-z0-9@#$%^&+=]{8,}", password) != None:
        return True
    else:
        return False
 
def validate_location(location):
    """
    Function to validate a user's location
    """
    if not re.match(r"^[A-Za-z0-9\.\+_-]*$", location):
        return False
    return True

def validate_NationalID(NationalID):
    """
    Function to validate the user's NationalID
    """
    if not len(str(NationalID)) == 8:
        return False
    return True

def validate_occupation(occupation):
    """
    Function to validate the user's occupation
    """
    # works = ['Employed','Unemployed','Retired']
    works = r'\b' + 'Employed' + r'\b' 
    works2 = r'\b' + 'Unemployed' + r'\b' 
    if not re.findall(works,occupation):
        if not re.findall(works2,occupation):
            return False
        return True
    return True

def validate_title(title):
    if not re.match(r"^[A-Za-z\.\+_-]*$", title):
        return False
    return True

def validate_responsibility(responsibility):
    if not re.match(r"^[A-Za-z\.\+_-]*$",responsibility):
        return False
    return True

def validate_company(company):
    if not re.match(r"^[A-Za-z0-9\.\+_-]*$", company):
        return False
    return True

def validate_salary(salary):
    regnumber = re.compile(r'\d+')
    if not regnumber.match(salary):
        return False
    return True

def validate_category(category):
    """
    Function to validate the job's category
    """
    # qualification = 'Diploma Certificate Degree '
    cat = r'\b' + 'Engineering' + r'\b' 
    cat2 = r'\b' + 'Medicine' + r'\b' 
    cat3 = r'\b' + 'Theology' + r'\b'
    cat4 = r'\b' + 'Business' + r'\b'
    cat5 = r'\b' + 'Hospitality' + r'\b'
    cat6 = r'\b' + 'Computer Science' + r'\b'
    if not re.findall(cat,category):
        if not re.findall(cat2,category):
            if not re.findall(cat3,category):
                if not re.findall(cat4,category):
                    if not re.findall(cat5,category):
                        if not re.findall(cat5,category):
                            return False
                        return True
                    return True
                return True
            return True
        return True
    return True

def validate_status(status_data):
    """
    Function to validate the status input
    """
    status = r'\b' + 'Apply' + r'\b' 
    status2 = r'\b' + 'Cancel' + r'\b'
    status3 = r'\b' + 'Approve' + r'\b' 
    if not re.findall(status,status_data):
        if not re.findall(status2,status_data):
            if not re.findall(status3,status_data):
                return False
            return True
        return True
    return True