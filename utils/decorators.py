from controllers.auth_permissions import authorize
from utils.get_object import get_id_by_token


def department_permission_required(department_id):
    def decorator(func):
        def wrapper(token, *args, **kwargs):
            if token:
                authorized = authorize(token, department_id)
                if authorized:
                    return func(token, *args, **kwargs)
                else:
                    print("Dans le decorateur")
                    print("Autorisation refusée pour ce département")
            else:
                print("Utilisateur non connecté")
        return wrapper
    return decorator


