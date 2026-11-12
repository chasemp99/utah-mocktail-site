"""Builds the Utah Mocktail Co. static pages from shared pieces.

Usage (from the repo root):  python3 build-pages.py
This rewrites the 7 .html pages in this folder. Commit the script AND the pages together.
Never edit the .html files by hand: the next build overwrites them. Rules for editors: AGENTS.md.
Output is plain HTML, so Cloudflare needs no build step. Design rules live in design.md.
"""
import sys, os, re

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
BIZ = "Utah Mocktail Co."
FOUNDER = "Jacob"
EMAIL = "utahmocktailco@gmail.com"
PHONE = "(928) 266-8863"
TEL = "+19282668863"
# Google Apps Script web app that saves each "Reserve your date" request to a Google Sheet and emails the team.
# Lives in Chase's Google account. Don't change this URL.
GA_ID = "G-688F3T92W2"  # Google Analytics 4, property "utahmocktailco.com"
FORM_URL = "https://script.google.com/macros/s/AKfycbwHHXpcNrJrIC-XcgOLXBQ7OhWbu58uSoJqrqlbmUCXUFE70B-InwVYyIa-P2md5CR05A/exec"
IG_HANDLE = "utahmocktailco"
IG_URL = f"https://www.instagram.com/{IG_HANDLE}/"
IG_ICON = '<svg class="ig" viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.4" cy="6.6" r="1.1" fill="currentColor" stroke="none"/></svg>'


NAV = [
    ("index.html", "Home"),
    ("weddings.html", "Weddings"),
    ("corporate.html", "Corporate"),
    ("packages.html", "Packages"),
    ("gallery.html", "Gallery"),
    ("reviews.html", "Reviews"),
    ("team.html", "The Team"),
]

SCHEMA = f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "{BIZ}",
  "description": "Mobile mocktail bar for weddings, corporate events and parties in Utah.",
  "image": "https://utahmocktailco.com/images/capitol-bar.jpg",
  "email": "{EMAIL}",
  "telephone": "+1-928-266-8863",
  "priceRange": "$650-$1,995+",
  "founder": {{"@type": "Person", "name": "{FOUNDER}"}},
  "address": {{"@type": "PostalAddress", "addressRegion": "UT", "addressCountry": "US"}},
  "areaServed": ["Utah County", "Salt Lake County", "Davis County", "Weber County", "Summit County", "Wasatch County", "Southern Utah"],
  "url": "https://utahmocktailco.com/",
  "logo": "https://utahmocktailco.com/images/logo.png",
  "sameAs": ["https://www.instagram.com/utahmocktailco/"]
}}
</script>"""


def head(title, desc, schema=False, over_hero=False):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>window.dataLayer = window.dataLayer || []; function gtag(){{dataLayer.push(arguments);}} gtag('js', new Date()); gtag('config', '{GA_ID}');</script>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Inter:wght@400;500;600&display=swap">
<link rel="icon" type="image/png" href="favicon.png">
<link rel="stylesheet" href="styles.css">
{SCHEMA if schema else ''}
<script>document.documentElement.classList.add('js');</script>
</head>
<body{' class="over-hero"' if over_hero else ''}>
"""


LEFT_NAV = [("weddings.html", "Weddings"), ("corporate.html", "Corporate"), ("packages.html", "Packages"), ("gallery.html", "Gallery")]
RIGHT_NAV = [("reviews.html", "Reviews"), ("team.html", "The Team")]


def header(current):
    def links(items, indent):
        out = []
        for href, label in items:
            cur = ' aria-current="page"' if href == current else ""
            out.append(f'{indent}<li><a href="{href}"{cur}>{label}</a></li>')
        return "\n".join(out)
    return f"""<header class="top">
  <div class="wrap">
    <nav class="main left" aria-label="Main">
      <ul>
{links(LEFT_NAV, '        ')}
      </ul>
    </nav>
    <a class="logo" href="index.html"><img src="images/logo-180.png" alt="" width="52" height="52"><span>Utah Mocktail <i>Co.</i></span></a>
    <nav class="main right" aria-label="More">
      <ul>
{links(RIGHT_NAV, '        ')}
        <li><a class="ig-link" href="{IG_URL}" aria-label="Instagram @{IG_HANDLE}">{IG_ICON}</a></li>
        <li><a class="book" href="#book">Reserve your date</a></li>
      </ul>
    </nav>
    <details class="menu-toggle">
      <summary>Menu</summary>
      <ul>
{links(NAV, '        ')}
        <li><a href="{IG_URL}">Instagram @{IG_HANDLE}</a></li>
        <li><a href="#book">Reserve your date</a></li>
      </ul>
    </details>
  </div>
</header>
"""


EVENT_TYPES = ["Wedding or reception", "Corporate or conference", "Shower or birthday", "Graduation or reunion", "School or university event", "Religious or community gathering", "Something else"]


