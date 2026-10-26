"""Lance le rendu.  Usage :
    python run.py silent    # test rapide, basse qualité, sans voix (vérifier les animations)
    python run.py preview   # basse qualité + ta voix (enregistrement)
    python run.py final     # 1080x1920, 30 fps + ta voix  -> output/git_vs_github.mp4
    python run.py gtts      # final avec voix de synthèse (internet requis)
"""
import glob, os, shutil, subprocess, sys

mode = sys.argv[1] if len(sys.argv) > 1 else "preview"
env = dict(os.environ)
env["VOICE"] = {"silent": "silent", "gtts": "gtts"}.get(mode, "rec")
env["PREVIEW"] = "1" if mode in ("silent", "preview") else "0"

name = f"git_vs_github_{mode}"
cmd = [sys.executable, "-m", "manim", "main.py", "GitVsGithub", "-o", name]
print(">>", " ".join(cmd), f"(VOICE={env['VOICE']}, PREVIEW={env['PREVIEW']})")
subprocess.run(cmd, env=env, check=True)

found = sorted(glob.glob(f"media/videos/**/{name}.mp4", recursive=True), key=os.path.getmtime)
if found:
    os.makedirs("output", exist_ok=True)
    out = os.path.join("output", f"{name}.mp4")
    shutil.copy(found[-1], out)
    print("\nVidéo prête :", out)
