# Changelog

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