def contact(default_type="Wedding or reception"):
    o = "".join(f"<option{' selected' if x == default_type else ''}>{x}</option>" for x in EVENT_TYPES)
    return f"""  <section class="contact" id="book">
    <div class="wrap">
      <div class="copy">
        <p class="eyebrow">Reserve your date</p>
        <h2>Let’s plan <em>your event.</em></h2>
        <p>Send a few details and our team will get back to you with availability and a quote. No obligation.</p>
        <ul class="checks">
          <li>Free, no-obligation quote</li>
          <li>Based in Utah County, serving statewide</li>
          <li>Destination events considered</li>
        </ul>
        <dl>
          <dt>Instagram</dt><dd><a class="ig-inline" href="{IG_URL}">{IG_ICON}@{IG_HANDLE}</a></dd>
          <dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd>
          <dt>Phone</dt><dd><a href="tel:{TEL}">{PHONE}</a></dd>
        </dl>
      </div>
      <form id="inquiry" class="form-card" novalidate>
        <label>Name<input id="f-name" name="name" autocomplete="name" placeholder="Your name" required></label>
        <label>Email<input id="f-email" name="email" type="email" autocomplete="email" placeholder="you@email.com" required></label>
        <label>Event date<input id="f-date" name="date" type="date"></label>
        <label>Guest count<input id="f-guests" name="guests" type="number" min="1" inputmode="numeric" placeholder="e.g. 80"></label>
        <label class="full">Venue or city<input id="f-venue" name="venue" placeholder="e.g. Hobble Creek Manor, Springville"></label>
        <label>Type of event
          <select id="f-type" name="type">{o}</select>
        </label>
        <label>Package
          <select id="f-pkg" name="package"><option>Not sure yet</option>{"".join(f"<option>{x[0]} ({x[2]})</option>" for x in PACKAGES)}</select>
        </label>
        <label class="full">Anything else?<textarea id="f-msg" name="message" placeholder="Location, vibe, must-have flavors..."></textarea></label>
        <label class="hp" aria-hidden="true">Company<input name="company" tabindex="-1" autocomplete="off"></label>
        <button class="btn full" type="submit">Reserve my date</button>
        <p class="form-note full" id="form-note" role="status"></p>
      </form>
    </div>
  </section>
"""


FOOT = f"""<footer>
  <div class="foot-top">
    <img src="images/logo-180.png" alt="{BIZ} logo" width="88" height="88" loading="lazy">
    <a class="ig-inline" href="{IG_URL}">{IG_ICON}@{IG_HANDLE}</a>
  </div>
  <div class="wrap">
    <div><strong>{BIZ}</strong>Mobile mocktail bar based in Utah County.<br><a href="tel:{TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></div>
    <div><strong>Events</strong><a href="weddings.html">Weddings</a><br><a href="corporate.html">Corporate events</a><br><a href="#book">Showers, birthdays and graduations</a></div>
    <div><strong>Where we pour</strong>Utah County, Salt Lake, Davis, Weber, Summit, Wasatch and Southern Utah</div>
    <div><strong>&nbsp;</strong>© 2026 {BIZ}</div>
  </div>
</footer>

<a class="float-book" href="#book">Reserve your date</a>

<dialog id="thanks" class="thanks" aria-labelledby="thanks-title">
  <h2 id="thanks-title">Thanks!</h2>
  <p>We’ve received your request. A member of our team will reach out soon.</p>
  <form method="dialog"><button class="btn">Close</button></form>
</dialog>

<script>
// Date form: sends to the Google Sheet web app (FORM_URL), which also emails our team.
document.getElementById('inquiry').addEventListener('submit', function (e) {{
  e.preventDefault();
  var f = this, note = document.getElementById('form-note'), btn = f.querySelector('button[type=submit]');
  var url = '{FORM_URL}';
  if (!f.elements['name'].value.trim() || !/^\\S+@\\S+\\.\\S+$/.test(f.elements['email'].value.trim())) {{
    note.textContent = 'Please add your name and a valid email so we can reach you.';
    return;
  }}
  var data = new URLSearchParams(new FormData(f));
  data.append('page', location.pathname);
  btn.disabled = true;
  note.textContent = 'Sending...';
  fetch(url, {{ method: 'POST', mode: 'no-cors', body: data }})
    .then(function () {{ f.reset(); note.textContent = ''; if (window.gtag) gtag('event', 'generate_lead', {{ form: 'date_request' }}); var d = document.getElementById('thanks'); if (d.showModal) d.showModal(); else note.textContent = d.querySelector('p').textContent; }})
    .catch(function () {{ note.textContent = 'That didn’t go through. Please email {EMAIL} or call {PHONE}.'; }})
    .then(function () {{ btn.disabled = false; }});
}});

// Scroll effects: the header turns solid past the video and photos ease in once.
// Both are off with "reduce motion".
(function () {{
  var still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var header = document.querySelector('header.top');
  if (still) {{ document.documentElement.classList.add('no-motion'); document.documentElement.classList.remove('js'); }}
  function onScroll() {{ header.classList.toggle('scrolled', window.scrollY > 40); }}
  // Floating "Reserve your date" button: shows after the first screen, hides while the form is on screen.
  var fb = document.querySelector('.float-book');
  var form = document.getElementById('book');
  var formOn = false;
  function showFloat() {{ if (fb) fb.classList.toggle('show', window.scrollY > window.innerHeight * 0.6 && !formOn); }}
  if (fb && form && 'IntersectionObserver' in window) {{
    new IntersectionObserver(function (en) {{ formOn = en[0].isIntersecting; showFloat(); }}).observe(form);
  }}
  window.addEventListener('scroll', showFloat, {{ passive: true }});
  // Package cards: swipe on phones, arrow buttons on computers.
  document.querySelectorAll('.swipe-wrap').forEach(function (w) {{
    var row = w.querySelector('.swipe-row');
    w.querySelectorAll('[data-dir]').forEach(function (b) {{
      b.addEventListener('click', function () {{ row.scrollBy({{ left: b.dataset.dir * row.clientWidth * 0.8, behavior: still ? 'auto' : 'smooth' }}); }});
    }});
  }});
  window.addEventListener('scroll', onScroll, {{ passive: true }});
  window.addEventListener('resize', onScroll);
  onScroll();
  if (!still && 'IntersectionObserver' in window) {{
    var io = new IntersectionObserver(function (entries) {{
      entries.forEach(function (e) {{ if (e.isIntersecting) {{ e.target.classList.add('in'); io.unobserve(e.target); }} }});
    }}, {{ rootMargin: '0px 0px -10% 0px' }});
    document.querySelectorAll('.reveal').forEach(function (el) {{ io.observe(el); }});
  }} else {{
    document.querySelectorAll('.reveal').forEach(function (el) {{ el.classList.add('in'); }});
  }}
}})();
</script>
</body>
</html>
"""

