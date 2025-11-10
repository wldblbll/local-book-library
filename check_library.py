#!/usr/bin/env python3
"""
Vérifie la validité du fichier library.json
"""
import json
import sys

def check_json_validity(json_file="library_data/library.json"):
    """Vérifie que le JSON est valide et complet"""
    try:
        print(f"🔍 Vérification de {json_file}...")

        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"✓ JSON valide!")
        print(f"  Version: {data.get('version', 'N/A')}")
        print(f"  Date de scan: {data.get('scan_date', 'N/A')}")
        print(f"  Chemin bibliothèque: {data.get('library_path', 'N/A')}")
        print(f"  Total livres: {data.get('total_books', 0)}")
        print(f"  Livres dans la liste: {len(data.get('books', []))}")

        # Vérifier que le nombre correspond
        if data.get('total_books') != len(data.get('books', [])):
            print(f"⚠️  Attention: Le nombre total ({data.get('total_books')}) ne correspond pas au nombre de livres ({len(data.get('books', []))})")

        # Vérifier quelques livres au hasard
        books = data.get('books', [])
        if books:
            print(f"\n📚 Vérification des livres:")
            required_fields = ['id', 'filename', 'path', 'type', 'title', 'author']

            errors = []
            for i, book in enumerate(books):
                for field in required_fields:
                    if field not in book:
                        errors.append(f"  Livre {i} ({book.get('filename', 'inconnu')}): champ '{field}' manquant")

            if errors:
                print(f"❌ {len(errors)} erreur(s) trouvée(s):")
                for error in errors[:10]:  # Afficher max 10 erreurs
                    print(error)
                if len(errors) > 10:
                    print(f"  ... et {len(errors) - 10} autre(s) erreur(s)")
                return False
            else:
                print(f"✓ Tous les livres ont les champs requis")

        print(f"\n✅ Le fichier JSON est valide et complet!")
        return True

    except FileNotFoundError:
        print(f"❌ Fichier non trouvé: {json_file}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ JSON invalide: {e}")
        print(f"  Position: ligne {e.lineno}, colonne {e.colno}")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    json_file = sys.argv[1] if len(sys.argv) > 1 else "library_data/library.json"
    success = check_json_validity(json_file)
    sys.exit(0 if success else 1)
