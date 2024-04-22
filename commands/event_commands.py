import click
from controllers.auth_permissions import authorize
from controllers.event_crud import display_all_events, display_event_without_support, display_my_events, create_event, update_event, delete_event, update_support_in_event


@click.group()
def event_commands():
    pass


@event_commands.command()
@click.pass_context
def view_events_command(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant d'afficher les événementss.")
        return
    display_all_events(token)


@event_commands.command()
@click.pass_context
def create_event_command(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant de créer un événement.")
        return
    create_event(token)


@event_commands.command()
@click.pass_context
def update_event_command(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant de modifier un événement.")
        return
    update_event(token)


@event_commands.command()
@click.pass_context
def update_support_in_event_command(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant de modifier un événement.")
        return
    update_support_in_event(token)

@event_commands.command()
@click.pass_context
def event_without_support_command(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant d'afficher les événements sans support.")
        return
    display_event_without_support(token)


@event_commands.command()
@click.pass_context
def view_my_events_command(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant d'afficher les événements qui vous sont associés.")
        return
    display_my_events(token)


@event_commands.command()
@click.pass_context
def delete_event_command(ctx):
    token = ctx.obj["token"]

    if token is None or not authorize(token):
        click.echo(
            "Veuillez vous connecter en utilisant la commande 'login' avant de supprimer un événement.")
        return
    delete_event(token)
