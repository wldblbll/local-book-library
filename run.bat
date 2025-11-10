@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo 📚 Bibliothèque Locale - Assistant de démarrage
echo ==============================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé. Veuillez l'installer d'abord.
    pause
    exit /b 1
)

echo ✓ Python détecté
echo.

REM Vérifier les dépendances
python -c "import pypdf" 2>nul
if errorlevel 1 (
    echo 📦 Installation des dépendances...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Erreur lors de l'installation des dépendances
        pause
        exit /b 1
    )
    echo ✓ Dépendances installées
) else (
    echo ✓ Dépendances déjà installées
)

echo.
echo Choisissez une option :
echo 1) Scanner une nouvelle bibliothèque
echo 2) Ouvrir l'interface web
echo 3) Lancer un serveur web local
echo 4) Quitter
echo.
set /p choice="Votre choix (1-4) : "

if "%choice%"=="1" (
    echo.
    set /p library_path="Entrez le chemin vers votre dossier de livres : "
    if not exist "!library_path!" (
        echo ❌ Le dossier n'existe pas : !library_path!
        pause
        exit /b 1
    )
    echo.
    echo 🔍 Scan en cours...
    python scanner.py "!library_path!"
    echo.
    echo ✓ Scan terminé !
    echo   Vous pouvez maintenant ouvrir index.html dans votre navigateur
    pause
) else if "%choice%"=="2" (
    if not exist "library_data\library.json" (
        echo ❌ Aucune bibliothèque trouvée. Veuillez d'abord scanner vos livres (option 1^)
        pause
        exit /b 1
    )
    echo.
    echo 🌐 Ouverture de l'interface...
    start index.html
) else if "%choice%"=="3" (
    if not exist "library_data\library.json" (
        echo ❌ Aucune bibliothèque trouvée. Veuillez d'abord scanner vos livres (option 1^)
        pause
        exit /b 1
    )
    echo.
    echo 🚀 Démarrage du serveur web local...
    echo    Accédez à : http://localhost:8000
    echo    Appuyez sur Ctrl+C pour arrêter
    echo.
    python -m http.server 8000
) else if "%choice%"=="4" (
    echo Au revoir ! 👋
    exit /b 0
) else (
    echo ❌ Option invalide
    pause
    exit /b 1
)
