#!/usr/bin/env python3
"""
Scanner de bibliothèque locale pour PDF et ePub
"""
import os
import json
import base64
import hashlib
from pathlib import Path
from io import BytesIO
import argparse
from datetime import datetime
import signal
import sys

try:
    from pypdf import PdfReader
except ImportError:
    from PyPDF2 import PdfReader

try:
    import ebooklib
    from ebooklib import epub
    EPUB_AVAILABLE = True
except ImportError:
    EPUB_AVAILABLE = False
    print("Warning: ebooklib non installé, les fichiers ePub ne seront pas traités")

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("Warning: Pillow non installé, les couvertures ne seront pas extraites")


class BookScanner:
    def __init__(self, library_path, output_dir="library_data", incremental=True):
        self.library_path = Path(library_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.covers_dir = self.output_dir / "covers"
        self.covers_dir.mkdir(exist_ok=True)
        self.books = []
        self.incremental = incremental
        self.existing_books = {}  # hash -> book_info

    def get_file_hash(self, filepath):
        """Génère un hash unique pour identifier le fichier"""
        return hashlib.md5(str(filepath).encode()).hexdigest()

    def load_existing_database(self):
        """Charge la base de données existante pour un scan incrémental"""
        db_file = self.output_dir / "library.json"
        if not db_file.exists():
            print("Aucune base de données existante - scan complet")
            return

        try:
            with open(db_file, 'r', encoding='utf-8') as f:
                old_library = json.load(f)

            # Créer un dictionnaire des livres existants par ID
            for book in old_library.get('books', []):
                self.existing_books[book['id']] = book

            print(f"Base de données chargée: {len(self.existing_books)} livres existants")
        except Exception as e:
            print(f"Erreur lors du chargement de la base: {e}")
            print("Scan complet effectué")

    def extract_pdf_metadata(self, filepath):
        """Extrait les métadonnées d'un fichier PDF"""
        try:
            reader = PdfReader(filepath)
            metadata = reader.metadata

            title = metadata.get('/Title', '') if metadata else ''
            author = metadata.get('/Author', '') if metadata else ''

            # Si pas de titre, utiliser le nom du fichier
            if not title or title.strip() == '':
                title = filepath.stem

            # Extraction de la première page comme couverture
            cover_path = None
            if PIL_AVAILABLE and len(reader.pages) > 0:
                try:
                    first_page = reader.pages[0]
                    if '/XObject' in first_page['/Resources']:
                        xobjects = first_page['/Resources']['/XObject'].get_object()
                        for obj in xobjects:
                            if xobjects[obj]['/Subtype'] == '/Image':
                                size = (xobjects[obj]['/Width'], xobjects[obj]['/Height'])
                                data = xobjects[obj].get_data()

                                # Sauvegarder l'image de couverture
                                file_hash = self.get_file_hash(filepath)
                                cover_filename = f"{file_hash}.jpg"
                                cover_path = self.covers_dir / cover_filename

                                try:
                                    image = Image.open(BytesIO(data))
                                    # Redimensionner pour économiser de l'espace
                                    image.thumbnail((300, 400))
                                    image.save(cover_path, "JPEG")
                                    cover_path = str(cover_path.relative_to(self.output_dir))
                                except:
                                    cover_path = None
                                break
                except:
                    pass

            return {
                'title': title,
                'author': author or 'Auteur inconnu',
                'cover': cover_path,
                'pages': len(reader.pages)
            }
        except Exception as e:
            print(f"Erreur lors de la lecture de {filepath}: {e}")
            return None

    def extract_epub_metadata(self, filepath):
        """Extrait les métadonnées d'un fichier ePub"""
        if not EPUB_AVAILABLE:
            return None

        try:
            book = epub.read_epub(filepath)

            title = book.get_metadata('DC', 'title')
            title = title[0][0] if title else filepath.stem

            author = book.get_metadata('DC', 'creator')
            author = author[0][0] if author else 'Auteur inconnu'

            # Extraction de la couverture
            cover_path = None
            if PIL_AVAILABLE:
                try:
                    # Chercher l'image de couverture
                    for item in book.get_items():
                        if item.get_type() == ebooklib.ITEM_IMAGE:
                            # Prendre la première image (souvent la couverture)
                            file_hash = self.get_file_hash(filepath)
                            cover_filename = f"{file_hash}.jpg"
                            cover_path = self.covers_dir / cover_filename

                            image = Image.open(BytesIO(item.get_content()))
                            image.thumbnail((300, 400))
                            image.save(cover_path, "JPEG")
                            cover_path = str(cover_path.relative_to(self.output_dir))
                            break
                except:
                    pass

            return {
                'title': title,
                'author': author,
                'cover': cover_path,
                'pages': None  # ePub n'a pas de pages fixes
            }
        except Exception as e:
            print(f"Erreur lors de la lecture de {filepath}: {e}")
            return None

    def scan_directory(self):
        """Scanne récursivement le répertoire pour les livres"""
        print(f"Scan du répertoire: {self.library_path}")

        # Charger la base existante si scan incrémental
        if self.incremental:
            self.load_existing_database()

        # Extensions supportées
        pdf_files = list(self.library_path.rglob("*.pdf"))
        epub_files = list(self.library_path.rglob("*.epub")) if EPUB_AVAILABLE else []

        total_files = len(pdf_files) + len(epub_files)
        print(f"Fichiers trouvés: {len(pdf_files)} PDF, {len(epub_files)} ePub")

        # Garder trace des IDs trouvés pour détecter les suppressions
        found_ids = set()

        new_books = 0
        reused_books = 0
        processed = 0

        # Traiter les PDF
        for pdf_file in pdf_files:
            processed += 1

            try:
                file_id = self.get_file_hash(pdf_file)
                found_ids.add(file_id)

                # Vérifier si le livre existe déjà
                if file_id in self.existing_books:
                    existing = self.existing_books[file_id]
                    # Vérifier si le fichier a été modifié
                    current_mtime = datetime.fromtimestamp(pdf_file.stat().st_mtime).isoformat()

                    if existing['modified'] == current_mtime:
                        # Fichier inchangé, réutiliser les métadonnées
                        print(f"[{processed}/{total_files}] ✓ Déjà indexé: {pdf_file.name}")
                        self.books.append(existing)
                        reused_books += 1
                        continue

                # Nouveau livre ou modifié
                print(f"[{processed}/{total_files}] 📖 Scan: {pdf_file.name}")
                metadata = self.extract_pdf_metadata(pdf_file)
                if metadata:
                    book_info = {
                        'id': file_id,
                        'filename': pdf_file.name,
                        'path': str(pdf_file.absolute()),
                        'type': 'pdf',
                        'title': metadata['title'],
                        'author': metadata['author'],
                        'cover': metadata.get('cover'),
                        'pages': metadata.get('pages'),
                        'size': pdf_file.stat().st_size,
                        'modified': datetime.fromtimestamp(pdf_file.stat().st_mtime).isoformat(),
                        'categories': self.existing_books.get(file_id, {}).get('categories', [])
                    }
                    self.books.append(book_info)
                    new_books += 1
                else:
                    print(f"    ⚠️  Impossible d'extraire les métadonnées")

            except Exception as e:
                print(f"    ❌ Erreur: {e}")
                continue

        # Traiter les ePub
        for epub_file in epub_files:
            processed += 1

            try:
                file_id = self.get_file_hash(epub_file)
                found_ids.add(file_id)

                # Vérifier si le livre existe déjà
                if file_id in self.existing_books:
                    existing = self.existing_books[file_id]
                    # Vérifier si le fichier a été modifié
                    current_mtime = datetime.fromtimestamp(epub_file.stat().st_mtime).isoformat()

                    if existing['modified'] == current_mtime:
                        # Fichier inchangé, réutiliser les métadonnées
                        print(f"[{processed}/{total_files}] ✓ Déjà indexé: {epub_file.name}")
                        self.books.append(existing)
                        reused_books += 1
                        continue

                # Nouveau livre ou modifié
                print(f"[{processed}/{total_files}] 📖 Scan: {epub_file.name}")
                metadata = self.extract_epub_metadata(epub_file)
                if metadata:
                    book_info = {
                        'id': file_id,
                        'filename': epub_file.name,
                        'path': str(epub_file.absolute()),
                        'type': 'epub',
                        'title': metadata['title'],
                        'author': metadata['author'],
                        'cover': metadata.get('cover'),
                        'pages': metadata.get('pages'),
                        'size': epub_file.stat().st_size,
                        'modified': datetime.fromtimestamp(epub_file.stat().st_mtime).isoformat(),
                        'categories': self.existing_books.get(file_id, {}).get('categories', [])
                    }
                    self.books.append(book_info)
                    new_books += 1
                else:
                    print(f"    ⚠️  Impossible d'extraire les métadonnées")

            except Exception as e:
                print(f"    ❌ Erreur: {e}")
                continue

        # Détecter les livres supprimés
        deleted_books = []
        if self.incremental and self.existing_books:
            for book_id, book in self.existing_books.items():
                if book_id not in found_ids:
                    deleted_books.append(book)
                    # Supprimer la couverture si elle existe
                    if book.get('cover'):
                        cover_path = self.output_dir / book['cover']
                        if cover_path.exists():
                            try:
                                cover_path.unlink()
                                print(f"🗑️  Couverture supprimée: {book['cover']}")
                            except:
                                pass

        print(f"\n{'='*60}")
        print(f"Scan terminé!")
        print(f"  Total: {len(self.books)} livres")
        print(f"  Nouveaux/modifiés: {new_books}")
        print(f"  Réutilisés: {reused_books}")
        print(f"  Supprimés: {len(deleted_books)}")
        print(f"{'='*60}")

    def save_database(self):
        """Sauvegarde la base de données au format JSON de manière atomique"""
        db_file = self.output_dir / "library.json"
        db_file_temp = self.output_dir / "library.json.tmp"

        # Validation : s'assurer que tous les livres ont les champs requis
        for book in self.books:
            # Garantir que tous les champs critiques existent
            if 'cover' not in book or book['cover'] is None:
                book['cover'] = None
            if 'categories' not in book:
                book['categories'] = []
            if 'pages' not in book:
                book['pages'] = None

        database = {
            'version': '1.0',
            'scan_date': datetime.now().isoformat(),
            'library_path': str(self.library_path),
            'total_books': len(self.books),
            'books': self.books
        }

        try:
            # Écrire dans un fichier temporaire d'abord
            with open(db_file_temp, 'w', encoding='utf-8') as f:
                json.dump(database, f, ensure_ascii=False, indent=2)

            # Vérifier que le JSON est valide en le relisant
            with open(db_file_temp, 'r', encoding='utf-8') as f:
                json.load(f)

            # Si tout est OK, remplacer l'ancien fichier de manière atomique
            db_file_temp.replace(db_file)
            print(f"✓ Base de données sauvegardée: {db_file}")

            # Créer aussi une version compacte
            db_file_compact = self.output_dir / "library.min.json"
            db_file_compact_temp = self.output_dir / "library.min.json.tmp"

            with open(db_file_compact_temp, 'w', encoding='utf-8') as f:
                json.dump(database, f, ensure_ascii=False)

            db_file_compact_temp.replace(db_file_compact)
            print(f"✓ Version compacte: {db_file_compact}")

        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde: {e}")
            # Nettoyer les fichiers temporaires
            if db_file_temp.exists():
                db_file_temp.unlink()
            raise


def main():
    parser = argparse.ArgumentParser(
        description='Scanner de bibliothèque locale pour PDF et ePub'
    )
    parser.add_argument(
        'library_path',
        help='Chemin vers le dossier contenant vos livres'
    )
    parser.add_argument(
        '-o', '--output',
        default='library_data',
        help='Dossier de sortie pour la base de données (défaut: library_data)'
    )
    parser.add_argument(
        '--full',
        action='store_true',
        help='Forcer un scan complet (ignore la base existante)'
    )

    args = parser.parse_args()

    if not os.path.exists(args.library_path):
        print(f"Erreur: Le chemin {args.library_path} n'existe pas")
        return

    # Scan incrémental par défaut, complet si --full
    incremental = not args.full

    if args.full:
        print("🔄 Mode: Scan COMPLET (toutes les métadonnées seront réextraites)")
    else:
        print("⚡ Mode: Scan INCRÉMENTAL (seuls les nouveaux/modifiés seront scannés)")

    scanner = BookScanner(args.library_path, args.output, incremental=incremental)

    # Gestionnaire pour Ctrl+C - sauvegarder avant de quitter
    def signal_handler(sig, frame):
        print("\n\n⚠️  Interruption détectée (Ctrl+C)")
        if scanner.books:
            print(f"💾 Sauvegarde des {len(scanner.books)} livres déjà scannés...")
            try:
                scanner.save_database()
                print("✓ Sauvegarde réussie!")
            except Exception as e:
                print(f"❌ Erreur lors de la sauvegarde: {e}")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    try:
        scanner.scan_directory()
        scanner.save_database()

        print("\n✓ Indexation terminée!")
        print(f"  Vous pouvez maintenant ouvrir 'index.html' pour naviguer dans votre bibliothèque.")
    except Exception as e:
        print(f"\n❌ Erreur fatale: {e}")
        if scanner.books:
            print(f"💾 Tentative de sauvegarde des {len(scanner.books)} livres scannés...")
            try:
                scanner.save_database()
                print("✓ Sauvegarde partielle réussie!")
            except:
                pass
        raise


if __name__ == "__main__":
    main()