# Order follows the old site's scrolling names strip
DRINKS = [
    ("Lavender Lime Cooler", "Citrus, a little lavender, sparkling"),
    ("Cherry Parson", "Cherry balanced with citrus"),
    ("Berry Basil", "Fresh berries with basil"),
    ("Mint Mojito", "Fresh mint and lime"),
    ("Coco Kiwi", "Coconut and kiwi"),
    ("Strawberry Lime Sparkler", "Strawberry, lime, sparkling"),
    ("Lychee Rose", "Lychee with a floral finish"),
    ("White Peach & Elderflower", "White peach and elderflower"),
    ("Honey Blackberry Smash", "Blackberry, honey and citrus"),
    ("Citrus Refresher", "Bright citrus, coconut, sparkling"),
]

# Drink cards, text from the old site: file, width, height, name, description, alt
SIGNATURES = [
    ("berry-highball.jpg", 1023, 1537, "Lavender Lime Cooler", "Refreshing citrus balanced with subtle lavender and a sparkling, bright finish.", "A purple Lavender Lime Cooler with a lime wheel on the bar"),
    ("cherry-sour.jpg", 1066, 1600, "Cherry Parson", "Bold cherry flavors balanced with citrus and a smooth, sophisticated finish.", "A Cherry Parson with a cherry garnish"),
    ("mint-spritz.jpg", 1066, 1600, "Mint Mojito", "Fresh mint and lime come together in a crisp, refreshing, alcohol-free classic.", "A Mint Mojito with fresh mint and a lime wedge"),
    ("strawberry-sparkler.jpg", 941, 1176, "Strawberry Lime Sparkler", "Sweet strawberries and fresh lime with a lively, sparkling finish. A crowd favorite.", "A tall red Strawberry Lime Sparkler with a strawberry and lime garnish"),
]

# name, for, price, guests, hours, drinks, staff, extra, popular
PACKAGES = [
    ("Sweet & Simple", "Intimate gatherings", "$650", "Up to 75", "2 hours", "2 signature drinks", "1 bartender", "Styled bar setup", False),
    ("Signature Celebration", "Weddings and special events", "$995", "Up to 125", "3 hours", "3 signature drinks", "2 bartenders", "Extra garnish and a custom menu sign", True),
    ("Luxe Dry Bar", "Bigger celebrations", "$1,295", "Up to 200", "4 hours", "4 custom drinks", "2 to 3 bartenders", "Menu planning call before the event", False),
    ("Grand Event", "Large events", "$1,995", "Up to 400", "4 hours", "2 fast-pour signature drinks", "3 or more bartenders", "Full bar setup built for quick lines", False),
]

# From the old site's "Everything included" grid; glassware per Chase (2026-10-27)
INCLUDED = ["Professional beverage service", "Signature mocktails", "All ingredients", "Premium syrups &amp; mixers", "Fresh garnishes", "Ice", "Real glassware &amp; serving supplies", "Styled bar setup", "Menu display", "Setup &amp; cleanup"]

ARROW = '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'


def package_cards():
    cards = []
    for name, for_, price, guests, hours, drinks, staff, extra, pop in PACKAGES:
        badge = '<span class="badge">Most popular</span>' if pop else ""
        cards.append(f"""        <article class="card{' popular' if pop else ''}">
          {badge}
          <h3>{name}</h3>
          <p class="for">{for_}</p>
          <p class="price">from {price}</p>
          <ul>
            <li><strong>{guests}</strong> guests</li>
            <li>{hours} of service</li>
            <li>{drinks}</li>
            <li>{staff}</li>
            <li>{extra}</li>
          </ul>
          <a class="btn btn-light" href="#book">Reserve your date</a>
        </article>""")
    return f"""  <section class="packages" id="packages">
    <div class="wrap swipe-wrap">
      <div class="swipe-head">
        <p class="swipe-hint">Swipe to see all four packages</p>
        <div class="swipe-btns">
          <button type="button" data-dir="-1" aria-label="Previous packages"><span class="flip">{ARROW}</span></button>
          <button type="button" data-dir="1" aria-label="Next packages">{ARROW}</button>
        </div>
      </div>
      <div class="cards swipe-row">
{chr(10).join(cards)}
      </div>
      <p class="fine">Extra guests are $5 each. Travel, custom menus, specialty ingredients and longer service can change the final price.</p>
      <div class="pkg-ask">
        <p>Questions about a package, or want something custom?</p>
        <a class="btn" href="#book">Send us a message</a>
      </div>
    </div>
  </section>
"""


