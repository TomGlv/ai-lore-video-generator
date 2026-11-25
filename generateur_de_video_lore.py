#!/usr/bin/env python3
"""
Générateur automatique de vidéos TikTok de lore de personnages
Version ÉPIQUE avec VRAIES IMAGES + VOIX IA GRATUITE
"""

import os
import json
import asyncio
import requests
from pathlib import Path
from typing import List, Dict
import logging
import time
import base64
from io import BytesIO

# Imports pour OpenCV
try:
    import cv2
    import numpy as np
except ImportError:
    print("❌ Installez OpenCV avec: pip install opencv-python numpy")
    import sys
    sys.exit(1)

# Imports pour les images
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("❌ Installez Pillow avec: pip install Pillow")
    import sys
    sys.exit(1)

# Import pour l'audio
try:
    from pydub import AudioSegment
    from pydub.effects import normalize
except ImportError:
    print("❌ Installez pydub avec: pip install pydub")
    import sys
    sys.exit(1)

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LoreVideoGenerator:
    def __init__(self, groq_api_key: str, image_api_key: str = None):
        """Initialise le générateur avec clé API Groq"""
        self.groq_api_key = groq_api_key
        self.image_api_key = image_api_key
        self.groq_api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.groq_model = "llama-3.3-70b-versatile"
        
        # Dossiers de travail
        self.output_dir = Path("output")
        self.temp_dir = Path("temp")
        self.create_directories()
        
        # Configuration vidéo TikTok
        self.video_config = {
            'width': 1080,
            'height': 1920,
            'fps': 24,
            'segment_duration': 4,
            'total_segments': 15
        }
    
    def create_directories(self):
        """Crée les dossiers nécessaires"""
        self.output_dir.mkdir(exist_ok=True)
        self.temp_dir.mkdir(exist_ok=True)
        (self.temp_dir / "images").mkdir(exist_ok=True)
        (self.temp_dir / "audio").mkdir(exist_ok=True)
    
    def generate_lore_with_groq(self, character_name: str) -> Dict:
        """Génère le lore ÉPIQUE avec l'API Groq"""
        logger.info(f"🤖 Récupération du lore ÉPIQUE de {character_name} via Groq AI...")
        
        try:
            prompt = f"""Tu es un MAÎTRE CONTEUR ÉPIQUE, spécialiste des narrations dramatiques et captivantes pour les réseaux sociaux.

🎭 MISSION : Raconte l'histoire COMPLÈTE et le lore du personnage "{character_name}" en EXACTEMENT 15 segments ÉPIQUES et DRAMATIQUES.

📜 STYLE DE NARRATION EXIGÉ :
- Ton CINÉMATIQUE et ÉPIQUE (comme les bandes-annonces de films)
- Phrases PERCUTANTES avec impact émotionnel fort
- Vocabulaire DRAMATIQUE et ÉVOCATEUR
- Créer du SUSPENSE et de l'ÉMOTION
- Utiliser des tournures narratives engageantes
- Donner envie de connaître la suite à chaque segment

✨ STRUCTURE DE CHAQUE SEGMENT :
- 1-2 phrases maximum (20-40 mots)
- CAPTIVANT dès les premiers mots
- Focus sur un moment CLÉ (origine mystérieuse, révélation choc, bataille légendaire, sacrifice héroïque, transformation épique)
- Respecter le LORE OFFICIEL du personnage
- Créer une PROGRESSION NARRATIVE cohérente

🎬 EXEMPLE DE TON ÉPIQUE :
❌ PAS ÇA : "Il est né dans un village."
✅ MAIS ÇA : "Dans les ténèbres d'une nuit sans lune, une prophétie ancestrale s'accomplit..."

🎨 DESCRIPTIONS VISUELLES :
Pour CHAQUE segment, fournis une description visuelle ULTRA-DÉTAILLÉE pour générer une image cinématique :
- Style artistique (realistic, cinematic, epic fantasy, dark atmosphere, etc.)
- Éclairage et ambiance (dramatic lighting, volumetric fog, golden hour, etc.)
- Composition et angle de vue (wide shot, close-up, aerial view, etc.)
- Détails spécifiques du personnage et de la scène
- Palette de couleurs dominante

📋 FORMAT DE RÉPONSE (JSON STRICT) :
{{
  "title": "Titre ÉPIQUE et ACCROCHEUR (ex: 'La Légende Oubliée de...', 'L'Ascension Sanglante de...')",
  "segments": [
    "Segment 1 : Accroche ÉPIQUE qui donne envie...",
    "Segment 2 : Révélation DRAMATIQUE...",
    "Segment 3 : Moment CLÉ captivant...",
    ...15 segments ÉPIQUES au total
  ],
  "visual_prompts": [
    "Ultra detailed cinematic description for segment 1, dramatic lighting, epic composition, [character details], [scene details], [mood and atmosphere], 8k, highly detailed",
    "Description segment 2...",
    ...15 descriptions DÉTAILLÉES
  ]
}}

🎯 PERSONNAGE À ANALYSER : {character_name}

Crée maintenant une narration ÉPIQUE qui donnera des FRISSONS et captivera l'audience du début à la fin !"""

            headers = {
                "Authorization": f"Bearer {self.groq_api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.groq_model,
                "messages": [
                    {
                        "role": "system",
                        "content": "Tu es un MAÎTRE CONTEUR ÉPIQUE, expert en narration dramatique, lore de personnages légendaires et storytelling cinématique. Tu crées des histoires qui donnent des FRISSONS et captivent l'audience. Ton style est DRAMATIQUE, ÉPIQUE et ÉMOTIONNEL. Tu connais parfaitement les personnages de fiction, jeux vidéo, films, séries, anime et mangas."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.9,  # Plus créatif pour un style épique
                "max_tokens": 4000,
                "response_format": {"type": "json_object"}
            }
            
            logger.info("📡 Envoi de la requête à Groq...")
            response = requests.post(
                self.groq_api_url,
                headers=headers,
                json=payload,
                timeout=45
            )
            
            if response.status_code != 200:
                logger.error(f"Erreur API Groq: {response.status_code} - {response.text}")
                raise Exception(f"API Groq erreur {response.status_code}")
            
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            logger.info("✅ Lore ÉPIQUE reçu de Groq")
            
            lore_data = json.loads(content)
            
            if 'segments' not in lore_data:
                raise Exception("Format de réponse invalide")
            
            segments = lore_data['segments']
            visual_prompts = lore_data.get('visual_prompts', [])
            
            # S'assurer qu'on a exactement 15 segments
            if len(segments) < 15:
                logger.warning(f"Seulement {len(segments)} segments reçus, padding...")
                while len(segments) < 15:
                    segments.append(f"Et la légende de {character_name} résonne encore à travers les âges, immortelle et éternelle.")
            elif len(segments) > 15:
                segments = segments[:15]
            
            # S'assurer qu'on a 15 visual prompts
            if len(visual_prompts) < 15:
                for i in range(len(visual_prompts), 15):
                    visual_prompts.append(f"{character_name} in an epic cinematic scene, dramatic lighting, highly detailed, 8k quality, trending on artstation")
            elif len(visual_prompts) > 15:
                visual_prompts = visual_prompts[:15]
            
            logger.info(f"✅ {len(segments)} segments ÉPIQUES générés avec descriptions visuelles détaillées")
            
            return {
                "lore": " ".join(segments),
                "title": lore_data.get('title', f"La Légende de {character_name}"),
                "segments": segments,
                "visual_prompts": visual_prompts
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur Groq AI: {e}")
            return self.generate_lore_fallback(character_name)
    
    def generate_lore_fallback(self, character_name: str) -> Dict:
        """Fallback ÉPIQUE si l'API ne fonctionne pas"""
        logger.info("📝 Génération du lore ÉPIQUE en mode fallback...")
        
        segments = [
            f"Dans les ténèbres d'un monde oublié, {character_name} vit le jour sous un ciel déchiré par la foudre.",
            f"Les anciennes prophéties murmurent son nom depuis des millénaires, annonçant l'arrivée d'un destin hors du commun.",
            f"Dès ses premiers pas, une puissance ancestrale coule dans ses veines, terrifiante et magnifique à la fois.",
            f"Les sages tremblent en reconnaissant les signes : une légende vivante marche parmi eux.",
            f"Le destin l'appelle vers une quête impossible : affronter les ténèbres qui menacent d'engloutir toute existence.",
            f"Chaque épreuve forge son âme dans les flammes de l'adversité, le transformant en guerrier légendaire.",
            f"Ses ennemis tombent un à un, pétrifiés par la puissance dévastatrice qui émane de son être.",
            f"Pourtant, derrière cette force incommensurable se cache une humilité qui touche les cœurs les plus endurcis.",
            f"Les plus grands héros se rallient à sa cause, unis par un serment de sang et d'honneur éternel.",
            f"Ensemble, ils affrontent des batailles si épiques que les dieux eux-mêmes retiennent leur souffle.",
            f"Les cieux s'embrasent, la terre tremble, et l'histoire du monde bascule sous leurs coups titanesques.",
            f"Son courage inspire des générations entières, transformant le désespoir en une flamme d'espoir inextinguible.",
            f"Dans l'obscurité la plus totale, sa vraie nature se révèle : un phénix né des cendres de l'apocalypse.",
            f"Son sacrifice ultime bouleverse l'ordre du cosmos, gravant son nom dans l'éternité même.",
            f"Aujourd'hui encore, {character_name} règne comme une légende immortelle, symbole éternel de courage et de détermination."
        ]
        
        visual_prompts = [
            f"{character_name} epic birth scene, dramatic stormy sky, lightning, dark atmosphere, cinematic, 8k",
            f"{character_name} ancient prophecy scene, mystical symbols, glowing runes, ethereal lighting",
            f"{character_name} young warrior, power awakening, energy aura, dramatic lighting",
            f"{character_name} surrounded by ancient sages, temple setting, mystical atmosphere",
            f"{character_name} standing before darkness, epic scale, dramatic composition",
            f"{character_name} intense training montage, fire and steel, dynamic action",
            f"{character_name} epic battle scene, defeated enemies, dramatic lighting",
            f"{character_name} humble moment, emotional scene, soft dramatic lighting",
            f"{character_name} with legendary heroes, epic group shot, cinematic composition",
            f"{character_name} massive epic battle, destruction, gods watching, grand scale",
            f"{character_name} apocalyptic battle, earth shattering, cosmic scale, dramatic",
            f"{character_name} inspiring others, hope and light, emotional cinematic scene",
            f"{character_name} phoenix transformation, fire and rebirth, spectacular visual",
            f"{character_name} ultimate sacrifice, emotional peak, dramatic composition",
            f"{character_name} legendary immortal form, eternal and powerful, epic finale"
        ]
        
        return {
            "lore": " ".join(segments),
            "title": f"La Légende Éternelle de {character_name}",
            "segments": segments,
            "visual_prompts": visual_prompts
        }
    
    def generate_voice_with_tts(self, text: str, index: int) -> str:
        """Génère un fichier audio avec TTS gratuit (gTTS ou edge-tts)"""
        try:
            logger.info(f"🎙️ Génération voix segment {index + 1}/15...")
            
            audio_path = self.temp_dir / "audio" / f"audio_{index:02d}.mp3"
            
            # Utiliser edge-tts (gratuit, voix Microsoft de qualité)
            try:
                import subprocess
                
                # Voix française masculine dramatique
                voice = "fr-FR-HenriNeural"  # Voix masculine française
                
                # Commande edge-tts
                cmd = [
                    "edge-tts",
                    "--voice", voice,
                    "--text", text,
                    "--write-media", str(audio_path),
                    "--rate=+5%",  # Légèrement plus rapide pour dynamisme
                    "--pitch=+0Hz"  # Ton normal
                ]
                
                subprocess.run(cmd, check=True, capture_output=True)
                
                if audio_path.exists():
                    logger.info(f"✅ Voix générée pour segment {index + 1}")
                    return str(audio_path)
                else:
                    raise Exception("Fichier audio non créé")
                    
            except Exception as e:
                logger.warning(f"Edge-TTS non disponible: {e}")
                # Fallback vers gTTS
                from gtts import gTTS
                
                tts = gTTS(text=text, lang='fr', slow=False)
                tts.save(str(audio_path))
                
                logger.info(f"✅ Voix générée (gTTS) pour segment {index + 1}")
                return str(audio_path)
                
        except Exception as e:
            logger.error(f"❌ Erreur génération voix {index + 1}: {e}")
            # Créer un silence de 4 secondes en fallback
            return self.create_silent_audio(index)
    
    def create_silent_audio(self, index: int) -> str:
        """Crée un fichier audio silencieux de 4 secondes"""
        audio_path = self.temp_dir / "audio" / f"audio_{index:02d}.mp3"
        
        # Créer un silence de 4 secondes
        silence = AudioSegment.silent(duration=4000)
        silence.export(str(audio_path), format="mp3")
        
        return str(audio_path)
    
    def generate_image_with_pollinations(self, prompt: str, index: int) -> str:
        """Génère une image avec l'API Pollinations.AI (GRATUIT)"""
        try:
            # Améliorer le prompt pour un style cinématique ÉPIQUE
            enhanced_prompt = f"{prompt}, epic cinematic scene, dramatic lighting, highly detailed, 8k quality, masterpiece, trending on artstation, professional photography"
            
            # URL de l'API Pollinations (gratuite, pas de clé nécessaire)
            url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(enhanced_prompt)}"
            params = {
                "width": 1080,
                "height": 1920,
                "nologo": "true",
                "model": "flux",
                "enhance": "true"
            }
            
            logger.info(f"🎨 Génération image ÉPIQUE {index + 1}/15...")
            
            response = requests.get(url, params=params, timeout=60)
            
            if response.status_code == 200:
                # Sauvegarder l'image
                image_path = self.temp_dir / "images" / f"image_{index:02d}.png"
                
                img = Image.open(BytesIO(response.content))
                img = img.resize((1080, 1920), Image.Resampling.LANCZOS)
                img.save(image_path, format='PNG')
                
                logger.info(f"✅ Image ÉPIQUE {index + 1}/15 générée")
                return str(image_path)
            else:
                raise Exception(f"Erreur API: {response.status_code}")
                
        except Exception as e:
            logger.error(f"❌ Erreur génération image {index + 1}: {e}")
            # Créer une image de fallback simple
            return self.create_fallback_image(prompt, index)
    
    def create_fallback_image(self, prompt: str, index: int) -> str:
        """Crée une image de fallback si la génération échoue"""
        logger.info(f"📝 Création image fallback {index + 1}/15...")
        
        # Créer une image simple avec le texte
        img = Image.new('RGB', (1080, 1920), (20, 20, 30))
        draw = ImageDraw.Draw(img)
        
        # Essayer de charger une police
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 40)
            except:
                font = ImageFont.load_default()
        
        # Écrire le prompt en multi-lignes
        words = prompt.split()
        lines = []
        current_line = ""
        max_width = 950
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            try:
                bbox = draw.textbbox((0, 0), test_line, font=font)
                if bbox[2] - bbox[0] <= max_width:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
            except:
                if len(test_line) <= 30:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Centrer le texte verticalement
        y_start = 960 - (len(lines) * 50) // 2
        
        for line in lines:
            try:
                bbox = draw.textbbox((0, 0), line, font=font)
                line_width = bbox[2] - bbox[0]
                x = (1080 - line_width) // 2
                draw.text((x, y_start), line, fill=(255, 255, 255), font=font)
            except:
                draw.text((50, y_start), line, fill=(255, 255, 255), font=font)
            y_start += 50
        
        # Sauvegarder
        image_path = self.temp_dir / "images" / f"image_{index:02d}.png"
        img.save(image_path, format='PNG')
        
        return str(image_path)
    
    def create_images_and_audio(self, segments: List[str], visual_prompts: List[str], character_name: str) -> tuple:
        """Génère toutes les images ET les audios"""
        logger.info("🎨 Génération des images et voix IA...")
        
        image_paths = []
        audio_paths = []
        
        for i, (segment, prompt) in enumerate(zip(segments, visual_prompts)):
            # Générer l'image
            full_prompt = f"{character_name}, {prompt}"
            image_path = self.generate_image_with_pollinations(full_prompt, i)
            image_paths.append(image_path)
            
            # Générer la voix pour ce segment
            audio_path = self.generate_voice_with_tts(segment, i)
            audio_paths.append(audio_path)
            
            # Petit délai pour ne pas surcharger les APIs
            time.sleep(1.5)
        
        return image_paths, audio_paths
    
    def merge_audio_files(self, audio_paths: List[str]) -> str:
        """Fusionne tous les fichiers audio en un seul"""
        logger.info("🎵 Fusion des fichiers audio...")
        
        try:
            combined = AudioSegment.empty()
            
            for audio_path in audio_paths:
                audio = AudioSegment.from_mp3(audio_path)
                
                # Ajuster la durée à exactement 4 secondes
                target_duration = 4000  # 4 secondes en ms
                
                if len(audio) < target_duration:
                    # Ajouter du silence si trop court
                    silence = AudioSegment.silent(duration=target_duration - len(audio))
                    audio = audio + silence
                elif len(audio) > target_duration:
                    # Couper si trop long
                    audio = audio[:target_duration]
                
                combined += audio
            
            # Normaliser le volume
            combined = normalize(combined)
            
            # Sauvegarder
            final_audio_path = self.temp_dir / "final_audio.mp3"
            combined.export(str(final_audio_path), format="mp3", bitrate="192k")
            
            logger.info(f"✅ Audio fusionné: {len(combined)/1000:.1f}s")
            return str(final_audio_path)
            
        except Exception as e:
            logger.error(f"❌ Erreur fusion audio: {e}")
            return None
    
    def create_video_with_audio(self, images: List[str], audio_path: str, character_name: str) -> str:
        """Crée la vidéo avec images et audio"""
        logger.info("🎞️ Montage de la vidéo avec audio...")
        
        try:
            width = self.video_config['width']
            height = self.video_config['height']
            fps = self.video_config['fps']
            segment_duration = self.video_config['segment_duration']
            
            timestamp = int(time.time())
            video_no_audio = self.temp_dir / "video_no_audio.mp4"
            output_path = self.output_dir / f"lore_{character_name.replace(' ', '_')}_{timestamp}.mp4"
            
            # Codec H.264 pour compatibilité TikTok
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video_writer = cv2.VideoWriter(
                str(video_no_audio),
                fourcc,
                fps,
                (width, height)
            )
            
            if not video_writer.isOpened():
                raise Exception("Impossible d'ouvrir le VideoWriter")
            
            # Pour chaque image, créer les frames
            for i, image_path in enumerate(images):
                logger.info(f"Traitement segment {i+1}/15...")
                
                # Charger l'image avec PIL puis convertir en OpenCV
                pil_img = Image.open(image_path)
                pil_img = pil_img.resize((width, height), Image.Resampling.LANCZOS)
                
                # Convertir PIL -> NumPy -> OpenCV (BGR)
                frame = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
                
                # Écrire le nombre de frames pour la durée souhaitée
                num_frames = fps * segment_duration
                for _ in range(num_frames):
                    video_writer.write(frame)
            
            video_writer.release()
            
            # Ajouter l'audio avec ffmpeg
            if audio_path and Path(audio_path).exists():
                logger.info("🎵 Ajout de l'audio à la vidéo...")
                
                import subprocess
                
                cmd = [
                    'ffmpeg',
                    '-i', str(video_no_audio),
                    '-i', str(audio_path),
                    '-c:v', 'copy',
                    '-c:a', 'aac',
                    '-strict', 'experimental',
                    '-shortest',
                    '-y',
                    str(output_path)
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode != 0:
                    logger.warning(f"Erreur ffmpeg: {result.stderr}")
                    # Si ffmpeg échoue, utiliser la vidéo sans audio
                    import shutil
                    shutil.copy(video_no_audio, output_path)
            else:
                # Pas d'audio disponible
                import shutil
                shutil.copy(video_no_audio, output_path)
            
            if output_path.exists() and output_path.stat().st_size > 0:
                file_size_mb = output_path.stat().st_size / (1024 * 1024)
                logger.info(f"✅ Vidéo créée: {file_size_mb:.2f} MB")
                return str(output_path)
            else:
                raise Exception("Fichier vidéo invalide")
            
        except Exception as e:
            logger.error(f"❌ Erreur montage vidéo: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def cleanup_temp_files(self):
        """Nettoie les fichiers temporaires"""
        import shutil
        try:
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir)
            self.create_directories()
            logger.info("🧹 Nettoyage terminé")
        except Exception as e:
            logger.warning(f"Erreur nettoyage: {e}")
    
    async def generate_full_video(self, character_name: str) -> str:
        """Pipeline complet de génération ÉPIQUE"""
        try:
            logger.info(f"🎬 Génération ÉPIQUE pour: {character_name}")
            
            # 1. Génération du lore ÉPIQUE
            lore_data = self.generate_lore_with_groq(character_name)
            
            # 2. Génération des images IA + voix IA
            image_paths, audio_paths = self.create_images_and_audio(
                lore_data['segments'],
                lore_data['visual_prompts'],
                character_name
            )
            
            # 3. Fusion des audios
            final_audio = self.merge_audio_files(audio_paths)
            
            # 4. Montage vidéo avec audio
            video_path = self.create_video_with_audio(image_paths, final_audio, character_name)
            
            logger.info(f"✅ Vidéo ÉPIQUE terminée: {video_path}")
            return video_path
            
        except Exception as e:
            logger.error(f"❌ Erreur génération: {e}")
            raise
        finally:
            try:
                self.cleanup_temp_files()
            except:
                pass

def main():
    """Fonction principale"""
    print("🎬 Générateur de Vidéos TikTok Lore ÉPIQUE avec VOIX IA")
    print("=" * 70)
    
    # ⚠️ METTEZ VOTRE CLÉ API GROQ ICI ⚠️
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
    
    if GROQ_API_KEY == "VOTRE_NOUVELLE_CLE_API_ICI":
        print("❌ ERREUR: Vous devez mettre votre clé API Groq")
        print("📝 Obtenez votre clé sur: https://console.groq.com/keys")
        return
    
    print("✅ Fonctionnalités ÉPIQUES:")
    print("   - Narration ÉPIQUE et DRAMATIQUE via Groq AI")
    print("   - Génération de VRAIES IMAGES cinématiques (Pollinations.AI)")
    print("   - VOIX IA GRATUITE française (edge-tts ou gTTS)")
    print("   - Audio synchronisé avec les images")
    print("   - Format: 1080x1920 (TikTok)")
    print("   - 15 segments × 4s = 60 secondes")
    print("   - ⏱️  Temps estimé: 3-4 minutes par vidéo")
    print()
    print("📦 Dépendances requises:")
    print("   pip install opencv-python numpy Pillow pydub gtts edge-tts")
    print("   (+ ffmpeg installé sur votre système)")
    print()
    
    generator = LoreVideoGenerator(groq_api_key=GROQ_API_KEY)
    
    while True:
        character_name = input("🎭 Nom du personnage (ou 'quit'): ").strip()
        
        if character_name.lower() in ['quit', 'q', 'exit']:
            print("👋 Au revoir!")
            break
        
        if not character_name:
            print("❌ Entrez un nom valide")
            continue
        
        try:
            print(f"\n⏳ Génération ÉPIQUE en cours... (cela peut prendre 3-4 minutes)")
            video_path = asyncio.run(generator.generate_full_video(character_name))
            print(f"\n🎉 Vidéo ÉPIQUE générée avec VOIX IA!")
            print(f"📁 Fichier: {video_path}")
            print(f"📱 Format: 1080x1920 (TikTok)")
            print(f"⏱️ Durée: 60 secondes")
            print(f"🤖 Lore: Groq AI (ÉPIQUE)")
            print(f"🎨 Images: Pollinations.AI (Cinématiques)")
            print(f"🎙️ Voix: IA française (edge-tts/gTTS)")
            print(f"🎵 Audio: Synchronisé avec la vidéo")
            print()
            
        except KeyboardInterrupt:
            print("\n⏸️ Arrêté par l'utilisateur")
            generator.cleanup_temp_files()
            break
        except Exception as e:
            print(f"❌ Erreur: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()