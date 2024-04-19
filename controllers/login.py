import click
from controllers.auth_permissions import authenticate, authorize
from views.view_login import view_login


@click.command()
@click.pass_context
def login(ctx):
    """
    Authentifie un utilisateur et stocke le token d'authentification dans le contexte.
    """
    checked = False
    authorized = False
    info_user = view_login(checked, authorized)
    if info_user:
        email = info_user[0]
        password = info_user[1]
        token = authenticate(email, password)
        if token:
            authorized = authorize(token)
            if authorized:
                checked = True
                ctx.obj["token"] = token
                info_user = view_login(checked, authorized)
