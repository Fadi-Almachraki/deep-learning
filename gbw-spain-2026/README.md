# Barcelona to Madrid — GBW Spain 2026

An interactive walkthrough of the schedule for *Competitive Advantage in the
Leisure Industries: Spain* (Wharton MBA for Executives, Global Business Week,
13–18 September 2026).

## Files

| File | What it is |
| --- | --- |
| `index.html` | The source page. Loads its typefaces from Google Fonts. |
| `Barcelona-to-Madrid.html` | **Download this one.** Identical page with the fonts subsetted and embedded — one 396 KB file, no network needed. |
| `Barcelona-to-Madrid.pdf` | The whole week as 21 printable A4 pages. |
| `build-offline.py` | Regenerates both of the above from `index.html`. |
| `GBW-Spain2026Syllabus.pdf` | The source syllabus. |

Every HTML version is a single file — open it in any browser, no build step and
no server required.

## What it does

- **Day rail** — the week drawn as a journey line, with each segment coloured by
  city (Barcelona teal → Penedès gold → Madrid carmine) and the Iryo high-speed
  leg drawn as a dashed crossing. Arrow keys move between days; the URL hash
  (`#mon`, `#places`) deep-links to a day.
- **Live status** — reads the current time in `Europe/Madrid`, auto-selects the
  day you are actually on during the trip, dims events that have passed, and
  drops a NOW marker into the timeline.
- **Timeline** — rail-timetable layout, filterable by session / visit / meal /
  transit / free time / logistics. Each session carries a short note on why it
  matters to the course argument.
- **Places & Stories** — the twelve venues as a second navigation axis, each
  with a short history, a fun fact, and a Google Maps link.
- **Free-time picks** for Wednesday evening and Friday morning, with map links.

- **Print / PDF** — prints the entire week rather than the day on screen. The
  itinerary pages stay compact (venues reduced to a location line) because the
  Places & Stories section at the back carries the full notes.

Light and dark themes, responsive to phone width.

## Rebuilding the downloads

```sh
pip install fonttools brotli playwright && playwright install chromium
python3 build-offline.py
```

The script fetches the Google Fonts faces, subsets them to the ~160 characters
the page actually uses, pins Newsreader's optical-size axis (the page never
varies it), and embeds them as base64 woff2 — 514 KB of font data down to 244 KB.
It asserts glyph coverage and non-empty outlines before writing, since a subset
that silently loses its glyphs still *loads* in the browser and then renders as
a fallback.

## Source

Built from `GBW-Spain2026Syllabus.pdf` (included here for reference). The
schedule in that PDF is preliminary and updated daily — check Canvas for the
current version. Historical notes and fun facts are added trip colour, not part
of the course materials.
