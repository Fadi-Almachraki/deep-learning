# Barcelona to Madrid — GBW Spain 2026

An interactive walkthrough of the schedule for *Competitive Advantage in the
Leisure Industries: Spain* (Wharton MBA for Executives, Global Business Week,
13–18 September 2026).

`index.html` is a single self-contained page — open it in any browser, no build
step and no server required.

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

Light and dark themes, responsive to phone width, and a print stylesheet that
expands every place note.

## Source

Built from `GBW-Spain2026Syllabus.pdf` (included here for reference). The
schedule in that PDF is preliminary and updated daily — check Canvas for the
current version. Historical notes and fun facts are added trip colour, not part
of the course materials.
