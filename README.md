# ai-lore-video-generator

> Generates short vertical 'character lore' videos end-to-end: LLM script (Groq/Llama 3.3), AI images, AI voice-over, OpenCV video assembly.

## Pipeline
1. **Script** — Groq API (`llama-3.3-70b-versatile`) writes the lore of a character, split into segments + one visual prompt per segment (fallback script if the API fails)
2. **Images** — one AI image per segment (Pollinations), fallback image generated with Pillow
3. **Voice-over** — free AI text-to-speech per segment, merged and normalised with `pydub`
4. **Video** — frames assembled with **OpenCV** (`VideoWriter`, 24 fps, 9:16), audio muxed in, temp files cleaned

## Run
```bash
pip install -r requirements.txt
set GROQ_API_KEY=...
python generateur_de_video_lore.py
```
`setup.py` creates a `.env` template for the optional keys.

---
Made by [Tom Galvan](https://tomglv.dev) · Bachelor in AI, ECE Paris
