#!/usr/bin/env python3
"""
Script pour importer les catégories exportées depuis l'interface web
et les fusionner dans library.json
"""
import json
import sys
from pathlib import Path
from datetime import datetime


def import_categories(categories_file, library_file="library_data/library.json"):
    """
    Importe les catégories depuis un fichier exporté et les fusionne dans library.json
    """
    # Vérifier que les fichiers existent
    categories_path = Path(categories_file)
    library_path = Path(library_file)

    if not categories_path.exists():
        print(f"❌ Erreur: Le fichier {categories_file} n'existe pas")
        return False

    if not library_path.exists():
        print(f"❌ Erreur: Le fichier {library_file} n'existe pas")
        print("   Assurez-vous d'avoir lancé le scanner d'abord")
        return False

    # Charger les catégories exportées
    print(f"📥 Chargement des catégories depuis {categories_file}...")
    try:
        with open(categories_path, 'r', encoding='utf-8') as f:
            categories_data = json.load(f)
    except Exception as e:
        print(f"❌ Erreur lors du chargement des catégories: {e}")
        return False

    # Charger la bibliothèque
    print(f"📚 Chargement de la bibliothèque depuis {library_file}...")
    try:
        with open(library_path, 'r', encoding='utf-8') as f:
            library = json.load(f)
    except Exception as e:
        print(f"❌ Erreur lors du chargement de la bibliothèque: {e}")
        return False

    # Créer un dictionnaire des catégories par ID de livre
    categories_by_id = {}
    for book_data in categories_data.get('books', []):
        categories_by_id[book_data['id']] = book_data['categories']

    # Fusionner les catégories dans la bibliothèque
    print("🔄 Fusion des catégories...")
    updated_count = 0
    for book in library['books']:
        book_id = book['id']
        if book_id in categories_by_id:
            new_categories = categories_by_id[book_id]
            if book.get('categories') != new_categories:
                book['categories'] = new_categories
                updated_count += 1

    print(f"   {updated_count} livres mis à jour")

    # Créer une sauvegarde de library.json
    backup_path = library_path.parent / f"library_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    print(f"💾 Création d'une sauvegarde: {backup_path}")
    try:
        with open(backup_path, 'w', encoding='utf-8') as f:
            with open(library_path, 'r', encoding='utf-8') as orig:
                f.write(orig.read())
    except Exception as e:
        print(f"⚠️  Avertissement: Impossible de créer la sauvegarde: {e}")

    # Sauvegarder la bibliothèque mise à jour
    print(f"💾 Sauvegarde dans {library_file}...")
    try:
        with open(library_path, 'w', encoding='utf-8') as f:
            json.dump(library, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde: {e}")
        return False

    print("\n✅ Importation réussie!")
    print(f"   {updated_count} livres ont été mis à jour avec leurs catégories")
    print(f"   Sauvegarde créée: {backup_path.name}")
    print("\n💡 Rechargez la page web pour voir les changements")

    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 import_categories.py <fichier_categories.json>")
        print("\nExemple:")
        print("  python3 import_categories.py categories_2025-11-10.json")
        print("\nCe script fusionne les catégories exportées depuis l'interface web")
        print("dans le fichier library.json")
        sys.exit(1)

    categories_file = sys.argv[1]
    library_file = sys.argv[2] if len(sys.argv) > 2 else "library_data/library.json"

    success = import_categories(categories_file, library_file)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
