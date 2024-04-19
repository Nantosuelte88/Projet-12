import click
from controllers.auth_permissions import authorize
from controllers.collaborator_crud import create_collaborator, update_collaborator, delete_collaborator


@click.group()
def collaborator_commands():
    pass


@collaborator_commands.command()
@click.pass_context
def create_collaborator_command(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant de créer un collaborateur.")
        return
    create_collaborator(token)


@collaborator_commands.command()
@click.pass_context
def update_collaborator_command(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant de modifier un collaborateur.")
        return
    update_collaborator(token)


@collaborator_commands.command()
@click.pass_context
def delete_collaborator_command(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant de supprimer un collaborateur.")
        return
    delete_collaborator(token)