def included():
    items = "".join(f"<li>{x}</li>" for x in INCLUDED)
    return f"""  <section class="included-sec">
    <div class="wrap">
      <div class="sec-head">
        <h2>Everything included</h2>
        <p>No hidden beverage costs. We bring everything needed for the experience, so you can focus on enjoying your event.</p>
      </div>
      <ul class="inc-grid">{items}</ul>
    </div>
  </section>
"""


def names_strip():
    names = "".join(f"<li>{n.replace('&', '&amp;')}</li>" for n, _ in DRINKS)
    return f"""    <div class="names" aria-label="Our signature mocktails">
      <div class="wrap">
        <div class="names-box">
          <div class="names-track">
            <ul>{names}</ul>
            <ul aria-hidden="true">{names}</ul>
          </div>
        </div>
      </div>
    </div>
"""


def menu():
    cards = "\n".join(f"""        <article class="sig">
          <div class="sig-img"><img src="images/{f}" alt="{a}" width="{w}" height="{h}" loading="lazy"></div>
          <div class="sig-body">
            <p class="sig-tag">Signature</p>
            <h3>{n}</h3>
            <p>{d}</p>
          </div>
        </article>""" for f, w, h, n, d, a in SIGNATURES)
    items = "\n".join(f'        <li><span class="name">{n.replace("&", "&amp;")}</span><span class="desc">{d}</span></li>' for n, d in DRINKS)
    return f"""  <section class="menu" id="menu">
    <div class="wrap">
      <div class="sec-head">
        <h2>Our signature mocktails</h2>
        <p>Pick two to four for your event, or we’ll create one around your colors or theme.</p>
      </div>
      <div class="sig-cards">
{cards}
      </div>
    </div>
{names_strip()}    <div class="wrap">
      <div class="menu-card">
        <p class="menu-title">The full menu</p>
        <ul class="drinks">
{items}
        </ul>
        <p class="menu-note">All alcohol-free. Custom drinks on request.</p>
      </div>
      <p class="link-row"><a href="gallery.html">See the full gallery</a><a href="{IG_URL}">Follow @{IG_HANDLE}</a></p>
    </div>
  </section>
"""


STEPS = f"""  <section class="how" id="how">
    <div class="wrap">
      <div class="sec-head">
        <h2>How it works</h2>
        <p>Three easy steps from first message to last pour.</p>
      </div>
      <ol class="how-steps">
        <li>
          <span class="num">01</span>
          <h3>Reach Out</h3>
          <p>DM us on <a href="{IG_URL}">Instagram</a> or fill out the <a href="#book">form below</a>. Tell us a little about your event, and let’s start dreaming up something special. A member of our team will reach out to you shortly.</p>
        </li>
        <li>
          <span class="num">02</span>
          <h3>Make it yours</h3>
          <p>We’ll connect over FaceTime or meet in person to find the perfect package for your event. From custom mocktails to the finishing touches, we’ll tailor every detail to your vision. We’ll provide a free, no-obligation quote and work with you to create the perfect setup for your event!</p>
        </li>
        <li>
          <span class="num">03</span>
          <h3>Sit back &amp; sip</h3>
          <p>Once the details are set, you can check one more thing off your list!</p>
          <p>We’ll take care of everything from start to finish, bringing the drinks, fresh ingredients, and real glassware, setting up the bar, serving your guests, and handling all the cleanup. You focus on celebrating and making memories&mdash;we’ll handle the rest!</p>
        </li>
      </ol>
    </div>
  </section>
"""

# Selling points from Chase and Jake's 10/22 meeting
WHY = """  <section class="why" id="why">
    <div class="wrap">
      <div class="why-top">
        <div class="sec-head">
          <h2>A real bar, <em>without the alcohol</em></h2>
          <p>Our founder spent years behind the bar making craft cocktails and got tired of mocktails being an afterthought. So we make every one with the same care.</p>
        </div>
        <div class="why-photo reveal"><img src="images/candid-shaking.jpg" alt="Our bartenders shaking and pouring drinks behind the bar at a wedding, with real glassware ready" width="1122" height="1402" loading="lazy"></div>
      </div>
      <ul class="why-list">
        <li><h3>Real glassware</h3><p>Every drink is served in a real glass, not a plastic cup.</p></li>
        <li><h3>One all-in price</h3><p>Drinks, ingredients, ice, glassware, bartenders, setup and cleanup are in your package. No surprise beverage costs.</p></li>
        <li><h3>Real bartenders</h3><p>Trained bartenders and an elegant mobile bar give your event the feel of a cocktail lounge, not a soda shop.</p></li>
        <li><h3>Shaken to order</h3><p>Fresh ice in every pour, and each drink is shaken right in front of your guests.</p></li>
      </ul>
    </div>
  </section>

  <section class="venues" aria-label="Venues we’re listed with">
    <div class="wrap">
      <p class="venues-label">A preferred vendor at</p>
      <p class="venues-names"><span>Utah State Capitol Building</span><span>Hobble Creek Manor</span></p>
      <p class="venues-label venues-label-2">We’ve also served events at</p>
      <p class="venues-names venues-more"><span>Adobe</span><span>Sleepy Ridge</span><span>The Ballroom at the Commercial Club</span></p>
    </div>
  </section>
"""


