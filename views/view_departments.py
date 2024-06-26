import click


def view_wich_collaborator_in_department(collaborators_corresponding, department_id, found):
    """
    Affiche les collaborateurs correspondant à un département spécifié et demande à l'utilisateur de choisir s'il y en a plusieurs.
    """
    if found:
        collaborator_found = None

        if collaborators_corresponding:
            if len(collaborators_corresponding) == 1:

                click.echo(f'Un collaborateur correspondant {collaborators_corresponding[0].full_name}')
                response = click.prompt(
                    'Selectionner ce collaborateur ? (O/N) ')
                if response.upper() == 'O':
                    collaborator_found = collaborators_corresponding[0]
                else:
                    return None
            else:
                click.echo("Plusieurs collaborateurs correspondent à ce nom :")
                for idx, collaborator in enumerate(collaborators_corresponding, start=1):
                    click.echo(f"{idx}. {collaborator.full_name}")

                selected_idx = click.prompt(
                    "Entrez le numéro correspondant: ", type=int)
                if 1 <= selected_idx <= len(collaborators_corresponding):
                    click.echo(
                        f'{collaborators_corresponding[selected_idx - 1].full_name}')
                    collaborator_found = collaborators_corresponding[selected_idx - 1]

            if collaborator_found.department_id == department_id:
                return collaborator_found.id
            else:
                click.echo(
                    'Le collaborateur trouvé ne fait pas partie du departement demandé, aucun collaborateur ne sera ajouté')
                return None

        else:
            click.echo("Aucun collaborateur correspondant.")
            return None

    else:
        collaborator_name = click.prompt(
            "Entrez le nom du collaborateur: ", type=str)
        if collaborator_name:
            return collaborator_name 
