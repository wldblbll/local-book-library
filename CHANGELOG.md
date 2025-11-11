# Changelog

## Version 1.4.0 - Nouvelles fonctionnalités interactives (2025-11-11)

### ✨ Nouvelles fonctionnalités

- **Système de notation par étoiles** : Notez vos livres de 0 à 5 étoiles
  - Affichage des notes sur les cartes de livres
  - Notation interactive dans la modal de détails
  - Sauvegarde des notes dans localStorage et export/import
  - **Filtre par nombre d'étoiles** : Filtrez les livres par note (5★, 4+, 3+, 2+, 1+, Sans note)

- **Ouverture des PDF dans le navigateur** : Bouton pour ouvrir directement les PDF
  - Uniquement pour les fichiers PDF
  - Message d'aide si le navigateur bloque l'accès file://

- **Vue des catégories** : Nouvelle vue affichant toutes les catégories
  - Nombre de livres par catégorie
  - Tri par nombre de livres décroissant
  - Clic sur une catégorie pour filtrer les livres

- **Fermeture de la modal avec Escape** : Appuyez sur Echap pour fermer la modal

### 🔧 Améliorations

- Export/import des notes avec les catégories
- Script import_categories.py mis à jour pour importer les notes
- **Scripts run.sh et run.bat améliorés** : Nouvelle option 2 pour importer directement les catégories/notes depuis le menu interactif

---

## Version 1.3.0 - Catégories colorées et gestion améliorée (2025-11-10)

### ✨ Nouvelles fonctionnalités

- **Catégories colorées** : Chaque catégorie a maintenant sa propre couleur unique
  - Couleur générée automatiquement basée sur le nom de la catégorie
  - Cohérente et déterministe (même nom = même couleur)
  - Palette harmonieuse via HSL

- **Autocomplétion des catégories** : Suggestions en temps réel lors de l'ajout
  - Affiche les catégories existantes pendant la saisie
  - Évite les doublons et variations de noms
  - Interface fluide et intuitive

- **Suppression de livres** : Possibilité de retirer un livre de la bibliothèque
  - Bouton "🗑️ Supprimer ce livre" dans la modal
  - Confirmation obligatoire avant suppression
  - Le fichier physique est préservé
  - Mise à jour automatique de toutes les vues

### 🐛 Corrections

- **Élimination des doublons** dans les listes déroulantes
  - Les filtres auteur/catégorie sont maintenant correctement vidés avant remplissage
  - Plus de catégories en double dans le menu déroulant

### 🎨 Améliorations visuelles

- Text-shadow sur les tags pour meilleure lisibilité
- Bouton de suppression visuellement distinct (rouge)
- Messages de confirmation clairs

---

## Version 1.2.0 - Robustesse et Fiabilité (2025-11-10)

### 🛡️ Corrections critiques

- **Écriture atomique du JSON** : Le fichier library.json est maintenant écrit dans un fichier temporaire puis renommé atomiquement, évitant toute corruption
- **Validation des données** : Tous les champs sont validés avant l'écriture JSON
- **Gestion des erreurs par livre** : Une erreur sur un livre n'interrompt plus le scan complet
- **Sauvegarde sur interruption** : Appuyer sur Ctrl+C sauvegarde les livres déjà scannés
- **Sauvegarde en cas d'erreur** : Même en cas d'erreur fatale, une tentative de sauvegarde partielle est effectuée

### 🔧 Outils

- **check_library.py** : Nouveau script pour vérifier la validité du fichier library.json
  ```bash
  python3 check_library.py
  ```

### 📚 Documentation

- Ajout d'une section dépannage pour JSON corrompu
- Documentation des nouvelles protections

---

## Version 1.1.0 - Scan Incrémental (2025-11-10)

### 🚀 Nouvelles fonctionnalités

- **Scan incrémental** : Le scanner détecte automatiquement les changements depuis le dernier scan
  - Ne traite que les nouveaux fichiers ou modifiés (beaucoup plus rapide !)
  - Supprime automatiquement les livres dont les fichiers ont été effacés
  - Préserve les catégories personnalisées ajoutées par l'utilisateur
  - Nettoie les couvertures des livres supprimés

- **Option `--full`** : Force un scan complet si nécessaire
  ```bash
  python scanner.py /chemin/vers/livres --full
  ```

- **Statistiques détaillées** : Le scanner affiche maintenant :
  - Nombre de livres réutilisés (inchangés)
  - Nombre de nouveaux/modifiés
  - Nombre de livres supprimés

### 🐛 Corrections

- Amélioration du diagnostic des erreurs de chargement JSON
- Meilleurs messages d'erreur pour guider l'utilisateur
- Ajout de logs détaillés dans la console pour le debug

### 📚 Documentation

- Mise à jour du README avec les nouvelles fonctionnalités
- Ajout d'instructions claires pour utiliser le serveur HTTP local
- Amélioration du QUICKSTART.md

---

## Version 1.0.0 - Version Initiale (2025-11-10)

### ✨ Fonctionnalités initiales

- Scanner récursif pour PDF et ePub
- Extraction automatique des métadonnées (titre, auteur, pages)
- Extraction des couvertures de livres
- Interface web HTML/JavaScript pure (sans framework)
- Recherche et filtrage par titre, auteur, catégorie, type
- Support des catégories personnalisées
- Vues grille et liste
- Scripts assistants pour Linux/macOS et Windows
- Documentation complète
