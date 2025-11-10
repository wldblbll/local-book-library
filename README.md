# 📚 Bibliothèque Locale - Gestionnaire de Livres PDF et ePub

Une application simple et élégante pour gérer votre collection de livres numériques en local, sans dépendances externes complexes.

## ✨ Fonctionnalités

- 📖 **Scan automatique** : Scanne récursivement un dossier pour trouver tous vos PDF et ePub
- 🎨 **Extraction de couvertures** : Affiche les couvertures de vos livres
- 🔍 **Recherche puissante** : Recherchez par titre, auteur ou mot-clé
- 🏷️ **Catégorisation** : Ajoutez et gérez des catégories personnalisées
- 📊 **Filtres multiples** : Filtrez par auteur, catégorie et type de fichier
- 🎯 **Interface moderne** : Interface web simple et intuitive (aucun serveur requis)
- 💾 **100% local** : Toutes vos données restent sur votre machine

## 🚀 Installation

### Prérequis

- Python 3.7 ou supérieur
- Un navigateur web moderne (Chrome, Firefox, Edge, Safari)

### Étapes d'installation

1. **Installer les dépendances Python** :

```bash
pip install -r requirements.txt
```

Les dépendances incluent :
- `pypdf` : Pour lire les fichiers PDF
- `ebooklib` : Pour lire les fichiers ePub
- `Pillow` : Pour extraire et traiter les couvertures

## 📖 Utilisation

### Étape 1 : Scanner votre bibliothèque

Exécutez le scanner en lui indiquant le chemin vers votre dossier de livres :

```bash
python scanner.py /chemin/vers/vos/livres
```

**Options disponibles** :

```bash
python scanner.py /chemin/vers/vos/livres [OPTIONS]

Options:
  -o, --output DIR    Dossier de sortie (défaut: library_data)
  --full              Forcer un scan complet (ignore la base existante)
```

**Exemple** :

```bash
# Windows
python scanner.py "C:\Users\VotreNom\Documents\Livres"

# macOS/Linux
python scanner.py ~/Documents/Livres

# Forcer un scan complet
python scanner.py ~/Documents/Livres --full
```

Le scanner va :
1. Parcourir récursivement tous les sous-dossiers
2. Trouver tous les fichiers `.pdf` et `.epub`
3. **🚀 Mode incrémental (par défaut)** : Ne scanne que les nouveaux/modifiés, garde les catégories
4. Extraire les métadonnées (titre, auteur, etc.)
5. Extraire les couvertures quand c'est possible
6. Créer une base de données JSON dans le dossier `library_data/`

> ⚡ **Nouveau !** Le scanner est maintenant **incrémental** : si vous relancez le scan, seuls les nouveaux livres ou modifiés seront traités. Les livres supprimés seront automatiquement retirés. Vos catégories personnalisées sont préservées !

### Étape 2 : Ouvrir l'interface web

Une fois le scan terminé, ouvrez simplement le fichier `index.html` dans votre navigateur :

- **Double-cliquez** sur `index.html`, ou
- **Faites un clic droit** > Ouvrir avec > Votre navigateur préféré

C'est tout ! Aucun serveur web n'est nécessaire.

## 🎯 Utilisation de l'interface

### Vue d'ensemble

L'interface vous permet de :

1. **Voir tous vos livres** en mode grille ou liste
2. **Rechercher** dans les titres et auteurs
3. **Filtrer** par auteur, catégorie ou type de fichier
4. **Ajouter des catégories** à vos livres
5. **Ouvrir les livres** directement dans votre lecteur PDF/ePub préféré

### Barre de recherche

Tapez n'importe quel mot-clé pour rechercher dans :
- Les titres de livres
- Les noms d'auteurs
- Les noms de fichiers

### Filtres

Utilisez les menus déroulants pour filtrer par :
- **Auteur** : Voir tous les livres d'un auteur spécifique
- **Catégorie** : Afficher seulement les livres d'une catégorie
- **Type** : Filtrer par PDF ou ePub

### Modes d'affichage

- **Mode Grille** : Grandes cartes avec couvertures (par défaut)
- **Mode Liste** : Vue compacte pour parcourir rapidement

### Gestion des catégories

