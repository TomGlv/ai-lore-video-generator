#!/usr/bin/env python3
"""
Script d'installation et de configuration pour le Générateur de Vidéos Lore TikTok (Version ChatGPT)
"""
import os
import sys
import subprocess
from pathlib import Path

def install_requirements():
    """Installe les dépendances Python"""
    print("📦 Installation des dépendances Python...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dépendances installées avec succès")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'installation des dépendances: {e}")
        return False

def check_ffmpeg():
    """Vérifie si FFmpeg est installé"""
    try:
        subprocess.check_output(['ffmpeg', '-version'], stderr=subprocess.STDOUT)
        print("✅ FFmpeg est installé")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ FFmpeg n'est pas installé")
        print("💡 Installez FFmpeg:")
        print("   - Windows: https://ffmpeg.org/download.html")
        print("   - macOS: brew install ffmpeg")
        print("   - Ubuntu/Debian: sudo apt install ffmpeg")
        return False

def create_env_file():
    """Crée un fichier .env template"""
    env_content = """# Configuration des clés API
# Remplacez les valeurs par vos vraies clés API

# OpenAI API Key (pour ChatGPT et DALL-E 3)
OPENAI_API_KEY=your_openai_key_here

# ElevenLabs API Key (pour la voix-off)
ELEVENLABS_API_KEY=your_elevenlabs_key_here
"""
    
    env_path = Path(".env")
    if not env_path.exists():
        with open(env_path, 'w') as f:
            f.write(env_content)
        print("✅ Fichier .env créé")
        print("📝 Éditez le fichier .env avec vos vraies clés API")
    else:
        print("ℹ️ Fichier .env existe déjà")

def create_directories():
    """Crée les dossiers nécessaires"""
    directories = ['output', 'temp', 'temp/images', 'temp/audio']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("✅ Dossiers créés")

def main():
    """Installation complète"""
    print("🎬 Configuration du Générateur de Vidéos Lore TikTok (Version ChatGPT)")
    print("=" * 70)
    
    # 1. Installation des dépendances
    if not install_requirements():
        print("❌ Impossible de continuer sans les dépendances")
        sys.exit(1)
    
    # 2. Vérification FFmpeg
    if not check_ffmpeg():
        print("⚠️ FFmpeg requis pour le montage vidéo")
    
    # 3. Création du fichier .env
    create_env_file()
    
    # 4. Création des dossiers
    create_directories()
    
    print("\n🎉 Configuration terminée!")
    print("\n📋 Prochaines étapes:")
    print("1. Éditez le fichier .env avec vos clés API")
    print("2. Installez FFmpeg si pas encore fait")
    print("3. Lancez: python lore_video_generator.py")
    
    print("\n🔑 Où obtenir les clés API:")
    print("- OpenAI (ChatGPT + DALL-E): https://platform.openai.com/api-keys")
    print("- ElevenLabs (Voix-off): https://elevenlabs.io/")
    
    print("\n💰 Coûts approximatifs par vidéo:")
    print("- OpenAI (ChatGPT): ~$0.10-0.20")
    print("- OpenAI (DALL-E 3): ~$0.60-1.20 (15 images)")
    print("- ElevenLabs: ~$0.05-0.15")
    print("- Total: ~$0.75-1.55 par vidéo")

if __name__ == "__main__":
    main()