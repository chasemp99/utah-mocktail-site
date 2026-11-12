# Utah Mocktail Co. website

Live at https://utahmocktailco.com, hosted on Cloudflare (Jake's account). Cloudflare republishes about a minute after anything lands on `main`.

**Editing the site? Read [AGENTS.md](AGENTS.md) first.** If you use an AI helper, tell it to read AGENTS.md before making changes.

## How it's built
- `build-pages.py` generates all 7 pages: index, weddings, corporate, packages, gallery, reviews, team. Edit the script, then run `python3 build-pages.py` from this folder.
- `styles.css` holds the look. `design.md` explains the design rules.
- `images/` and the `.mp4` files are the photos and video loops.
- `sitemap.xml` and `robots.txt` are for Google. The Google Analytics tag is `G-688F3T92W2`.
- `scripts/check_site.py` runs on every pull request. It blocks pages that were hand-edited or lost their tracking or Google tags.

The date request form sends to a Google Sheet and emails utahmocktailco@gmail.com.

Built and managed by Chase (Standout).
