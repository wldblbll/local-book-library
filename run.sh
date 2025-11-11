#!/bin/bash

# Script d'aide pour lancer la bibliothèque locale

echo "📚 Bibliothèque Locale - Assistant de démarrage"
echo "=============================================="
echo ""

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

echo "✓ Python 3 détecté"

# Vérifier si les dépendances sont installées
if ! python3 -c "import pypdf" 2>/dev/null; then
    echo ""
    echo "📦 Installation des dépendances..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Erreur lors de l'installation des dépendances"
        exit 1
    fi
    echo "✓ Dépendances installées"
else
    echo "✓ Dépendances déjà installées"
fi

echo ""
echo "Choisissez une option :"
echo "1) Scanner une nouvelle bibliothèque"
echo "2) Importer des catégories/notes depuis un fichier JSON"
echo "3) Ouvrir l'interface web"
echo "4) Lancer un serveur web local"
echo "5) Quitter"
echo ""
read -p "Votre choix (1-5) : " choice

case $choice in
    1)
        echo ""
        read -p "Entrez le chemin vers votre dossier de livres : " library_path
        if [ ! -d "$library_path" ]; then
            echo "❌ Le dossier n'existe pas : $library_path"
            exit 1
        fi
        echo ""
        echo "🔍 Scan en cours..."
        python3 scanner.py "$library_path"
        echo ""
        echo "✓ Scan terminé !"
        echo "  Vous pouvez maintenant ouvrir index.html dans votre navigateur"
        ;;
    2)
        if [ ! -f "library_data/library.json" ]; then
            echo "❌ Aucune bibliothèque trouvée. Veuillez d'abord scanner vos livres (option 1)"
            exit 1
        fi
        echo ""
        read -p "Entrez le chemin du fichier JSON de catégories/notes : " categories_file
        if [ ! -f "$categories_file" ]; then
            echo "❌ Le fichier n'existe pas : $categories_file"
            exit 1
        fi
        echo ""
        echo "📥 Import des catégories et notes en cours..."
        python3 import_categories.py "$categories_file"
        if [ $? -eq 0 ]; then
            echo ""
            echo "✓ Import terminé !"
            echo "  Rechargez votre page web (F5) pour voir les changements"
        else
            echo ""
            echo "❌ Erreur lors de l'import"
            exit 1
        fi
        ;;
    3)
        if [ ! -f "library_data/library.json" ]; then
            echo "❌ Aucune bibliothèque trouvée. Veuillez d'abord scanner vos livres (option 1)"
            exit 1
        fi
        echo ""
        echo "🌐 Ouverture de l'interface..."
        # Tenter d'ouvrir selon l'OS
        if command -v xdg-open &> /dev/null; then
            xdg-open index.html
        elif command -v open &> /dev/null; then
            open index.html
        else
            echo "Veuillez ouvrir manuellement le fichier : $(pwd)/index.html"
        fi
        ;;
    4)
        if [ ! -f "library_data/library.json" ]; then
            echo "❌ Aucune bibliothèque trouvée. Veuillez d'abord scanner vos livres (option 1)"
            exit 1
        fi
        echo ""
        echo "🚀 Démarrage du serveur web local..."
        echo "   Accédez à : http://localhost:8000"
        echo "   Appuyez sur Ctrl+C pour arrêter"
        echo ""
        python3 -m http.server 8000
        ;;
    5)
        echo "Au revoir ! 👋"
        exit 0
        ;;
    *)
        echo "❌ Option invalide"
        exit 1
        ;;
esac
