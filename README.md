# Projet-12

<div align="center">
  <img alt="Logo de Epic Events" src="https://github.com/Nantosuelte88/Projet-12/blob/main/media/logo%20epic%20events.png" width="300px">
</div>
<p align="center">
    “Créez des fêtes épiques avec Epic Events, votre partenaire événementiel pour les start-up ambitieuses.”
</p>

## Pour commencer

Ce projet est créé dans le cadre de la formation de Développeur d'application Python proposée par [OpenClassrooms](https://openclassrooms.com/fr/).


### Le projet

Elaborer un système CRM (Customer Relationship Management) sécurisé interne à l'entreprise Epic Events, afin de collecter et de traiter les données des clients et de leurs événements. 

### Les exigences :
  + Créer une base de données permettant de stocker et de manipuler les informations des clients de manière sécurisée.
  + Suivre le cahier des charges.
  + Faire une application en ligne de commande.
  + Empêcher les injections SQL.
  + Respecter les exigences d'autorisations.
  + Mettre en place une journalisation avec Sentry.
  + Respecter les directives de codage de la PEP8 pour assurer la lisibilité du code.


### Prérequis

> [!IMPORTANT]
> Nécessite une version de Python supérieure à 3 (la version 3.9 ou une version plus récente)



## Installation

D'abord, clonez le projet : 
```
$ git clone https://github.com/Nantosuelte88/Projet-12.git
```


Pour créer l'environnement :
```
$ python -m venv env
```

Pour l'activer sur Unix et MacOS :
```
$ source env/bin/activate
```

Pour l'activer sur Windows (Pas de ".bat" sous Powershell) :
```
$ env\Scripts\activate.bat
```

Installez les dépendances :
```
$ pip install -r requirements.txt
```

## Mise en place de la base de données

J'ai utilisé MySQL pour ce projet. Si vous souhaitez utiliser un autre moteur de base de données, vous devrez modifier certaines parties du code. Vous pouvez installer MySQL depuis le [site officiel](https://www.mysql.com/fr/) en vous conformant à la documentation appropriée. Vous pouvez également installer les outils d'administration associés tels que PgAdmin ou MySQL Workbench.

1. Renommez le fichier "fichier_env.txt" en ".env". Ce fichier ".env" sera utilisé pour stocker toutes les données sensibles.

2. Créez une base de données vide à l'aide de MySQL.

3. Créez un utilisateur dans MySQL et enregistrez les informations de connexion dans le fichier ".env". Assurez-vous que l'utilisateur dispose des autorisations appropriées pour la création des tables et des données.

4. Exécutez le fichier "database_setup.py" pour créer les tables initiales dans la base de données. Assurez-vous d'avoir activé l'environnement virtuel et d'avoir installé les dépendances requises.

5. Exécutez le fichier "secret_key_setup.py" pour créer une clé secrète. Cette clé est essentielle pour sécuriser votre base de données et sera automatiquement ajoutée à votre fichier ".env".

6. Allez sur le site Sentry et créez un nouveau projet. Copiez le lien fourni (DSN) et ajoutez-le dans le fichier ".env" sous la variable "DSN=". Cela permettra de lier votre application à Sentry pour la gestion des erreurs.

7. Exécutez le fichier "create_data_for_db.py" pour créer les 3 départements et un premier collaborateur. Assurez-vous de lire attentivement les commentaires dans le fichier pour comprendre comment personnaliser les données.


Une fois que vous avez configuré la base de données comme expliqué précédemment, vous pouvez utiliser les lignes de commande pour exécuter le programme. Suivez les étapes suivantes : 

Connexion avec le compte du collaborateur du département "Gestion": 
```
$ python epicevents.py auth-commands login-command
```

Création d'autres collaborateurs : (il vous faut au moins un collaborateur dans chaque département :

```
$ python epicevents.py collaborator-commands create-collaborator-command
```

Une fois que vous avez créé les collaborateurs, vous êtes libre d'exécuter les différentes fonctionnalités offertes par cette application.




## Fonctionnalités


Plusieurs fonctionnalités sont disponibles dans l'application, mais veuillez noter que certaines nécessitent des permissions spécifiques pour y accéder.

1. **Connexion et déconnexion** :
   - Pour vous connecter :
     ```
     $ python epicevents.py auth-commands login-command
     ```
     Le token sera enregistré dans le fichier "token.txt" (créé automatiquement s'il n'existe pas).
   - Pour vous déconnecter :
     ```
     $ python epicevents.py auth-commands logout-command
     ```
     Le token sera alors effacé.

2. **Collaborateurs** :
   - Pour voir tous les collaborateurs :
     ```
     $ python epicevents.py collaborator-commands view-collaborators
     ```
   - Pour créer un collaborateur :
     ```
     $ python epicevents.py collaborator-commands create-collaborator-command
     ```
   - Pour mettre à jour un collaborateur :
     ```
     $ python epicevents.py collaborator-commands update-collaborator-command
     ```
   - Pour supprimer un collaborateur :
     ```
     $ python epicevents.py collaborator-commands delete-collaborator-command
     ```

3. **Clients** :
   - Pour voir tous les clients :
     ```
     $ python epicevents.py clients-commands view-clients
     ```
   - Pour voir les clients associés à votre compte :
     ```
     $ python epicevents.py clients-commands view-my-clients
     ```
   - Pour créer un client :
     ```
     $ python epicevents.py clients-commands create-client-command
     ```
   - Pour mettre à jour un client :
     ```
     $ python epicevents.py clients-commands update-client-command
     ```
   - Pour supprimer un client :
     ```
     $ python epicevents.py clients-commands delete-client-command
     ```


4. **Contrats** :
   - Pour voir tous les contrats :
     ```
     $ python epicevents.py contract-commands view-contracts-command
     ```
   - Pour créer un contrat :
     ```
     $ python epicevents.py contract-commands create-contract-command
     ```
   - Pour mettre à jour un contrat :
     ```
     $ python epicevents.py contract-commands update-contract-command
     ```
   - Pour voir les contrats impayés :
     ```
     $ python epicevents.py contract-commands view-contracts-unpaid
     ```
   - Pour voir les contrats non signés :
     ```
     $ python epicevents.py contract-commands view-unsigned-contracts
     ```
   - Pour supprimer un contrat :
     ```
     $ python epicevents.py contract-commands delete-contract-command
     ```


5. **Événements** :
   - Pour voir tous les événements :
     ```
     $ python epicevents.py event-commands view-events-command
     ```
   - Pour créer un événement :
     ```
     $ python epicevents.py event-commands create-event-command
     ```
   - Pour mettre à jour un événement :
     ```
     $ python epicevents.py event-commands update-event-command
     ```
   - Pour mettre à jour le support d'un événement :
     ```
     $ python epicevents.py event-commands update-support-in-event-command
     ```
   - Pour voir les événements sans support :
     ```
     $ python epicevents.py event-commands event-without-support-command
     ```
   - Pour voir les événements qui vous sont associés :
     ```
     $ python epicevents.py event-commands view-my-events-command
     ```
   - Pour supprimer un événement :
     ```
     $ python epicevents.py event-commands delete-event-command
     ```




## Langages Utilisés

* Python 
* MySQL
* Click
* SQLAlchemy
* Sentry

  
> README rédigé à l'aide de :
> - [Docs GitHub](https://docs.github.com/fr/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
> - [Template by PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
> - [Align items by DavidWells](https://gist.github.com/DavidWells/7d2e0e1bc78f4ac59a123ddf8b74932d)
