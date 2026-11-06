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

- Prediction: Pending.
- Check interpretation: Pending.
- Browser observation: Pending.
- Keep decision: Pending.
- Review: Pending.
- Help/gaps: Pending.
- Evidence links / next step: Keep APP-001 before agreeing this lesson.

## APP-003

- Prediction: Pending.
- Check interpretation: Pending.
- Browser observation: Pending.
- Keep decision: Pending.
- Review: Pending.
- Help/gaps: Pending.
- Evidence links / next step: Keep APP-002 before agreeing this lesson.
