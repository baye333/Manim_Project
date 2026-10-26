# Git vs GitHub — capsule Manim 9:16 avec ta voix

Vidéo verticale (1080×1920, 30 fps, ~60 s) : animations Manim + ta voix enregistrée + sous-titres dynamiques.

## 1. Installation

Python 3.10 à 3.12 recommandé, puis :

```bash
python -m venv venv
# Windows : venv\Scripts\activate      Linux/Mac : source venv/bin/activate
pip install -r requirements.txt
```

Il faut aussi **FFmpeg** (obligatoire), et **Cairo/Pango** sous Linux/Mac :
- Windows : `winget install ffmpeg` (ou `choco install ffmpeg`)
- Ubuntu : `sudo apt install ffmpeg libcairo2-dev libpango1.0-dev pkg-config python3-dev portaudio19-dev`
- Mac : `brew install ffmpeg cairo pango pkg-config portaudio`

Un avertissement « SoX could not be found » est sans conséquence ici.

## 2. Tester les animations (sans voix, en 30 s)

```bash
python run.py silent
```

Sortie : `output/git_vs_github_silent.mp4` (basse qualité, silence calé sur le texte).

## 3. Enregistrer ta voix et rendre la vidéo

```bash
python run.py final
```

Le terminal te présente chaque phrase de `script.py` et enregistre ton micro, phrase par phrase.
Suis les instructions affichées et recommence une phrase si elle ne te plaît pas.
Les enregistrements sont gardés dans `media/voiceovers/` : au rendu suivant, seules les phrases modifiées sont à ré-enregistrer.

Sortie : `output/git_vs_github_final.mp4`

Autres modes : `python run.py preview` (basse qualité + ta voix, pour répéter) et `python run.py gtts` (voix de synthèse, internet requis).

## 4. Personnaliser

| Je veux… | Je modifie… |
|---|---|
| Changer le texte dit / affiché en sous-titres | `script.py` |
| Changer couleurs, polices, zones sûres TikTok | haut de `helpers.py` (`FONT="Poppins"` possible via variable d'environnement) |
| Modifier une scène | la méthode correspondante dans `main.py` (`intro`, `part_git`, `part_github`, `part_link`, `part_recap`, `outro`) |
| Réutiliser pour une autre vidéo | copie `main.py`, change `script.py` et les méthodes de scène : `say()`, `Pill`, `Laptop`, `Cloud`, `Node` sont réutilisables |

Principe à retenir : chaque animation est dans un bloc `with self.say(TEXTE) as tr:` et utilise `tr.duration`
(ex. `run_time=d * 0.3`), ce qui cale automatiquement les images sur ta voix.

## 5. Musique de fond (optionnel)

```bash
ffmpeg -i output/git_vs_github_final.mp4 -i musique.mp3 -filter_complex "[1:a]volume=0.08[m];[0:a][m]amix=inputs=2:duration=first[a]" -map 0:v -map "[a]" -c:v copy output/final_musique.mp4
```

## 6. Conseils d'enregistrement

- Pièce calme, micro à ~15 cm, parle un peu plus lentement que d'habitude.
- Garde 1 phrase = 1 prise ; une pause naturelle d'une demi-seconde en début et fin de prise est normale.
- Zones sûres TikTok : le bas (~20 %) et le bord droit sont masqués par l'interface ; les sous-titres sont placés juste au-dessus.
