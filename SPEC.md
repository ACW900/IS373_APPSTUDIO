# App Studio decisions

The durable agreement between learner and AI. Update only agreed decisions and
actual evidence; pending is a valid state. Keep explanations/help in
[LEARNING.md](LEARNING.md), not a second copy here.

## Current stage

- **Current feature:** APP-002.
- **Status:** APP-001 kept (PR #2 merged). APP-002 scope being agreed.
- **Next step:** Learner prediction, then the APP-002 plan.
- **Implementation marker:** `studio.json` starts at `implemented_through: 0`.

This repository owns application code. Server/proxy changes and production
deployment are outside these three local-development lessons. Prepared helpers
are reusable foundations, not evidence that unfinished routes are implemented.

## APP-001 · Branded homepage

**Scope:** make the neutral FastAPI homepage express one chosen identity with
a simple original SVG mark, coherent copy, navigation and shared style tokens.
Keep account actions honest about their unfinished state.

| Decision | Agreement |
|---|---|
| Visitor and concrete use situation | "a gamer looking for news about his favorite games" |
| Reused IS117 brand, or name / promise / primary archetype | New identity (not reusing IS117). Working name: **Save Point** (picked from AI suggestions). Promise (learner's words): "New patch get caught up from the last time you played." Primary archetype: **Everyman** (friendly fellow player), with a Sage influence: "the grity data" in the content. |
| One visible choice and visitor benefit | Friendly fellow-player (Everyman) voice. Learner's reason: "It makes them want to pick the game back up without the pressure an expert may exude." |
| Look / style tokens | Simple, uncluttered. Navy background, bright red highlight, white text. |
| Own issue / branch / PR | [ACW900/IS373_APPSTUDIO#1](https://github.com/ACW900/IS373_APPSTUDIO/issues/1) / `app-001-homepage` / [PR #2](https://github.com/ACW900/IS373_APPSTUDIO/pull/2) |

**Keep when:** the agreed identity is visible and usable at desktop/narrow widths;
full foundation + APP-001 checks pass; AI review and the learner's actual check
interpretation/browser observation/keep reason are recorded; reviewed evidence
and verified GitHub state are linked below.

## APP-002 · Signup, login and logout

**Scope:** add browser forms and REST behavior for member signup, login, a private
dashboard and logout backed by SQLite. Reuse the prepared password/JWT/CSRF/session
helpers; keep data local. New accounts cannot choose their role.

| Decision | Agreement |
|---|---|
| Expected public/private behavior and account flow | After login (learner): "each game the user has marked/saved." Agreed option B: a logged-in member can save a short list of game names to their account in local SQLite. No patch/update info (no real news source in this lesson). Before login (learner): "something along the lines of please make an account in order to continue and point them towards a login." Learner also wants public game pages that need no login; not in APP-002 (no game data source), kept as a later idea. |
| Valid and rejected cases to demonstrate | Password minimum: learner asked for 7 ("most passwords that are made quickly are around 8 characters"). AI explained the template's 15 follows NIST SP 800-63B for password-only accounts and advised against 7; learner chose **8** (option B), knowingly weaker than 15. Signup page encourages longer phrases. Learner: "dont tell the user the cap unless they go over": pages no longer show the 20-game, 128-character or 32-character limits; the server still enforces them and explains a limit only when it is exceeded. Other cases pending. |
| Own issue / branch / PR | [ACW900/IS373_APPSTUDIO#3](https://github.com/ACW900/IS373_APPSTUDIO/issues/3) / `app-002-accounts` / [PR #4](https://github.com/ACW900/IS373_APPSTUDIO/pull/4) |

**Keep when:** the agreed forms/API work; duplicate/invalid signup and wrong
credentials are rejected; passwords are hashed; authentication uses validated,
expiring JWTs with protected cookies and CSRF; private requests require a live
session and logout revokes it. Full cumulative checks, AI review, actual learner
contributions and GitHub state are recorded. This is not a production-security certification.

## APP-003 · Server-enforced roles

**Scope:** enforce a small member/admin boundary in the API and browser. Assign
roles only through the trusted local terminal command; use current server-side
permissions, including for an existing session after a role change.

| Visitor | Homepage | Member area | Admin area/API |
|---|---|---|---|
| Anonymous | Allowed | Login required | Login required |
| Member | Allowed | Allowed | Forbidden |
| Admin | Allowed | Allowed | Allowed |

| Decision | Agreement |
|---|---|
| Intended admin-only result | Pending |
| Actual allowed/denied request evidence | Pending |
| Own issue / branch / PR | Pending |

**Keep when:** a direct request cannot bypass the role boundary, role changes
take effect as specified, new signup remains member-only, and full cumulative
checks plus AI review pass. Link the learner's actual interpretation/observation,
reviewed record and verified GitHub result. Hidden navigation alone is insufficient.

## Evidence

Link actual files/checks and the student's own issues/PRs. No fabricated URLs,
customer research or claims that a timestamp proves learning.

| Feature | Files / own issue / PR | Actual checks and learner observations | Kept / GitHub state |
|---|---|---|---|
| APP-001 | `app/brand.json`, `app/templates/home.html`, `app/templates/base.html`, `app/static/logo.svg`, `app/static/site.css`; [issue #1](https://github.com/ACW900/IS373_APPSTUDIO/issues/1), [PR #2](https://github.com/ACW900/IS373_APPSTUDIO/pull/2) | Local Windows full check (2026-11-06): Black, Pylint, 2 APP-001 contracts and 2 Chromium journeys passed; 95 foundation tests passed, 1 failed only because Windows denied symlink creation (privilege, not app code); CI pending. AI viewed desktop and 375px layouts (no horizontal scroll). Learner check interpretation/observation pending | Pending |
| APP-002 | `app/features/accounts.py`, `app/features/games.py`, `app/features/pages.py`, `app/database.py` (saved_games table), `app/schemas.py` (GameInput), templates `signup/login/dashboard/message.html`, `tests/test_saved_games.py`; [issue #3](https://github.com/ACW900/IS373_APPSTUDIO/issues/3), [PR #4](https://github.com/ACW900/IS373_APPSTUDIO/pull/4) | Local Windows full check at `implemented_through: 2` (2026-11-06): Black, Pylint, 14 contracts through APP-002, 5 new saved-games tests and 2 Chromium journeys passed; only the Windows symlink test failed (Developer Mode off). AI used a throwaway local account: signup, login, add/remove a game, logout; desktop and 375px layouts checked. Learner interpretation/observation pending | Pending |
| APP-003 | Pending | Unfinished; explicit contracts not yet passed | Pending |

The instructor's reference branches show possible implementations. They do not
establish this repository's completion or the learner's own reasoning.
