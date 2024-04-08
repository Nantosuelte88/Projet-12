from controllers.auth_permissions import authorize


def department_permission_required(department_id):
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
