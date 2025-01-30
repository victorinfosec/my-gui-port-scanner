# PentesterTool

## Description
PentesterTool est une application GUI en Python permettant d'effectuer différentes tâches de cybersécurité :
- Scan de ports ouverts sur une cible
- Génération de commandes de reverse shell
- Identification de types de hash

L'application utilise `customtkinter` pour l'interface et est organisée en plusieurs onglets accessibles via un menu déroulant.

## Installation

### 1. Cloner le dépôt
```bash
git clone <URL_DU_REPO>
cd <NOM_DU_REPO>
```

### 2. Installer les dépendances
Assurez-vous d'avoir Python 3 installé, puis exécutez :
```bash
pip install -r requirements.txt
```

## Utilisation

### 1. Lancer l'application
```bash
python app.py
```

### 2. Fonctionnalités
L'application est divisée en trois onglets :

#### **Scan**
- Entrer une adresse IP et un port de fin (par défaut 1024).
- Lancer un scan de ports ouverts.
- Arrêter un scan en cours.
- Exporter les résultats dans un fichier texte.

#### **Exploit**
- Affiche l'adresse IP locale.
- Génère des commandes de reverse shell en Bash et Python.
- Copie facilement les commandes générées dans le presse-papiers.

#### **Hash**
- Permet d'entrer un hash et d'identifier son type.

## Exigences
L'application nécessite les bibliothèques suivantes :
- `customtkinter`
- `socket`
- `threading`
- `module.PortScanner`
- `module.HashIdentifier`

## Exportation des résultats
Les résultats des scans de ports peuvent être exportés dans un fichier `scan_results.txt`.