1. **Cliquez sur un livre** pour ouvrir ses détails
2. **Tapez une catégorie** dans le champ prévu
3. **Cliquez sur "Ajouter"**
4. Les catégories sont sauvegardées localement dans votre navigateur

**Exemples de catégories** : Roman, Science-Fiction, Technique, Cuisine, Biographie, etc.

## 📁 Structure du projet

```
local-book-library/
├── scanner.py          # Script de scan et indexation
├── index.html          # Interface web
├── requirements.txt    # Dépendances Python
├── README.md          # Ce fichier
└── library_data/      # Créé après le premier scan
    ├── library.json   # Base de données de vos livres
    └── covers/        # Couvertures extraites
        ├── abc123.jpg
        └── def456.jpg
```

## 🔄 Mettre à jour votre bibliothèque

### Scan incrémental (recommandé - ultra rapide !)

Si vous ajoutez ou supprimez des livres, relancez simplement le scanner :

```bash
python scanner.py /chemin/vers/vos/livres
```

Le scanner détectera automatiquement :
- ✅ **Nouveaux livres** : Seront scannés et ajoutés
- ✅ **Livres modifiés** : Seront re-scannés
- ✅ **Livres supprimés** : Seront retirés de la base
- ✅ **Livres inchangés** : Seront ignorés (super rapide !)

**Vos catégories personnalisées sont préservées** pendant les scans incrémentiaux !

### Scan complet (si nécessaire)

Si vous voulez tout rescanner (par exemple après un problème) :

```bash
python scanner.py /chemin/vers/vos/livres --full
```

> ⚡ **Astuce** : Avec 1465 livres, un scan incrémental prend quelques secondes au lieu de plusieurs minutes !

Puis **rechargez** la page web (`F5` ou `Ctrl+R` / `Cmd+R`).

## 🎨 Personnalisation

### Changer les couleurs

Modifiez les couleurs dans le fichier `index.html` :

```css
/* Ligne 16 - Dégradé de fond */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Ligne 134 - Couleur des tags */
background: #667eea;
```

### Ajuster la taille des couvertures

Dans `scanner.py`, ligne 82 et 142 :

```python
image.thumbnail((300, 400))  # Modifier ces valeurs
```

## ❓ FAQ

### Mes livres n'ont pas de couverture ?

- Certains PDF n'ont pas d'image sur la première page
- Les ePub nécessitent que la couverture soit correctement définie dans les métadonnées
- Un icône de livre 📖 sera affiché par défaut

### Les métadonnées sont incorrectes ?

Les métadonnées dépendent de ce qui est encodé dans le fichier. Si elles sont manquantes :
- Le nom du fichier sera utilisé comme titre
- "Auteur inconnu" sera affiché

Pour corriger cela, vous pouvez utiliser des outils comme :
- [Calibre](https://calibre-ebook.com/) pour éditer les métadonnées

### Puis-je utiliser ceci sur un réseau local ?

Oui ! Pour partager avec d'autres ordinateurs :

```bash
# Lancez un serveur HTTP simple
python -m http.server 8000
```

Puis accédez à `http://[votre-ip]:8000` depuis un autre appareil.

### Les catégories disparaissent quand je rescanne ?

Les catégories sont sauvegardées dans le `localStorage` du navigateur et sont restaurées automatiquement. Assurez-vous d'utiliser toujours le même navigateur.

## 🐛 Dépannage

### Erreur "Module not found"

```bash
pip install -r requirements.txt
```

### "Impossible de charger la bibliothèque"

- Vérifiez que vous avez bien exécuté `scanner.py` d'abord
- Vérifiez que le dossier `library_data/` existe
- Ouvrez `index.html` depuis le même dossier où se trouve `library_data/`

### Les couvertures ne s'affichent pas

- Vérifiez que Pillow est installé : `pip install Pillow`
- Certains PDF/ePub n'ont pas de couvertures extraites automatiquement

## 📝 Licence

Projet libre, utilisez et modifiez comme vous le souhaitez !

## 🤝 Contribution

N'hésitez pas à améliorer ce projet :
- Ajoutez le support pour d'autres formats (MOBI, AZW, etc.)
- Améliorez l'extraction des métadonnées
- Ajoutez des fonctionnalités (notes, évaluations, etc.)

---

**Profitez de votre bibliothèque ! 📚✨**
