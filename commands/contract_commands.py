import click
from controllers.auth_permissions import authenticate, authorize
from controllers.contract_crud import display_all_contracts, display_contracts_unpaid, display_unsigned_contracts, create_contract, update_contract, delete_contract


@click.group()
def contract_commands():
    pass

@contract_commands.command()
@click.pass_context
def view_contracts_command(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant d'afficher les contrats.")
        return
    display_all_contracts(token)

@contract_commands.command()

@click.pass_context
def create_contract_command(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant de créer un contrat.")
        return
    create_contract(token)


@contract_commands.command()
@click.pass_context
def update_contract_command(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant de modifier un contrat.")
        return
    update_contract(token)

@contract_commands.command()
@click.pass_context
def view_contracts_unpaid(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant d'afficher les contrats impayés.")
        return
    display_contracts_unpaid(token)


@contract_commands.command()
@click.pass_context
def view_unsigned_contracts(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant d'afficher les contrats non signés.")
        return
    display_unsigned_contracts(token)


@contract_commands.command()
@click.pass_context
def delete_contract_command(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant de supprimer un contrat.")
        return
    delete_contract(token) 