def bio_teaser():
    return f"""  <section class="team-card" id="team">
    <img class="backdrop" src="images/capitol-bar.jpg" alt="" width="1200" height="1600" loading="lazy">
    <div class="wrap">
      <div class="card-box">
        <div class="copy">
          <h2>Meet <em>our team</em></h2>
          <p class="role">The people behind the bar</p>
          <p>Our team is led by {FOUNDER}, our founder and lead bartender, who spent years making craft cocktails before starting the company. Every bartender we send is trained to make each drink the same careful way.</p>
          <a class="text-link" href="team.html#story">Learn more about our story</a>
        </div>
        <div class="portrait"><img src="images/jacob.jpg" alt="{FOUNDER}, founder of {BIZ}, holding a mocktail" width="640" height="800" loading="lazy"></div>
      </div>
    </div>
  </section>
"""


# ---------------- Home ----------------
home = head(f"{BIZ} | Mocktail Bar for Utah Weddings and Events", f"{BIZ} is a mobile mocktail bar based in Utah County. Bartenders, a styled bar and ten signature mocktails for weddings and corporate events across Utah. Packages from $650.", schema=True, over_hero=True) + header("index.html") + f"""
<main id="top">
  <section class="hero">
    <video class="bg" autoplay muted loop playsinline aria-hidden="true"></video>
    <script>(function (v) {{ var tall = matchMedia('(orientation: portrait)').matches; v.poster = tall ? 'images/hero-slc-poster-m.jpg' : 'images/hero-slc-poster.jpg'; v.src = tall ? 'hero-slc-m.mp4' : 'hero-slc.mp4'; }})(document.currentScript.previousElementSibling);</script>
    <div class="wrap">
      <h1>Mocktail bars for Utah <em>weddings</em> and events</h1>
      <p>Our team brings fun mocktails to your event, with no stress or hassle for you.</p>
      <a class="btn" href="#book">Reserve your date</a>
    </div>
  </section>

  <section class="facts" aria-label="Quick facts">
    <ul class="wrap">
      <li>30 to 400 guests</li>
      <li>Bar, bartenders and cleanup included</li>
      <li>Based in Utah County, serving all of Utah</li>
    </ul>
  </section>

  <section class="statement">
    <div class="wrap narrow center">
      <h2>Nobody left out of <em>the toast</em></h2>
      <p>We bring the bar, the bartenders, the glassware and a menu of signature mocktails. We set up before your guests arrive, serve all night and clean up when it’s over.</p>
      <p>Every drink is alcohol-free, so kids, grandparents, designated drivers and coworkers can all raise the same glass.</p>
      <p class="link-row"><a href="weddings.html">Weddings</a><a href="corporate.html">Corporate events</a><a href="packages.html">Packages</a></p>
    </div>
  </section>

{menu()}

{WHY}
  <section class="clips band" id="weddings">
    <div class="wrap">
      <div class="copy">
        <h2>A drink named for <em>the two of you</em></h2>
        <p>We’ll create a signature drink just for your wedding. Name it after the two of you, your first date, or an inside joke you’d like everyone to be a part of.</p>
        <p>We’ll also match the menu to your colors and keep the line moving through cocktail hour. This clip is from a recent reception. Tap it to see more on Instagram.</p>
        <a class="btn" href="weddings.html">More about weddings</a>
      </div>
      <a class="clip-link" href="{IG_URL}" aria-label="Watch more of our events on Instagram @{IG_HANDLE}">
        <video src="wedding-clip.mp4" poster="images/wedding-poster.jpg" autoplay muted loop playsinline preload="metadata" aria-hidden="true"></video>
        <span class="clip-cta">{IG_ICON}Watch on Instagram</span>
      </a>
    </div>
  </section>

  <section class="pillars" aria-label="Events we serve">
    <div class="wrap">
      <article class="pillar">
        <div class="pillar-img reveal"><img src="images/popup-bar.jpg" alt="Our bartender serving at a pop-up bar outside a storefront" width="1200" height="1600" loading="lazy"></div>
        <div class="pillar-copy">
          <h3>Corporate events</h3>
          <p>Holiday parties, client nights, conferences and brand pop-ups. With an alcohol-free bar, the whole team can join in and you don’t have an open bar to manage. Winter is our busiest season, so book early.</p>
          <a class="btn btn-light" href="corporate.html" style="justify-self:start">More about corporate events</a>
        </div>
      </article>
      <article class="pillar">
        <div class="pillar-img reveal"><img src="images/couple-toast.jpg" alt="The bride and groom holding up their mocktails at their reception" width="1143" height="1600" loading="lazy" style="object-position: 50% 30%"></div>
        <div class="pillar-copy">
          <h3>Weddings and celebrations</h3>
          <p>Receptions, bridal showers, birthdays, graduations, reunions, school events and church gatherings, anywhere in Utah.</p>
          <a class="btn btn-light" href="weddings.html" style="justify-self:start">More about weddings</a>
        </div>
      </article>
    </div>
  </section>

{STEPS}
{included()}
  <section class="pkg-teaser" id="packages">
    <div class="wrap narrow center">
      <h2>Packages</h2>
      <p>Four packages for 30 to 400 guests, starting at $650. Every one includes the bar, bartenders, real glassware and cleanup.</p>
      <a class="btn" href="packages.html">See packages and pricing</a>
    </div>
  </section>

{contact()}
{bio_teaser()}</main>

{FOOT}"""

