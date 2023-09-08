# Banque-App

Bienvenue dans Banque-App, une application web de gestion bancaire en temps réel développée avec Django et Vue.js.

## Fonctionnalités principales

Banque-App est conçue pour répondre aux besoins de différents types d'utilisateurs :

### Superadmins

- Création de comptes pour les administrateurs moyens.
- Possibilité de faire des dépôts et des retraits de fonds pour les clients.
- Gestion globale du système.

### Admins Moyens

- Gestion des clients et des comptes.
- Réalisation de dépôts et de retraits pour les clients.
- Consultation de l'historique des transactions.

### Clients

- Consultation de l'historique des transactions.
- Transfert de fonds vers des comptes valides.

## Technologies utilisées

- **Django** : Utilisé pour la gestion du backend, l'authentification des utilisateurs, et la gestion des données.
- **Vue.js** : Utilisé en tant que CDN pour la création d'interfaces utilisateur dynamiques et réactives.
- **Temps réel** : Votre application est en temps réel, permettant une expérience utilisateur fluide et en temps réel.

## Prérequis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés :

- [Python](https://www.python.org/downloads/)

## Installation

1. Clonez le dépôt :

```sh
git clone https://github.com/VotreNom/Banque-App.git
```

2. Installez les dépendances Python :

```sh
cd Banque-App
pip install -r requirements.txt
```

4. Lancez l'application :

```sh
python manage.py runserver
```

## Configuration

Assurez-vous de configurer correctement les paramètres de votre base de données et d'authentification Django dans le fichier `settings.py`, par defaut une base de donnée SQLite est utilisé en développement.

## Tester la version en ligne

Vous pouvez tester sa version en ligne sur [ce lien](https://banque-app.kabirou-alassane.com)

Pour se connecter:

### compte super admin

email: `admin@exemple.com`

password: `passme`

### compte Admins Moyens

Créer

### compte client

Créer

## Contribution

Les contributions à Banque-App sont les bienvenues ! Si vous souhaitez contribuer, veuillez suivre ces étapes :

1. Fork du dépôt.
2. Créez une branche pour votre fonctionnalité (`git checkout -b fonctionnalite/nom`).
3. Effectuez vos modifications et ajoutez-les (`git add .`).
4. Committez vos modifications (`git commit -m 'Ajout de la fonctionnalité X'`).
5. Poussez la branche (`git push origin fonctionnalite/nom`).
6. Ouvrez une demande d'extraction.

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.