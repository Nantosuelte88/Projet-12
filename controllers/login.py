import getpass
import click
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta, timezone
from connect_database import create_db_connection
from models.collaboration import Collaborator
from controllers.auth_permissions import authenticate, authorize
from utils.input_validators import is_valid_email, is_valid_password
from views.view_login import view_login

@click.command()
@click.pass_context
def login(ctx):
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