# ---------------- Weddings ----------------
weddings = head(f"Wedding Mocktail Bar in Utah | {BIZ}", "Mocktail bar for Utah weddings and receptions. A signature drink named for the couple, a styled bar and bartenders, from $650. Based in Utah County.") + header("weddings.html") + f"""
<main id="top">
  <section class="statement page-top">
    <div class="wrap narrow center">
      <h1 class="page-title">A mocktail bar for your <em>wedding</em></h1>
      <p>A drink named for the two of you, and bartenders from cocktail hour to send-off.</p>
      <p><a class="btn" href="#book">Reserve your date</a></p>
    </div>
  </section>

  <section class="pillars toast-pillar">
    <div class="wrap">
      <article class="pillar">
        <div class="pillar-img reveal"><img src="images/couple-toast.jpg" alt="The bride and groom holding up their mocktails at their reception" width="1143" height="1600" loading="lazy" style="object-position: 50% 30%"></div>
        <div class="pillar-copy">
          <h2>Something good to toast with</h2>
          <p>Your guests will have a drink in hand all night, whether or not they drink alcohol. We’ll match the menu to your colors, set the bar up before guests arrive and keep the line moving through cocktail hour.</p>
        </div>
      </article>
    </div>
  </section>

  <section class="clips band" id="clips">
    <div class="wrap">
      <div class="copy">
        <h2>From a recent wedding</h2>
        <p>A few seconds filmed behind our bar at a reception at Hobble Creek Manor. Tap the video to see more on Instagram.</p>
        <a class="btn" href="#book">Reserve your date</a>
      </div>
      <a class="clip-link" href="{IG_URL}" aria-label="Watch more of our events on Instagram @{IG_HANDLE}">
        <video src="wedding-clip.mp4" poster="images/wedding-poster.jpg" autoplay muted loop playsinline preload="metadata" aria-hidden="true"></video>
        <span class="clip-cta">{IG_ICON}Watch on Instagram</span>
      </a>
    </div>
  </section>

  <section class="details">
    <div class="wrap">
      <div class="sec-head"><h2>What couples usually ask for</h2></div>
      <dl>
        <div><dt>A drink named for you</dt><dd>We create a signature mocktail around your story or colors, and it goes on the menu sign with your names.</dd></div>
        <div><dt>A bar that fits the room</dt><dd>Our bar works in a ballroom, a barn or a backyard, with real glassware and a styled setup.</dd></div>
        <div><dt>Enough bartenders for cocktail hour</dt><dd>The Signature Celebration package has two bartenders for up to 125 guests.</dd></div>
        <div><dt>A dry wedding that still feels like a party</dt><dd>A good fit for families and venues that prefer no alcohol.</dd></div>
      </dl>
      <a class="btn btn-light" href="packages.html" style="justify-self:start">See packages and prices</a>
    </div>
  </section>

{contact("Wedding or reception")}</main>

{FOOT}"""

# ---------------- Corporate ----------------
corporate = head(f"Corporate Event Mocktail Bar in Utah | {BIZ}", "Mocktail bar for Utah holiday parties, company events, conferences and brand pop-ups. Bartenders, a styled bar and drinks named for your company.") + header("corporate.html") + f"""
<main id="top">
  <section class="statement page-top">
    <div class="wrap narrow center">
      <h1 class="page-title">Mocktail bars for <em>company events</em></h1>
      <p>Holiday parties, client nights, conferences and pop-ups. Winter is our busiest season, so book early.</p>
      <p><a class="btn" href="#book">Reserve your date</a></p>
    </div>
  </section>

  <section class="statement">
    <div class="wrap narrow center">
      <h2>A bar the whole team can enjoy</h2>
      <p>With an alcohol-free bar, everyone can join the toast and you don’t have to manage an open bar. We’ll name drinks after your company or event and match your brand colors.</p>
    </div>
  </section>

  <section class="pillars" aria-label="Corporate events">
    <div class="wrap">
      <article class="pillar">
        <div class="pillar-img reveal"><img src="images/berry-highball.jpg" alt="A dark berry mocktail with a lime wheel" width="1023" height="1537" loading="lazy"></div>
        <div class="pillar-copy">
          <h3>Holiday parties</h3>
          <p>We build our winter menus to taste like the holidays, with cranberry, citrus, honey and warm spice.</p>
        </div>
      </article>
      <article class="pillar">
        <div class="pillar-img reveal"><img src="images/popup-bar.jpg" alt="Bartender serving at a pop-up bar outside a storefront" width="1200" height="1600" loading="lazy"></div>
        <div class="pillar-copy">
          <h3>Brand pop-ups and store events</h3>
          <p>A drink in hand keeps people around longer. We set up outside storefronts for launches and open houses.</p>
        </div>
      </article>
      <article class="pillar">
        <div class="pillar-img reveal"><img src="images/capitol-guests.jpg" alt="Guests gathered around the bar at an evening event" width="1200" height="1600" loading="lazy"></div>
        <div class="pillar-copy">
          <h3>Conferences and galas</h3>
          <p>The Grand Event package serves up to 400 guests with three or more bartenders and fast-pour drinks. Need an invoice or other paperwork for your company? Just ask.</p>
        </div>
      </article>
    </div>
  </section>

{contact("Corporate or conference")}</main>

{FOOT}"""

