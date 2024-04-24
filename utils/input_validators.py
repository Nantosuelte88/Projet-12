import re
import datetime

def is_valid_email(email):
    """
    Vérifie si l'email est valide en utilisant une expression régulière
    """
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None


def is_valid_password(password):
    """
    Vérifie si le mot de passe est valide
    """
    # Personnaliser la création du mot de passe
    if len(password) < 10:
        return False

    return True


def is_valid_phone_number(phone_number):
    """
    Vérifie si le numéro de téléphone est valide
    """
    # Personnaliser les numéros de téléphone, ajustez selon les pays des clients etc
    pattern = r'^[\d\s+]+$'
    if len(phone_number) > 10:
        return False
    else:
        return True


def is_valid_money_format(value):
    pattern = r'^[0-9]+(?:\.[0-9]+)?$'
    return re.match(pattern, value) is not None


def is_valid_date_format(date_string):
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False
