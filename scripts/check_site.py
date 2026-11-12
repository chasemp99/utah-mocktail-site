"""Site safety check. Run from the repo root: python3 scripts/check_site.py

Fails (exit 1) if the committed pages don't match build-pages.py,
or if a page lost its Analytics tag or canonical link, or has noindex.
"""
import os, re, subprocess, sys, tempfile, filecmp

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ["index", "weddings", "corporate", "packages", "gallery", "reviews", "team"]
GA_ID = "G-688F3T92W2"
problems = []

with tempfile.TemporaryDirectory() as tmp:
    subprocess.run([sys.executable, os.path.join(ROOT, "build-pages.py"), tmp], check=True, stdout=subprocess.DEVNULL)
    for p in PAGES:
        f = p + ".html"
        if not os.path.exists(os.path.join(ROOT, f)):
            problems.append(f"{f} is missing")
        elif not filecmp.cmp(os.path.join(tmp, f), os.path.join(ROOT, f), shallow=False):
            problems.append(f"{f} doesn't match build-pages.py. Edit the script and run `python3 build-pages.py`, don't hand-edit HTML.")

for p in PAGES:
    path = os.path.join(ROOT, p + ".html")
    if not os.path.exists(path):
        continue
    html = open(path, encoding="utf-8").read()
    if f"googletagmanager.com/gtag/js?id={GA_ID}" not in html:
        problems.append(f"{p}.html is missing the Google Analytics tag ({GA_ID})")
    if '<link rel="canonical"' not in html:
        problems.append(f"{p}.html is missing its canonical link")
    if re.search(r'<meta[^>]+name=["\']robots["\'][^>]*noindex', html, re.I):
        problems.append(f"{p}.html has a noindex tag, which hides it from Google")

if problems:
    print("Site check FAILED:")
    for x in problems:
        print(" -", x)
    sys.exit(1)
print(f"Site check passed: {len(PAGES)} pages match build-pages.py and keep tracking + canonical tags.")