# ---------------- Team ----------------
# Other bartenders: (name, role, photo file in images/). Empty = only Jake shows (Jake 2026-11-04: team is changing).
TEAM_MEMBERS = []
def team_more():
    if not TEAM_MEMBERS:
        return ""
    people = "\n".join(f'        <div class="member"><img src="images/{f}" alt="{n}, {r.lower()}" loading="lazy"><h3>{n}</h3><p>{r}</p></div>' for n, r, f in TEAM_MEMBERS)
    return f"""  <section class="team-more">
    <div class="wrap">
      <div class="sec-head"><h2>Bartenders</h2></div>
      <div class="team-list">
{people}
      </div>
    </div>
  </section>

"""
team = head(f"The Team | {BIZ}", f"The bartenders behind {BIZ}, a Utah County mocktail bar for weddings and corporate events, led by founder {FOUNDER}.") + header("team.html") + f"""
<main id="top">
  <section class="statement page-top">
    <div class="wrap narrow center">
      <h1 class="page-title">The team</h1>
      <p>The people behind the bar at every {BIZ} event.</p>
    </div>
  </section>

  <section class="bio" id="story">
    <div class="wrap">
      <div class="portrait"><img src="images/jacob.jpg" alt="{FOUNDER}, founder of {BIZ}, holding a mocktail" width="640" height="800"></div>
      <div class="copy">
        <p class="role">Founder and lead bartender</p>
        <h2>A drink for <em>everyone</em> at the party.</h2>
        <p>I started {BIZ} after years behind the bar, watching the same thing happen at every event: hosts had to choose between a casual soda setup or a traditional bar where mocktails were an afterthought.</p>
        <p>Most mocktails are just a cocktail recipe with the alcohol left out, and you can taste what’s missing. I felt like these drinks deserved more attention, so I set out to change that. Every drink on our menu is built to stand up to a real cocktail, with layers of fresh fruit, herbs and citrus chosen for the best possible flavor, without the alcohol.</p>
        <p>There was almost nothing for people who wanted a premium, alcohol-free experience, so I built it. As a BYU marketing student with a background in Utah Valley hospitality, I wanted to create beverage experiences that feel sophisticated and inclusive, where no one has to opt out.</p>
        <p>From a thirty-person dinner to a four-hundred-guest reception, every event gets the same thing: handcrafted drinks, premium ingredients, beautiful presentation, and genuine hospitality.</p>
        <p class="sign">{FOUNDER}, founder of {BIZ}</p>
      </div>
    </div>
  </section>

{team_more()}{contact()}</main>

{FOOT}"""


# ---------------- Gallery ----------------
# file, alt, width, height, caption (None = no caption)
GALLERY_PAGE = [
    ("capitol-guests.jpg", "Wedding guests gathered around the mocktail bar in a marble hall", 1200, 1600, None),
    ("stir-loop.mp4", "A purple berry mocktail being stirred at a wedding at Hobble Creek Manor", 540, 960, None),
    ("couple-toast.jpg", "The bride and groom holding up their mocktails at the reception", 1146, 1600, None),
    ("cherry-sour.jpg", "Cherry Parson with a cherry garnish", 1066, 1600, "Cherry Parson"),
    ("berry-highball.jpg", "Lavender Lime Cooler with dried lavender and a lime wheel", 1023, 1537, "Lavender Lime Cooler"),
    ("glasses-toast.jpg", "Guests clinking mocktail glasses with pink straws", 1600, 1143, None),
    ("mint-spritz.jpg", "Mint Mojito with fresh mint and lime", 1066, 1600, "Mint Mojito"),
    ("capitol-bar.jpg", "Pink mocktails lined up on the bar in a marble hall", 1200, 1600, None),
    ("dragonfruit-toast.jpg", "A guest holding a pink mocktail with a dragonfruit slice", 1170, 1552, None),
    ("bar-citrus.jpg", "A yellow citrus mocktail with an orange slice on the bar", 1200, 1600, None),
    ("berry-loop.mp4", "A blackberry garnish being set on a dark berry mocktail", 540, 960, None),
    ("jacob.jpg", "Jacob, our founder, holding a mocktail", 640, 800, None),
    ("sunset-pour.jpg", "A bartender straining an orange-red mocktail", 1066, 1600, None),
]
# A .mp4 entry is a short silent loop that plays like a live photo
def tile(f, a, w, h, c):
    if f.endswith(".mp4"):
        media = f'<video src="{f}" poster="images/{f[:-4]}-poster.jpg" width="{w}" height="{h}" autoplay muted loop playsinline aria-label="{a}"></video>'
    else:
        media = f'<img src="images/{f}" alt="{a}" width="{w}" height="{h}" loading="lazy">'
    return f'      <figure>{media}' + (f'<figcaption>{c}</figcaption>' if c else '') + '</figure>'
