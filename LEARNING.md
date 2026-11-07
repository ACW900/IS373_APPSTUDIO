# Conversation evidence

AI-drafted task summary, not a transcript or grade. It may be public. Use actual
short words or labeled paraphrases; disclose help and leave missing responses
pending. The learner reviews, corrects or removes new excerpts before commit/push.
Accuracy approval is not proof of understanding. Label simulated trials explicitly.

**Available conversation context:** Claude Code desktop chat, 2026-11-06, from clone check and setup onward.

## APP-001

- Prediction: Asked what a gamer would feel or do on first seeing navy with red
  highlights: "i dont know, i thought navy was good because it is easier to open in
  darker rooms. the red was so that the page didnt look bland but we could change the
  red to any other highlighting color."
- Check interpretation: Shown `test_chosen_brand_reaches_the_homepage` (GET /; expects
  200 with brand name, headline and promise, no "Your Project", an h1, logo served as
  SVG; passed). After asking for clarification and an AI example (a deleted promise
  line): "I think that it would mess up how the sizing of the page is and may shove
  information in the wrong places." (AI note: this check only looks for text and the
  logo, so layout and sizing problems are something it leaves open; the separate
  Chromium test checks the narrow width.)
- Browser observation: On their own local page: "i think the words Patch catch-up for
  returning players is a bit small and has a lot of space above it."
- Keep decision: Revise. "make it larger because it conveys what our site actually
  does." AI enlarged the top label and reduced the space above it.
- Review: On 2026-11-06 the learner was shown the new excerpts and AI-help summary and
  confirmed: "Yes, it's accurate," before the first commit. Approval covers record
  accuracy only.
- Help/gaps: Learner chose a new identity and named the visitor. Asked for name ideas;
  AI offered Patch Notes, Respawn Daily, The Loot Drop and Save Point. Learner said they
  like reading patch notes "but i would like my site to seem simpler"; turned down two
  simpler variants; then chose: "Save Point kind of speaks to me." Name came from an AI
  suggestion.
  Promise in learner's words: "New patch get caught up from the last time you played."
  AI explained an archetype as the brand's recurring character and offered Sage and
  Everyman. Learner blended them: "i like the everyman but i want the grity data that
  comes with the sage." Why the voice helps the visitor: "It makes them want to pick
  the game back up without the pressure an expert may exude."
  Learner chose navy, bright red highlights and white text. AI wrote the page copy
  (headline, summary, sections), the flag logo and the style changes from these
  decisions, and added only punctuation to the promise on the page.
- Evidence links / next step: Clone `ACW900/IS373_APPSTUDIO` (SSH) confirmed; `studio.py setup` ran via `py`
  (Python 3.13). Baseline check: Black, Pylint, 95 foundation tests and 2 Chromium
  journeys passed; 1 test failed because Windows denied symlink creation (local
  privilege, not app code). First look at the neutral page (onboarding, before any
  APP-001 work): "it seems verry modern and looks like a template you would see like
  in slide templates or something." Issue: [#1](https://github.com/ACW900/IS373_APPSTUDIO/issues/1);
  branch `app-001-homepage`. Next: accuracy review, then commit, PR and CI.

## APP-002

- Prediction: Asked what Save Point stores in its database for a signup password:
  "a secure hash."
- Check interpretation: Shown `test_logout_revokes_a_copied_token_and_get_does_not_log_out`
  (copy the login cookie, log out, replay it on `GET /api/me`; expects 200 before,
  401 after, 405 for GET logout; passed): "this would stop people from faking who they
  are from a stolen device." (AI note: it covers a copied cookie used after logout; a
  cookie stolen before logout still works until it expires, up to 15 minutes.)
- Browser observation: Own throwaway account on the local page: "after i hit log out it
  put me right back to the login screen." (Revisit of /dashboard after logout not
  separately reported.)
- Keep decision: Keep. "it works for now we can always add in the future."
- Review: On 2026-11-06 the learner was shown the new APP-002 excerpts and AI-help
  summary and confirmed: "Yes, accurate," before commit. Approval covers record
  accuracy only.
- Help/gaps: Learner described the after-login view ("each game the user has
  marked/saved with the latest changes/update info"). AI explained that real update info
  needs a news source and offered two sizes; learner chose B (save game names, no update
  info). Before login (learner): "please make an account in order to continue and point
  them towards a login"; learner's public game-page idea kept for later. Learner asked
  for pages that feel friendly (Everyman) with Sage detail. AI built the routes, pages,
  saved-games table and tests using the prepared security helpers.
  Learner asked to lower the password minimum to 7 ("most passwords that are made
  quickly are around 8 characters"); AI explained the template's 15 follows NIST
  guidance and advised against 7; learner chose 8. Learner asked: "dont tell the user
  the cap unless they go over"; AI hid the displayed limits (server still enforces them).
- Evidence links / next step: [Issue #3](https://github.com/ACW900/IS373_APPSTUDIO/issues/3);
  branch `app-002-accounts`. Next: accuracy review, then commit, PR and CI.

## APP-003

- Prediction: Asked what happens when a logged-in member types `/api/admin` directly:
  "They are denied and maybe if it is a frequent problem they are banned/flagged in our
  system."
- Check interpretation: Shown `test_trusted_role_change_applies_to_the_existing_session`
  (member promoted to admin by the trusted command → 200 on `/api/admin` and `/admin`;
  downgraded → 403 on the same session; passed): "this keeps out people who are trying
  to fake being a admin user." (AI note: this test specifically catches a stale role,
  e.g. a downgraded admin keeping access until logout; faking a role in the token is
  covered by the separate role-claim test.)
- Browser observation: After logging in as the AI-created local `test_admin` account,
  first said "it works"; asked for one detail: "the button was a toggle like i
  mentioned but i would like it if a game that was still getting patches was green."
- Keep decision: Revise: show a game that is still getting patches in green. AI
  changed the "Still getting patches" badge on the admin page to green.
- Review: On 2026-11-06 the learner was shown the new APP-003 excerpts and AI-help
  summary and confirmed: "Yes, accurate," before commit. Approval covers record
  accuracy only.
- Help/gaps: Learner proposed the admin idea (manage games no longer updated; a toggle
  that shows players an indicator; deletion rarely needed). AI narrowed it to an add/
  toggle "no longer patched" list plus a member badge; learner agreed ("if it shifts
  during conversation we can adjust"). Learner's ban/flag idea for repeat attempts kept
  for later. Learner working remotely; AI built the routes, pages, tests and ran the
  trusted role command on a throwaway local account.
  At the learner's request AI created a local `test_admin` account (password kept in
  ignored `runtime/`, not in chat) and promoted it with the trusted command.
- Evidence links / next step: [Issue #5](https://github.com/ACW900/IS373_APPSTUDIO/issues/5);
  branch `app-003-roles`. Next: accuracy review, then commit, PR and CI.
