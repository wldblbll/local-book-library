#!/usr/bin/env python3
"""
Script de test pour vérifier la structure du projet
"""
import os
import json
from pathlib import Path

def test_project_structure():
    """Vérifie que tous les fichiers nécessaires sont présents"""
    print("🔍 Vérification de la structure du projet...\n")

    required_files = [
        'scanner.py',
        'index.html',
        'requirements.txt',
        'README.md',
        'run.sh',
        'run.bat',
        '.gitignore'
    ]

    all_ok = True
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"✓ {file} ({size} bytes)")
        else:
            print(f"❌ {file} manquant")
            all_ok = False

    print()

    # Vérifier le contenu de requirements.txt
    print("📦 Vérification des dépendances...")
    with open('requirements.txt', 'r') as f:
        deps = f.read()
        required_deps = ['pypdf', 'ebooklib', 'Pillow']
        for dep in required_deps:
            if dep in deps:
                print(f"✓ {dep} dans requirements.txt")
            else:
                print(f"❌ {dep} manquant dans requirements.txt")
                all_ok = False

    print()

    # Vérifier que scanner.py est syntaxiquement correct
    print("🐍 Vérification de la syntaxe Python...")
    try:
        with open('scanner.py', 'r') as f:
            code = f.read()
            compile(code, 'scanner.py', 'exec')
            print("✓ scanner.py syntaxe valide")
    except SyntaxError as e:
        print(f"❌ Erreur de syntaxe dans scanner.py: {e}")
        all_ok = False

    print()

    # Vérifier que index.html contient les éléments essentiels
    print("🌐 Vérification de l'interface web...")
    with open('index.html', 'r') as f:
        html = f.read()
        required_elements = [
            'search-input',
            'author-filter',
            'category-filter',
            'books-display',
            'book-modal',
            'loadLibrary'
        ]
        for element in required_elements:
            if element in html:
                print(f"✓ {element} présent")
            else:
                print(f"❌ {element} manquant")
                all_ok = False

    print()
    print("=" * 50)
    if all_ok:
        print("✅ Tous les tests sont passés !")
        print("\nProchaines étapes :")
        print("1. Installez les dépendances : pip install -r requirements.txt")
        print("2. Scannez votre bibliothèque : python scanner.py /chemin/vers/livres")
        print("3. Ouvrez index.html dans votre navigateur")
    else:
        print("❌ Certains tests ont échoué")
    print("=" * 50)

if __name__ == "__main__":
    test_project_structure()
