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
    def __init__(self, library_path, output_dir="library_data"):
        self.library_path = Path(library_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.covers_dir = self.output_dir / "covers"
        self.covers_dir.mkdir(exist_ok=True)
        self.books = []

    def get_file_hash(self, filepath):
        """Génère un hash unique pour identifier le fichier"""
        return hashlib.md5(str(filepath).encode()).hexdigest()

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

        # Extensions supportées
        pdf_files = list(self.library_path.rglob("*.pdf"))
        epub_files = list(self.library_path.rglob("*.epub")) if EPUB_AVAILABLE else []

        total_files = len(pdf_files) + len(epub_files)
        print(f"Fichiers trouvés: {len(pdf_files)} PDF, {len(epub_files)} ePub")

        processed = 0

        # Traiter les PDF
        for pdf_file in pdf_files:
            processed += 1
            print(f"[{processed}/{total_files}] Traitement: {pdf_file.name}")

            metadata = self.extract_pdf_metadata(pdf_file)
            if metadata:
                book_info = {
                    'id': self.get_file_hash(pdf_file),
                    'filename': pdf_file.name,
                    'path': str(pdf_file.absolute()),
                    'type': 'pdf',
                    'title': metadata['title'],
                    'author': metadata['author'],
                    'cover': metadata['cover'],
                    'pages': metadata['pages'],
                    'size': pdf_file.stat().st_size,
                    'modified': datetime.fromtimestamp(pdf_file.stat().st_mtime).isoformat(),
                    'categories': []
                }
                self.books.append(book_info)

        # Traiter les ePub
        for epub_file in epub_files:
            processed += 1
            print(f"[{processed}/{total_files}] Traitement: {epub_file.name}")

            metadata = self.extract_epub_metadata(epub_file)
            if metadata:
                book_info = {
                    'id': self.get_file_hash(epub_file),
                    'filename': epub_file.name,
                    'path': str(epub_file.absolute()),
                    'type': 'epub',
                    'title': metadata['title'],
                    'author': metadata['author'],
                    'cover': metadata['cover'],
                    'pages': metadata['pages'],
                    'size': epub_file.stat().st_size,
                    'modified': datetime.fromtimestamp(epub_file.stat().st_mtime).isoformat(),
                    'categories': []
                }
                self.books.append(book_info)

        print(f"\nScan terminé! {len(self.books)} livres indexés.")

    def save_database(self):
        """Sauvegarde la base de données au format JSON"""
        db_file = self.output_dir / "library.json"

        database = {
            'version': '1.0',
            'scan_date': datetime.now().isoformat(),
            'library_path': str(self.library_path),
            'total_books': len(self.books),
            'books': self.books
        }

        with open(db_file, 'w', encoding='utf-8') as f:
            json.dump(database, f, ensure_ascii=False, indent=2)

        print(f"Base de données sauvegardée: {db_file}")

        # Créer aussi une version compacte
        db_file_compact = self.output_dir / "library.min.json"
        with open(db_file_compact, 'w', encoding='utf-8') as f:
            json.dump(database, f, ensure_ascii=False)

        print(f"Version compacte: {db_file_compact}")


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

    args = parser.parse_args()

    if not os.path.exists(args.library_path):
        print(f"Erreur: Le chemin {args.library_path} n'existe pas")
        return

    scanner = BookScanner(args.library_path, args.output)
    scanner.scan_directory()
    scanner.save_database()

    print("\n✓ Indexation terminée!")
    print(f"  Vous pouvez maintenant ouvrir 'index.html' pour naviguer dans votre bibliothèque.")


if __name__ == "__main__":
    main()
