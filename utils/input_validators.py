import re


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
    # Exemple de règles de validation du mot de passe
    if len(password) < 10:
        return False

    return True

def is_valid_phone_number(phone_number):
    """
    Vérifie si le numéro de téléphone est valide
    """
    pattern = r'^[\d\s+]+$'
    if re.match(pattern, phone_number) is None:
        return False
    elif len(phone_number) > 10:
        return False
    else:
        return True