tiles = "\n".join(tile(*g) for g in GALLERY_PAGE)
gallery = head(f"Gallery | {BIZ}", f"Photos of {BIZ} mocktail bars at Utah weddings, receptions and company events.") + header("gallery.html") + f"""
<main id="top">
  <section class="statement">
    <div class="wrap narrow center">
      <div class="frame">
        <span class="corner tl"></span><span class="corner tr"></span><span class="corner bl"></span><span class="corner br"></span>
        <h1 class="page-title">Gallery</h1>
        <p>Drinks and bars from our recent weddings and events. For more, follow along on Instagram.</p>
        <p class="link-row"><a class="ig-handle" href="{IG_URL}">{IG_ICON}@{IG_HANDLE}</a></p>
      </div>
    </div>
  </section>

  <section class="photo-wall">
    <div class="wrap">
{tiles}
    </div>
  </section>

{contact()}</main>

{FOOT}"""

# ---------------- Reviews ----------------
# Real reviews only, copied word for word: quote, name, event, where it was posted (Google or Instagram)
# Real reviews only. Instagram story shoutouts, worded as posted (typos fixed).
REVIEWS = [
    ("There's usually only soda at events, and as someone who doesn't drink it, I was SO excited to see mocktails at this Utah event. I literally downed three in the hour and a half I was there. Thanks for keeping me hydrated all night!", "Maddie", "", "Via Instagram"),
    ("We seriously live laugh love Utah Mocktail Co. Book them for every event you have!", "Avery", "", "Via Instagram"),
    ("Best in the business!! Book with them for your next event.", "Liv", "", "Via Instagram"),
]
def review_card(q, n, e, src):
    return f'      <figure class="review"><span class="stars" role="img" aria-label="5 stars">★★★★★</span><blockquote>“{q}”</blockquote><figcaption><strong>{n}</strong>{e}<span class="src">{src}</span></figcaption></figure>'
if REVIEWS:
    review_cards = "\n".join(review_card(*r) for r in REVIEWS)
else:
    review_cards = "\n".join('      <figure class="review"><blockquote><span class="ph">[Review quote from Instagram or Google]</span></blockquote><figcaption><strong><span class="ph">[Name]</span></strong><span class="ph">[Event and venue]</span></figcaption></figure>' for _ in range(3))
reviews_page = head(f"Reviews | {BIZ}", f"What couples, families and companies say about {BIZ}, a mobile mocktail bar in Utah.") + header("reviews.html") + f"""
<main id="top">
  <section class="statement page-top">
    <div class="wrap narrow center">
      <h1 class="page-title">Reviews</h1>
      <p>What couples, families and event planners have said after having our team behind the bar.</p>
    </div>
  </section>

  <section class="reviews">
    <div class="wrap">
{review_cards}
    </div>
    <p class="link-row center"><a href="https://www.instagram.com/utahmocktailco/">See more on Instagram @utahmocktailco</a></p>
  </section>

{contact()}</main>

{FOOT}"""

# ---------------- Packages ----------------
packages_page = head(f"Packages and Pricing | {BIZ}", f"Mocktail bar packages from {BIZ}: four options for 30 to 400 guests, from $650, with bartenders, real glassware, setup and cleanup included.") + header("packages.html") + f"""
<main id="top">
  <section class="statement page-top">
    <div class="wrap narrow center">
      <h1 class="page-title">Packages &amp; pricing</h1>
      <p>Four packages for 30 to 400 guests. Not sure which fits? We’ll help you choose on a quick FaceTime call.</p>
    </div>
  </section>

{package_cards()}
{included()}
{contact()}</main>

{FOOT}"""

for name, html in [("index.html", home), ("packages.html", packages_page), ("weddings.html", weddings), ("corporate.html", corporate), ("team.html", team), ("gallery.html", gallery), ("reviews.html", reviews_page)]:
    url = "https://utahmocktailco.com/" + ("" if name == "index.html" else name[:-5])
    html = html.replace('<link rel="icon"', f'<link rel="canonical" href="{url}">\n<link rel="icon"', 1)
    # Link to clean URLs (/weddings, not weddings.html) so Google doesn't see two addresses per page.
    html = re.sub(r'href="(index|weddings|corporate|packages|gallery|reviews|team)\.html(#[^"]*)?"',
                  lambda m: f'href="/{"" if m.group(1) == "index" else m.group(1)}{m.group(2) or ""}"', html)
    open(os.path.join(OUT, name), "w").write(html)
    print(name, len(html))
