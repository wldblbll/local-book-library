# 🚀 Démarrage Rapide

## En 3 étapes simples

### 1️⃣ Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2️⃣ Scanner votre bibliothèque

```bash
python scanner.py /chemin/vers/vos/livres
```

**Exemples** :

```bash
# Windows
python scanner.py "C:\Users\VotreNom\Documents\Livres"

# macOS
python scanner.py ~/Documents/Livres

# Linux
python scanner.py /home/user/Documents/Livres
```

### 3️⃣ Ouvrir l'interface

**Important** : Vous devez utiliser un serveur HTTP local !

```bash
# Lancer le serveur
python3 -m http.server 8000

# Puis ouvrir dans votre navigateur :
# http://localhost:8000
```

---

## 🔄 Mettre à jour votre bibliothèque

**Ajouté/supprimé des livres ?** Relancez simplement :

```bash
python scanner.py /chemin/vers/vos/livres
```

⚡ Le scan incrémental ne traite que les changements (ultra rapide !)

---

## 🎯 Utilisation avec les scripts assistants

### Linux/macOS

```bash
chmod +x run.sh
./run.sh
```

### Windows

```cmd
run.bat
```

---

## 📋 Ce que vous pouvez faire

- ✅ Rechercher dans vos livres par titre, auteur, mot-clé
- ✅ Filtrer par auteur, catégorie, type de fichier
- ✅ Voir les couvertures de vos livres
- ✅ Ajouter des catégories personnalisées
- ✅ Passer en vue grille ou liste
- ✅ Ouvrir vos livres directement

---

## ❓ Besoin d'aide ?

Consultez le **README.md** pour la documentation complète !
