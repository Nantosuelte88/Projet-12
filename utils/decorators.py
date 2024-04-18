from controllers.auth_permissions import authorize
from utils.get_object import get_id_by_token
from controllers.auth_permissions import verify_department

COMMERCIAL = 3
GESTION = 2
SUPPORT = 1


def user_authorized(department_id):
    def decorator(func):
        def wrapper(token, *args, **kwargs):
            if token:
                authorized = authorize(token, department_id)
                if authorized:
                    return func(token, *args, **kwargs)
                else:
                    print("Autorisation refusée pour ce département")
            else:
                print("Utilisateur non connecté")
        return wrapper
    return decorator


def permission_for_commercial_department():
    def decorator(func):
        def wrapper(token, *args, **kwargs):
            if token:
                authorized = verify_department(token, COMMERCIAL)
                if authorized:
                    return func(token, *args, **kwargs)
                else:
                    print('Seul le département Commercial est autorisé à accéder à cette fonctionnalité.')
            else:
                print("Utilisateur non connecté")
        return wrapper
    return decorator


def permission_for_gestion_department():
    def decorator(func):
        def wrapper(token, *args, **kwargs):
            if token:
                authorized = verify_department(token, GESTION)
                if authorized:
                    return func(token, *args, **kwargs)
                    
                else:
                    print('Seul le département Gestion est autorisé à accéder à cette fonctionnalité.')
            else:
                print("Utilisateur non connecté")
        return wrapper
    return decorator

def permission_for_support_department():
    def decorator(func):
        def wrapper(token, *args, **kwargs):
            if token:
                authorized = verify_department(token, SUPPORT)
                if authorized:
                    return func(token, *args, **kwargs)
                else:
                    print('Seul le département Support est autorisé à accéder à cette fonctionnalité.')
            else:
                print("Utilisateur non connecté")
        return wrapper
    return decorator

def permission_commercial_or_gestion():
    def decorator(func):
        def wrapper(token, *args, **kwargs):
            if token:
                authorized = verify_department(token, GESTION)
                if authorized:
                    return func(token, *args, **kwargs)
                else:
                    authorized = verify_department(token, COMMERCIAL)
                    if authorized:
                        return func(token, *args, **kwargs)
                    else:
                        # commerciaux ???
                        print('Seul les départements Gestion et Commercial sont autorisés à accéder à cette fonctionnalité.')
            else:
                print("Utilisateur non connecté")
        return wrapper
    return decorator

