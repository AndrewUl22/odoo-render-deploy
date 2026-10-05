# Portfolio — Odoo Website Portfolio Page

A public page at `/portfolio`, built into Odoo through the Website module and a QWeb template. It showcases my [`library`](https://github.com/AndrewUl22/library) project along with some basic info about me.

## Installation

1. Copy the `portfolio` folder into `addons/` (next to `library`):

```bash
cp -r portfolio /path/to/odoo/addons/
```

2. Install the module (requires the `website` module, which ships with Odoo by default — no separate installation needed):

```bash
./odoo-bin -d mydb --addons-path=addons,odoo/addons -i portfolio --dev=all
```

3. Open `http://localhost:8069/portfolio` — no login required, the page is public.

## What's on the page

- Hero section with name, tagline, and a link to GitHub
- Skills badges
- Project showcase: the [`library`](https://github.com/AndrewUl22/library) Odoo module
- Other projects: TravelTrucks RoadNest, LearnLingo, VocabBuilder (live demo + GitHub links each)
- Certification: GoIT Fullstack Developer course (872h)
- Contact section: email, phone, GitHub, LinkedIn

## TODO

- Add screenshots of the `library` interface (book form, loan list) to `static/description/` or an external image host, and embed them in the template via `<img t-att-src="...">`
- Optional: add a profile photo
- Optional: add live-stats from `library`

## Ideas for further improvement (optional, but a nice touch)

- Replace the static `skills` list with an `ir.model`-backed one (good practice for dynamic QWeb templates driven by database data)
- Add a simple contact form via `type='http', methods=['POST']`
- Add a live-stats section from `library` (number of books, number of loans) — a good excuse to practice ORM queries (`self.env['library.book'].search_count([])`)