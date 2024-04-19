import click
from controllers.auth_permissions import authorize
from controllers.client_crud import display_all_clients, delete_client, display_my_clients, create_new_client, update_client


@click.group()
def client_commands():
    pass


@client_commands.command()
@click.pass_context
def view_clients(ctx):
    token = ctx.obj["token"]
    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant d'afficher les clients.")
        return
    display_all_clients(token)


@client_commands.command()
@click.pass_context
def view_my_clients(ctx):
    token = ctx.obj["token"]
    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant d'afficher les clients qui vous sont associés.")
        return
    display_my_clients(token)


@client_commands.command()
@click.pass_context
def create_client_command(ctx):
    token = ctx.obj["token"]
    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant de créer un nouvel utilisateur.")
        return
    create_new_client(token)


@client_commands.command()
@click.pass_context
def update_client_command(ctx):
    token = ctx.obj["token"]
    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant de modifier un utilisateur.")
        return
    update_client(token)


@client_commands.command()
@click.pass_context
def delete_client_command(ctx):
    token = ctx.obj["token"]
    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant de supprimer un utilisateur.")
        return
    delete_client(token)
