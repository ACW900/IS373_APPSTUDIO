# App Studio decisions

The durable agreement between learner and AI. Update only agreed decisions and
actual evidence; pending is a valid state. Keep explanations/help in
[LEARNING.md](LEARNING.md), not a second copy here.

## Current stage

- **Current feature:** APP-003.
- **Status:** APP-001 and APP-002 kept (PRs #2 and #4 merged). APP-003 implemented and reviewed; PR pending.
- **Next step:** Open the APP-003 PR, review CI, merge.
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
| Intended admin-only result | Learner idea: admins manage games that are no longer updated ("maybe we put a special box for admission to toggle that puts an indicator on the game for players"); deleting rarely needed. Agreed scope: `/admin` and `/api/admin` show a shared "No longer getting patches" list; an admin can add a game name and switch the marker on/off (no delete). Members see a "No longer patched" badge on matching saved games but cannot change it. Admin role only via the trusted terminal command. Learner: "if it shifts during conversation we can adjust." |
| Actual allowed/denied request evidence | Tests: anonymous `/api/admin` 401 and `/admin` → login; member 403 for API, page, add and toggle (even with CSRF); admin 200/201; role downgrade blocks the same session on the next request; an altered role claim in the token is ignored. |
| Own issue / branch / PR | [ACW900/IS373_APPSTUDIO#5](https://github.com/ACW900/IS373_APPSTUDIO/issues/5) / `app-003-roles` / PR pending |

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
| APP-003 | `app/features/roles.py`, `app/features/games.py` (badge join), `app/database.py` (patch_status table), `app/schemas.py` (PatchToggle), templates `admin.html`, `admin_denied.html`, `dashboard.html`, `tests/test_patch_status.py`; [issue #5](https://github.com/ACW900/IS373_APPSTUDIO/issues/5) | Local Windows full check at `implemented_through: 3` (2026-11-06): Black, Pylint, 105 foundation tests, 18 contracts through APP-003 and 2 Chromium journeys passed. AI browser review with a throwaway account: member /admin → 403 page; after trusted `user role --role admin`, /admin worked, added a game, member dashboard showed the badge on a lowercase match; after `--role member` the same session got 403 again. Desktop and 375px checked. Learner interpretation/observation pending | Pending |

The instructor's reference branches show possible implementations. They do not
establish this repository's completion or the learner's own reasoning.
