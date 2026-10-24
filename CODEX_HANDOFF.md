# BridgeNext — Codex Project Handoff

Updated: 24 October 2026, Malaysia.
Purpose: continue this existing project in VS Code and deploy through Replit.
Primary working directory: `C:\Users\cminh\Downloads\BridgeNext` (section 23); full local app: http://localhost:5000.

LATEST APPROVED FLOW: see section 15 for prototype access, sections 16-17 for the simplified radar and visible five-group chart, section 20 for compact insights/static home cards, and section 21 for optional Gemini integration and live-verification limits. The frontend now uses an input-derived
`test` prototype session. This supersedes older demo/account-login UI rules,
including section 5-B, Mei/Aaron pickers and Review my answers. Real protected
backend account APIs are retained separately; test never authorizes them.

## 1. Instructions for the receiving Codex agent

Continue the supplied source project. Preserve its existing visual design,
assets, interactions and data. Do not rebuild the website from screenshots
or replace its framework.

This document is a curated project handoff, not a verbatim transcript.
The latest approved requirements below override conflicting older behavior
or wording in the source and README.

Discuss work with the user in Chinese. English is the default UI; the latest
approved inclusive-design requirement adds Bahasa Malaysia and Simplified Chinese.

Before editing:

1. Read this file and README.md.
2. Inspect the actual source files.
3. Identify which requested features already exist.
4. Preserve the current visual baseline.
5. Implement the pending corrections in section 5 first.

Do not claim authentication, a live model, data refresh, deployment or a test
is working unless verified. Report incomplete connections accurately.

If docs/CHAT_HISTORY.md exists, use it as supplementary historical context.
Do not implement abandoned ideas merely because they appear in old messages.

## 2. Project context

Product: BridgeNext.
Team: EyeScream, Chan Min Huey and Yap Li Shan, APU.
Competition: SDC Hackathon 2026, Domain 1, Future-Ready Workforce.

Broader intended audience:
Working adults adapting or transitioning as AI changes their work.

Preliminary prototype scope:
Malaysian financial operations and related administrative staff.

Core journey:
Confirmed skills profile -> explainable career comparison ->
affordable learning pathway within the user's weekly time budget.

The product assists human judgement.
It does not predict personal job loss, guarantee employment, determine hiring
or certify a user's professional competence.

Visual reference:
https://bridgenext-workforce-prototype.citrusplume512.chatgpt.site

Last source commit published by the previous assistant:
cfb35323cf94f94a4a026108c4778a052711e3e0

Latest distributed source:
BridgeNext-Replit.zip, containing the BridgeNext-Replit project folder.

The latest published version includes:

- Redesigned chick mascot and six occupational outfits.
- Explicit Accountant demo and Admin demo homepage buttons.
- Four-step guest questionnaire.
- Career recommendations and comparison.
- Future Skills Radar.
- Learning Pathway.
- Synthetic HR team overview.
- A Python backend and Replit configuration in the source.

Local implementation status (23 October 2026): section 5's independent
My Profile, explicit access/save rules and stable personal-avatar model are
implemented and locally verified. These changes have NOT been deployed to Replit.
See section 10 for checks and remaining deployment work.

## 3. Stack and important files

Frontend:

- React
- TypeScript
- Vite
- Recharts
- lucide-react
- PDF.js / pdfjs-dist
- Tesseract.js

Backend:

- Python 3.12
- FastAPI
- Pydantic
- Uvicorn
- SQLite
- Optional Gemini 2.5 Flash through Replit AI Integrations

Deployment target: Replit.
No RunPod/GPU service is currently used.

Use package-lock.json and requirements.txt as dependency authorities.

Important files:

- src/main.tsx:
  Screens, questionnaire, navigation, dialogs, demo profiles and API adapters.
- src/style.css:
  Visual design, layouts, responsive rules and mascot rendering.
- src/engine.ts:
  Deterministic browser matching and learning pathway.
- src/cv.ts:
  Browser-side CV extraction and OCR.
- backend/main.py:
  APIs, validation, SQLite, optional accounts, Gemini and evidence refresh.
- backend/engine.py:
  Python matching counterpart.
- data/catalogue.json:
  Skills, tasks, careers, learning resources, personas and source metadata.
- data/aei_subset.json:
  Selected original AI-use observations and provenance.
- data/market.json:
  Dated BLS occupational projection reference.
- public/assets/chick-careers-v2.png:
  CURRENT mascot sheet. Preserve it.
- public/assets/mascot-design.md:
  Current mascot design brief.
- public/previews/:
  Visual reference screenshots.
- tests/check_backend.py:
  Backend contract, validation, failure and account-isolation checks.
- scripts/check-parity.mjs:
  Browser/Python matching parity checks.
- scripts/package-replit.py:
  Source archive packaging.
- scripts/run-replit.sh:
  Replit build/start command.
- .replit:
  Replit configuration.
- README.md, THIRD_PARTY_NOTICES.md and LICENSE:
  Preserve and update as appropriate.

Do not casually run scripts/build_catalogue.py:
it regenerates curated catalogue data. Review intended differences first.

## 4. Existing design and flows to preserve

### Visual identity

Cream/off-white backgrounds, forest-green primary actions, sage supporting
colors, muted yellow accents, rounded panels and generous whitespace.

Fonts: DM Sans and Manrope.
Preserve existing icons, spacing, responsive behavior and modal styling.

The CURRENT chick is a newly generated character design with:

- Separate head/body proportions.
- A light face patch.
- Small oval teal eyes.
- A swept feather crest.
- Thin teal outlines.
- Occupational outfits.

Do not restore the older reference-like chick or regenerate the current
character without a user request.

Sprite sheet:
1536 x 1024 pixels, 3 columns x 2 rows.
Each cell is 512 x 512.

Avatar IDs:
0 = default, blue shirt and black trousers.
1 = accountant, sage vest and calculator.
2 = financial analyst, navy vest and chart.
3 = administrative assistant, lavender shirt, folder and mint scarf.
4 = customer support, teal shirt and headset.
5 = operations coordinator, terracotta shirt and checklist.

Existing CSS uses background-size: 300% 200%.
Keep all six characters fully visible without clipping.

### Home and demo profiles

Home offers:

- Find my next direction.
- Start with my CV.
- Try a demo profile.
- Optional Sign up / Log in.

Accountant demo:
Mei, Accountant, 4 years of experience, 4 learning hours/week.

Admin demo:
Aaron, Administrative assistant, 3 years of experience,
6 learning hours/week.

These are synthetic demo profiles, NOT email/password test accounts.
Admin means an administrative worker, not a system administrator.

The workspace also has a Demo profiles switcher.

### Four-step questionnaire

Step 1 — Your current chapter:

- Occupational chick carousel with previous/next controls.
- Custom occupation option.
- Relevant years of experience.
- Weekly learning hours.

Step 2 — Build your skill bubble:

- Tools / Work tasks / Skills tabs.
- Click or drag catalogue items to add.
- Removable skill bubbles.
- Deduplication.
- Other description input.
- Catalogue keyword fallback and optional Gemini suggestions.
- Users confirm suggested skills; tools/tasks do not prove competence.
- Unmatched descriptions remain notes and are excluded from scoring.

Step 3 — Your confidence:
Rate selected skills using these anchors:

1. Just starting.
2. With support.
3. Independently on routine tasks.
4. Confident with complex tasks.
5. Able to guide others.

Step 4 — What interests you?:

- Analysis.
- Finance.
- Data & technology.
- People & operations.
- Sustainability.
- No clear preference yet.
- Review profile before confirmation.

Confirm profile & see my top match opens a single top-direction overview first;
View learning pathway selects that direction, and Explore more opens Career Directions.

### CV import

Competition demonstrations use synthetic CVs.

Existing implementation:

- Browser processing; files are not posted to the application backend.
- Text extraction from the first three PDF pages.
- OCR for the first two scanned PDF pages or uploaded images.
- 8 MB file limit.
- Text/manual fallback and extraction timeout handling.
- Initial profile candidates use catalogue keyword matching.
- Confidence, interests and weekly learning time need user review/input.

OCR may download worker/language assets.
Do not claim the current importer is a complete live semantic CV parser.

Optional Gemini currently suggests controlled skill IDs from a submitted
short work description. Invalid IDs are rejected.

### Career Directions

Five curated target directions:

- Financial analyst.
- Business intelligence analyst.
- Compliance officer.
- Sustainability specialist.
- Payroll specialist.

Preserve:

- Explainable component scores.
- Transferable strengths.
- Potential skill gaps.
- Learning estimates.
- Sources.
- SDG target and contribution explanation.
- Two-direction comparison.
- Choose direction -> Learning Pathway.

The Focus control changes card order, not hidden score weights.

Unassessed skills must be labelled as not assessed, not confirmed incompetence.

### Future Skills Radar

Tabs:

- Your tasks.
- Career outlook.
- Across scenarios.

Keep evidence-period selection separate from scenario selection.

Show:

- Source and date.
- Geography and period.
- Observed data versus model assumptions.
- Why computed outputs change.
- Skills with high priority in both scenarios.

AI-use observations are not Malaysian adoption rates or personal job-loss
probabilities.

### Learning Pathway

Preserve:

- Catalogue-selected learning resources.
- Ordered steps and stated prerequisite assumptions.
- Estimated hours.
- Weekly time-budget recalculation.
- Source/provider links.
- SDG explanations.
- Self-reported progress.
- Export.

IMPORTANT:
Existing guest browser-save behavior is superseded by section 5.

Free learning content may exclude paid software or certificates.
Durations are team estimates, not provider promises.

### Individual scope update - 23 October 2026

The HR view and all team navigation/banner entry points have been removed at
user request. Keep the product focused on individual planning. Do not restore
HR based on historical feature descriptions.

Home now has one demo entry, Try a demo profile, with the existing Mei/Aaron
picker. The separate Accountant demo and Admin demo homepage shortcuts are removed.
The workspace Demo profiles picker remains.

After questionnaire confirmation, show only the highest-matching career first.
Its two main actions are View learning pathway (that direction) and Explore more
(the full Career Directions page). This supersedes the older direct-to-list flow.

## 5. Latest approved requirements — implement first

### P0-A: Independent My Profile page - completed locally

My Profile must be a separate workspace page.
It must NOT open the four-step questionnaire.

Desktop layout:

Left:

- User's confirmed current-occupation chick.
- Occupation label.
- Compact identity information.

Right:

- Name.
- Current occupation.
- Working experience.
- Weekly learning time.
- Skills and confidence.
- Interests.
- Edit profile button.

Default state: read-only profile overview.

Edit profile:

- Enter inline editing on the same page.
- Maintain a separate edit draft.
- Save changes validates and applies edits.
- Relevant recommendations update after confirmed changes.
- Cancel discards the edit draft.
- Do not force the user through four questionnaire steps.

Mobile:
Stack the character and profile information naturally.

### P0-B: Guest / demo / authenticated access - completed locally

Maintain explicit session provenance, for example:
guest | demo | authenticated.

Do not infer mode from the user's name, occupation or confirmed flag.

Demo status is a UI demonstration state.
It must never authorize protected account APIs.

Guest entering through Start:

- Can complete the questionnaire without login.
- Can explore career, radar and pathway results.
- My Profile opens a login/signup prompt.
- Save actions open the same prompt.
- Do not silently save guest data as an account plan.
- Closing the prompt preserves answers and current page.

For revising guest answers:
Provide a separate Review my answers action.
It returns to the current questionnaire draft and does not grant access to
an account Profile page.

Export and account save are different actions.
Guest export may remain available.

Demo profiles:

- Can view the independent My Profile page.
- Can edit profile information.
- Save updates only the current demo session.
- Feedback clearly says it is a demo/session save.
- Do not report successful cloud or account persistence.

Authenticated users:

- Can view/edit their own profile.
- Can save through protected backend endpoints.
- Server authorization remains mandatory.

There is already prototype account code in the backend.
Preserve it; do not fake authentication in the static preview.
Real integration, durable storage and cross-device behavior can be completed
later as the deployment is connected.

Login prompt copy:

Title:
Keep your next chapter with you.

Body:
Log in or sign up to view your profile and save your progress.
Your current answers will be kept.

Actions:
Log in / Sign up / Continue exploring.

Audit all related entry points:

- Sidebar My Profile.
- Existing Edit my profile buttons.
- Save my plan.
- Save changes.
- Continue a saved browser plan.

Starting a NEW guest journey after viewing a demo must not retain demo access.

Do not clear imported CV data accidentally.
Separate:

- Start a fresh journey.
- Continue a CV-imported draft.
- Review current answers.

### P0-C: Consistent personal chick - completed locally

The user's personal appearance must follow the occupation confirmed at
questionnaire step 1 throughout the application.

Preset occupation:
Keep its confirmed preset costume.

Other/custom occupation:
Keep the default blue shirt and black trousers.

Use that SAME confirmed personal appearance in:

- Career Directions.
- Sidebar.
- My Profile.
- Future Skills Radar.
- Learning Pathway.

Selecting a recommended future career must not automatically change the
user's personal chick.

Only an explicitly confirmed occupation edit changes the personal appearance.

Known causes in the existing source:

- The questionnaire applies custom/default logic but results use an older
  look index.
- Learning Pathway contains a hard-coded analyst look={2}.
- Appearance is not part of the canonical confirmed profile model.

Fix the underlying state model, not just one screen.

Store a stable occupation/avatar ID in the confirmed profile/session.
Use an explicit default for custom occupations.
Keep draft appearance separate until confirmation.

Preserve the association through:

- Navigation.
- Reload.
- Demo switching.
- Profile editing and saving.

If adding profile fields:
Update FastAPI/Pydantic models and saved-plan validation together.
The current API rejects unexpected fields.
Provide sensible defaults for old saved profiles.

Do not repeatedly guess avatars from free-text job titles.

## 6. Scoring and data rules

Current provisional score:
70% baseline skill fit

- 20% interest fit
- 10% scenario-adjusted skill fit.

These are prototype assumptions for validation.
Do NOT restore the older 50/30/20 formula.

For compatible AI-use observations:
a = observed automation-pattern share as a fraction.
d = -1 for reviewed routine-execution skills.
d = +1 for checking/oversight skills.
d = 0 for unaffected skills.

Evidence factor:
1 + 0.1 _ d _ a.
Average factors across linked tasks.

Moderate:
Use the evidence-adjusted weights.

Faster:
Additionally multiply:

- Routine execution by 0.8.
- Checking/oversight by 1.2.
- Other skills by 1.0.

Normalize role weights afterwards.

Do NOT restore the older scenario that adds 20 percentage points to observed
automation shares.

These are skill-importance assumptions, not workplace adoption estimates.

Missing evidence:
If any compared role has less than 50% compatible linked-task coverage,
omit the 10% component for ALL compared roles.
Renormalize baseline/interests to 70/90 and 20/90.
Missing observations are not zero.

Gap priority:
Adjusted skill weight \* remaining self-assessed gap.

Cross-scenario priority skills:
Intersection of both scenarios' top three positive gap priorities.
Withhold the label when compatible evidence is insufficient.

Keep TypeScript/Python parity.
LLMs do not calculate career scores or invent courses.

Evidence boundaries:

- Anthropic Economic Index, 26 June 2026 release:
  global sampled Claude.ai observations for April and May.
  These are two observation periods within one release, not two releases.
- BLS Table 1.2, 27 August 2026 release:
  U.S. 2025–2035 projections.
  Broader occupation mappings are explicitly labelled.
  Context only; excluded from match scores.
- O*NET occupation references:
  inform curated requirements; full O*NET database not imported.
- TalentCorp MyCOL / DOSM:
  linked Malaysian context; no live local salary/vacancy feed is claimed.

Backend refresh currently rechecks a PINNED AI release.
It validates values and retains the last valid catalogue on failure.
It does not automatically discover arbitrary future releases.

Do not label evidence-period switching as a successful live refresh.
Do not manufacture ranking changes for the demonstration.

Every recommended role, skill and resource needs relevant provenance.
Every recommended role and skill needs an SDG target plus an explanation.

## 7. Local development and Replit deployment

Preferred workflow:
VS Code/Codex -> GitHub -> Replit.

Use the same source project in both environments.
Local edits do not automatically update a published deployment.

Open the folder containing package.json.

Frontend-only local preview:
npm ci
npm run dev

Use the local URL printed by Vite.

Build:
npm run build

Windows PowerShell full-stack example:
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:VITE_BACKEND_ENABLED = "true"
npm run build
.venv\Scripts\python.exe -m backend.main

Open the Uvicorn URL, normally http://localhost:8000.

Adapt the interpreter command to the user's installed Python if necessary.
Do not replace the stack because an interpreter is missing.

Replit:
bash scripts/run-replit.sh

Existing .replit supplies build/start settings.
FastAPI serves built React files and /api from the same origin.

VITE_BACKEND_ENABLED is a build-time flag.
Rebuild when changing frontend-only/backend-connected mode.

Gemini server configuration:
AI_INTEGRATIONS_GEMINI_API_KEY
AI_INTEGRATIONS_GEMINI_BASE_URL

Verify the workspace's current Replit integration example before a live test.
A normal Google API key is not automatically interchangeable with a proxy key.

Keep credentials in server-side secrets.
Never put secrets in VITE\_ frontend variables, chat, logs or Git.

SQLite:
Public catalogue/observations plus optional account/session/saved-plan tables.
Verify durable deployment storage before relying on saved-account retention.

Do not commit:
.env, runtime SQLite, node_modules, build/cache outputs or session credentials.

## 8. Validation

Before the pending Profile changes, historical validation included:

- 10 backend checks.
- 9 browser/Python parity cases.

This is not proof that new edits pass.

Run appropriate checks after modifications:
npm run build
python tests/check_backend.py
node scripts/check-parity.mjs

For the parity script, BRIDGENEXT_PYTHON can specify a virtualenv interpreter
when needed.

Acceptance checks for the next task:

1. Selecting Accountant in the demo picker opens the independent Profile page with Mei's data.
2. Selecting Admin in the demo picker opens it with Aaron's data and the correct appearance.
3. Edit/Cancel preserves the original profile.
4. Edit/Save updates demo session data with truthful feedback.
5. New guest -> questionnaire -> results -> My Profile prompts login.
6. Guest Save prompts login; closing keeps answers and current results.
7. Review my answers remains available as a separate guest action.
8. Demo -> new guest does not retain demo privileges.
9. Preset occupation -> Other/custom -> confirm uses DEFAULT chick.
10. The default chick remains consistent on every personal screen.
11. Reload and revisiting pages preserve the confirmed appearance.
12. Choosing a target career/scenario does not change personal costume.
13. Profile/avatar changes do not introduce API 422 errors.
14. Hours, skills, interests and evidence/scenario switches still recompute.
15. Existing responsive and keyboard/modal behavior remains usable.

Report actual checks, remaining limitations and deployment status accurately.

## 9. Competition and continuity

Domain 1's planned core covers:

- Skills intake.
- Dated updatable AI/job-market evidence.
- Explainable matching and gaps.
- Ordered affordable learning pathways.
- Role/skill SDG contribution mapping.
- Multiple estimated future scenarios.

The primary demonstration connects evidence changes to recalculated,
explainable outputs.

HR has been removed from the current individual product scope.
Do not claim the static preview already satisfies all competition requirements.

If current official proposal, technical declaration or Domain 1 files are
provided, read them and flag real inconsistencies.
Do not invent attendance, contact information, links or evaluation results.

Create a short root AGENTS.md pointing to this handoff and recording:

- Continue the existing React/FastAPI implementation.
- Preserve the visual baseline and current mascot.
- Chinese conversation, English UI.
- Latest approved requirements override old suggestions.
- Keep score/data/SDG honesty and frontend/backend parity.
- Do not fake authentication, live updates or deployment.
- Update CODEX_HANDOFF.md after completed tasks.

Keep a completed/pending section in this file.
Move requirements from pending to completed only after implementation and
appropriate verification.


## 10. Completed / pending status - 23 October 2026

### Completed locally

- P0-A: Independent workspace My Profile, confirmed occupation chick and identity
  at left, all requested profile fields at right; same-page draft editing,
  validation, Save and Cancel; stacked mobile layout. Recommendations recompute
  from confirmed changes. Existing fractional demo confidence is preserved unless
  explicitly edited; changing a name/occupation does not round scoring inputs.
- P0-B: Explicit guest/demo/authenticated provenance. Profile and Save guest
  entry points share the approved login/signup prompt, preserving the current
  page and answers on dismissal. Review my answers is separate. New journeys
  reset demo privileges; CV import and questionnaire continuation retain their
  own draft. Guest export stays available. No new localStorage account/browser
  plans are written or silently restored. Demo saves remain session-only, even
  with an account cookie. Authenticated saves use protected APIs and handle
  expiry/failure without reporting false success. Real auth remains required.
- P0-C: Stable avatarId 0-5 in confirmed profiles, with default 0 for custom
  occupations, separate draft appearance, and one-time exact-preset migration
  for old records. Sidebar, Career Directions, Profile, Radar sidebar and both
  Learning Pathway chicks use confirmed appearance. Choosing a target career
  or scenario does not change the personal costume. FastAPI accepts and validates
  the field, and old saved plans migrate on read.
- Root AGENTS.md created; README reflects current access and persistence rules.
- Fixed an existing SQLite connection lifecycle issue exposed by Windows tests:
  transaction contexts now close handles, allowing temporary DB cleanup.

### Verification performed

- npm run build: passed (TypeScript and Vite); existing large-bundle advisory.
- .venv/Scripts/python.exe tests/check_backend.py: 12 tests passed, including
  account isolation, avatar/API roundtrip, legacy migration, invalid avatars,
  unauthenticated demo rejection and normal temporary DB cleanup.
- node scripts/check-parity.mjs with BRIDGENEXT_PYTHON: 9 cases passed.
- tests/check_ui.mjs with real headless Chrome: passed demo Mei/Aaron profile
  overview, inline edit/cancel/save, personal costumes across pages/reload,
  current-occupation draft isolation, mobile edit/layout without horizontal
  overflow, guest questionnaire/gates/save dismissal/review, demo-to-new-guest
  reset, CV draft reload, weekly hours and scenario/target changes. No page errors.
- Local browser tests use frontend-only mode; real account endpoints were tested
  through FastAPI TestClient, not a deployed browser account journey.
- Environment: Node 22.18, Python 3.14 isolated .venv; Python 3.12 was unavailable.
  Dependency authorities and intended Replit stack are unchanged. Starlette
  emits an httpx deprecation notice in tests; all tests exit successfully.
- Current v2 mascot asset, scoring formula, catalogue data and parity preserved.

### Pending

- Deploy the changed source through the existing Replit workflow; local changes
  do not update the previously published preview.
- Verify Node 24/Python 3.12 in the target Replit environment, real browser
  signup/login/logout/account save/load over HTTPS, durable SQLite hosting and
  cross-device account retention. Local TestClient success is not deployment proof.
- Configure and verify live Gemini and pinned-release evidence refresh on the
  intended backend when credentials/network are available. No live integration,
  deployment or new source validation is claimed in this task.


## 11. Latest individual-flow revision - 23 October 2026

Completed locally at user request (overrides older HR/homepage-flow descriptions):

- Removed HR overview rendering, synthetic team computation and export, homepage
  For teams navigation and team banner, and workspace team navigation.
- Removed duplicate Accountant demo / Admin demo homepage shortcut buttons.
  Kept Try a demo profile and the existing workspace Demo profiles picker.
- Questionnaire confirmation now opens one highest-matching direction with its
  score, strengths and potential learning priorities. The personal chick remains
  the confirmed current-occupation chick. No scores or data were changed.
- View learning pathway sets the displayed direction as the target and opens its
  pathway. Explore more opens the existing five-direction comparison page.
- Kept guest gates, demo session saves, independent Profile and CV draft behavior.
- Updated README and browser regression checks for the revised individual scope.

Verification: npm run build passed; real headless Chrome UI checks passed for
removed entries, retained demo selection, the top-direction page, both onward
actions and mobile layout, plus the existing profile/guest/avatar/CV checks.
The existing large-bundle advisory remains. Backend and scoring code were not
changed in this revision. Replit deployment remains pending.


## 12. Current-role growth, inclusive design and signal discovery - 23 October 2026

This section overrides older English-only, future-role-only and pinned-refresh
requirements. Existing individual scope, guest/demo/account rules and v2 mascot
remain in place. No HR view was restored and no scoring data was manufactured.

### Completed locally

- Current-role growth page: users review actual work tasks, source observations,
  skill gaps and modelled learning priorities, then build a current-role pathway.
  Only task-related skills are prioritised when tasks are selected; without tasks,
  confirmed skills are an explicitly labelled fallback. Custom titles do not infer
  occupational requirements. This mode does not display a career match probability.
- Current/future learning-goal switch, shared catalogue resources/prerequisites,
  schedules and SDG explanations. learningGoal persists in account plans; old
  records default to future. Personal appearance and access gates are unchanged.
- Local English/Bahasa Malaysia/Simplified Chinese presentation dictionaries,
  language and low-data preferences, localised catalogue search and selected
  multilingual keyword suggestions. Canonical profiles, scores, IDs, official
  course titles and source quotations remain intact. Unknown source text falls
  back to English. Preferences do not imply account-profile persistence.
- Low-data mode: no external font loads, text table instead of optional chart,
  lazy chart/PDF/OCR chunks, confirmation before PDF/image processing. Manual
  intake is available. Existing English OCR limitation is disclosed.
- backend/signals.py discovers official AEI releases, pins an immutable revision,
  validates source structure/periods/values/duplicates/coverage, preserves source
  provenance per historical period, and atomically activates compatible data.
  Unknown formats require review; failed checks retain validated evidence.
- Update history and API status; radar displays actual checks and observation
  differences. Newly added evidence periods work with matching and saved plans.
- In-process six-hour checks while backend is running, configurable with
  BRIDGENEXT_SIGNAL_INTERVAL_SECONDS (minimum 300). First automatic check waits
  the interval; manual checks remain available. This cannot wake a stopped host.
- Highest-match page now also links occupational evidence and shows role SDGs.

### Actual verification

- npm run build: TypeScript/Vite passed; chart split into a separate lazy chunk.
- tests/check_backend.py: 12 checks passed; tests/check_signals.py: 7 checks passed.
  Future-release, incompatible-schema, duplicate/NaN/coverage and failure cases
  use synthetic fixtures only. New months match/save and old data are retained.
- scripts/check-parity.mjs: 9 future-role and 11 current-role cases passed,
  including a custom title with no tasks and task-scope exclusion of irrelevant
  assessed skills. Future-role score formula remains 70/20/10.
- Existing Chrome UI regression passed; inclusive Chrome checks passed three
  languages, Chinese intake suggestions/edit cancellation, current-role path,
  canonical data unchanged, goal switching/reload, session save, Chinese/Malay
  mobile layout and persisted low-data text radar. No browser page errors.
- Live, read-only official-source validation succeeded: six releases discovered;
  newest was 2026-06-26, commit 4e5f69fab13a9c3f7d0dcc31a6f893a9818738f6.
  Complete compatible observation parsing found 0 changed fields (unchanged).
  This check did not write project datasets or a deployment database. A new
  future release has not been observed live; acceptance is tested with fixtures.
- Runtime backend adapter is backend/signals.py. scripts/fetch_evidence.py is
  retained as a legacy pinned offline import utility. Do not confuse the two.

### Remaining boundaries

- Replit deployment, HTTPS browser account flow and durable hosting remain pending.
- The scheduler is implemented and starts/stops with FastAPI, but has not undergone
  a six-hour deployed soak test. A sleeping/stopped deployment does not poll.
- Future source formats and metric meaning may still need human adapter review.
  BLS remains a dated contextual reference; no live Malaysian vacancy feed added.
- Malay translations need native-language editorial review. Official resources
  may be English; OCR remains English. No full offline/PWA behavior is claimed.
- Live Gemini remains unverified. Keep public/synthetic profiles for competition
  demos; do not introduce real personal CVs into competition demonstrations.


## 13. My Achievements and Data saver removal - 23 October 2026

Latest approved scope overrides section 12's low-data mode. Preserve the current
individual journey, normal radar, three languages, v2 mascot and existing access
rules. HR remains removed; the optional demo-profile picker remains.

### Completed locally

- Removed Data saver/Low data controls, automatic Save-Data mode and alternate
  radar table. Old bn-low-data preference is cleared. Normal fonts/radar remain;
  chart/PDF/OCR lazy loading and mobile layouts are preserved.
- My Achievements workspace page in English/Malay/Chinese, with an empty state,
  commemorative badge cards, completion dates, resource/skill/SDG snapshots,
  learning reflections and original source links. User reflections are not translated.
- A non-empty pathway must have every step marked complete before collection.
  The user writes a 10-1000-character reflection and explicitly attests completion.
  A celebration dialog links to the collection. All badges say self-reported
  completion, not skill/attendance/professional certification. Skill ratings do
  not change when a badge is recorded. No pre-earned demo badges were fabricated.
- Completed-pathway snapshots are stored independently of saved current plans.
  The unique path key is goal + target + sorted resource IDs; repeat collection
  does not duplicate a badge, including after reload or changing weekly hours.
- Explicit demo provenance remains mandatory. Mei/Aaron collections are isolated
  in browser session storage and never sent to account APIs, even with an account
  cookie. Signing in loads the real account collection, not the demo collection.
- Guest collection and award entry points share the login/signup gate. Dismissing
  it preserves current page and temporary completion progress.
- GET/POST /api/achievements require real server authorization. POST validates
  Origin, reflection/attestation, confirmed profile, goal/period/scenario, and all
  required resources computed on the server. The achievements table is scoped by
  account and path key, and retains snapshots independently of plans.
- Retained the optional Try a demo profile picker. No hard-coded login account
  or prepared fictional completion record was added. README includes a suggested
  presentation flow and guidance to use synthetic information with real login.

### Verification

- TypeScript/Vite build passed in frontend-only and backend-connected modes.
- 12 existing backend + 7 signal + 4 achievement tests passed. New checks cover
  protected routes, Origin, incomplete/empty/invalid claims, duplicate awards,
  independent history, goal changes and account isolation.
- 9 future-role + 11 current-role parity cases passed; an additional 20 cases
  verify server completion resources exactly match browser pathway resources.
- Existing UI and inclusive UI checks passed. Dedicated achievement UI checks
  passed empty state, complete/reflect/attest, reload, duplicate prevention,
  demo switching, goal changes, three languages, mobile and guest gates.
- Real Chrome account smoke test against a local FastAPI backend passed actual
  signup/login, demo-cookie isolation, account collection, reload and logout
  authorization. This used only synthetic identities and an isolated temporary
  SQLite database via tests/serve_test_backend.py. The test service was stopped.
- No production account or production database was used. Replit deployment,
  HTTPS/durable deployment retention and native Malay editorial review remain
  pending. The existing Starlette/httpx deprecation notice remains in tests.


## 14. Saved Pathways and consolidated learning page - 23 October 2026

Latest user-approved layout: remove the standalone Grow in my current role page
and sidebar entry. Both learning goals live in Learning Pathway. Current-role
mode retains expandable task selection, trend evidence and skill priorities.
Keep the independent Profile and Achievements pages and the existing mascot.

### Completed locally

- Independent Saved Pathways library, with sidebar and learning-page links,
  three-language empty/loading/error states and responsive cards.
- Save my plan stores multiple goal/target/resource-set snapshots, including
  weekly budget and completed steps. Re-saving the same route updates its entry.
- Open restores original resource steps, goal/scenario, schedule and saved
  progress. It does not replace the current profile or personal chick. Saved
  metadata is clearly labelled; Use latest recommendations leaves snapshot mode.
  Explicit new career/goal choices also clear the opened snapshot.
- Confirmed removal of a library item preserves completed achievements. Account
  saved-snapshot completion is validated against the owned stored resources,
  even after current recommendations change.
- Protected account GET/POST/DELETE /api/saved-pathways, Origin checks, validated
  server-generated resources, account ownership and independent storage.
- Legacy single-account plans migrate once at first library-table creation.
  Removed library entries do not reappear at restart; existing /api/plan remains
  available for profile/account-plan compatibility.
- Demo libraries isolated per Mei/Aaron in browser session storage; no account
  calls while in demo mode, even with a real login cookie. Guest library/save
  actions use the existing login/signup gate and preserve current work.
- No scoring/data formulas, badges, current-role scope rules, languages or
  occupation/avatar associations were replaced. No HR/Data saver restored.

### Actual verification

- TypeScript/Vite frontend-only and backend-connected builds passed.
- 12 backend + 7 signal + 4 achievement + 5 saved-pathway checks passed (28 total).
  New checks cover ownership, invalid/empty routes, multiple goals, updates,
  historical resources/progress/badges and one-time legacy migration/removal.
- Existing 9 future-role + 11 current-role + 20 completion-resource parity cases
  passed; the matching formula is unchanged.
- Browser suites passed original questionnaire/profile/avatar/CV flows,
  achievements, revised inclusive learning layout, saved snapshots/progress,
  reload, unchanged personal profile, demo isolation, remove, guest gates and
  Chinese/Malay mobile layout.
- Local connected Chrome test passed real signup/login, demo-cookie isolation,
  account library save/open, progress after reload, saved-snapshot badge award,
  achievement retention and logout authorization. Synthetic data and isolated
  temporary SQLite only; not a deployed Replit account or durable-storage test.
- README updated. Replit deployment and the previously listed live-hosting,
  native Malay review and Gemini limitations remain pending.


## 15. Input-derived test prototype workspace - 23 October 2026

User approved implementation after discussing the alternatives. This section
supersedes earlier frontend demo/authentication entry-point requirements.

### Completed locally

- Removed sidebar Review my answers, Home Try a demo profile, the workspace
  Demo profiles switcher and the ready-made Mei/Aaron picker. The catalogue
  personas remain test fixtures; no new fictional personal data is loaded.
- Frontend explicit provenance is guest | prototype, never inferred from name
  or occupation. Log in immediately activates the test prototype identity.
  Removed frontend signup/password UI and automatic real-cookie account restore.
- Occupation, experience, weekly budget, skills/confidence, interests, tasks and
  personal avatar come from the current session. Unfinished questionnaire/CV
  drafts retain their data and unconfirmed status; no guessed competence.
- Guest My Profile, Saved Pathways and My Achievements retain the common prompt.
  Clicking Log in opens the exact requested page. Closing it keeps current work.
- Save-triggered login completes the original pending save immediately, including
  checked steps, then offers View saved pathways. No second Save click required.
  Badge-triggered login resumes reflection/attestation, never auto-awards a badge.
- My Profile retains inline Edit/Save/Cancel. Home Continue questionnaire draft
  still resumes unfinished work. All personal pages keep the confirmed chick.
- Saved pathways and self-reported achievements use bn-test-pathways and
  bn-test-achievements in sessionStorage. No old Mei/Aaron collection migration,
  prepared awards, cloud-save claim or cross-device persistence. Unsaved progress
  is temporary; save explicitly to retain progress in a pathway snapshot.
- Exit prototype returns to guest gates while retaining current answers and the
  same browser session's collections for re-entry. Guest buttons do not reveal
  test's collected-badge status. Starting a fresh questionnaire while test is
  active keeps prototype access and existing collections.
- English, Bahasa Malaysia and Chinese labels explicitly identify prototype
  access and browser-session storage. Existing visual baseline/assets preserved.
- Frontend test operations never call /api/auth/*, /api/plan, /api/saved-pathways
  or /api/achievements, even with a real cookie. Public matching/catalogue/evidence
  APIs still work in connected builds. No fake user/password/session was inserted
  into SQLite. Real authorized account APIs and their validation remain intact
  for later integration; the current presentation UI uses local prototype access.

### Actual verification

- Frontend-only and backend-connected TypeScript/Vite builds passed.
- Existing 28 backend checks passed; 9 future-role + 11 current-role + 20
  completion-resource parity cases passed. Scoring/data formulas are unchanged.
- Browser suites passed profile/edit/cancel, stable custom/preset avatars,
  questionnaire top match, CV draft login/resume, three languages, mobile,
  achievement reflection/attestation/deduplication, saved snapshot/progress,
  reload, remove, guest gates, exit/re-entry and separate browser sessions.
- Dedicated prototype check passed pending-save login/cancel, input preservation,
  page destinations and badge-login continuation without fabricated awards.
- Connected Chrome test used a real synthetic account in an independent temporary
  database. Its cookie did not override test. Browser private API request count
  was zero; the real account plan/library/collection remained untouched. Local
  reload worked and backend routes remained protected after server logout.
- README and browser regression suites updated. This is local verification only:
  no Replit deployment, durable hosting, native Malay review or Gemini validation
  was performed in this change. Existing Starlette/httpx deprecation notice stays.


## 16. Plain-language Future Skills Radar - 24 October 2026

Latest approved requirement: make this page understandable at a glance for
non-specialists while retaining honest sources and the existing visual design.
This presentation supersedes the older three-tab radar layout in earlier sections.

### Completed locally

- Extracted the radar into src/FutureSkillsRadar.tsx, within the existing
  React/TypeScript app. Cream/green cards, existing buttons and personal v2 chick
  remain. Sidebar name Future skills radar is preserved.
- Start with a short current-work learning summary, using currentRole and up to
  three priorities. No selected tasks -> explicitly labelled rated-skill fallback.
- Tabs: Changes at work / Skills to build / Career outlook. Accessible tab roles,
  arrow/Home/End navigation and English/Malay/Chinese labels are included.
- Task cards describe the observed AI-led/collaborative mix in plain language.
  Raw percentages, month and original source observation expand on demand.
  No-task views label catalogue examples; missing data never becomes zero.
  Copy explicitly separates observed use from capability, accuracy and job loss.
- Skills to build shows priority skills, descriptions and self-rating/not-rated
  states. Both current-work and future-career actions open the intended learning
  goal and clear stale saved snapshots without altering the confirmed profile.
- The original moderate/fast comparison is now optional and explained as
  Today's work / More AI-led work. Existing canonical scenario IDs and formulas
  remain. Shared top-three claims still require sufficient evidence coverage.
- Sources/update status and latest-two-month match comparisons are collapsed
  details. Month comparison is labelled recommendation stability, not personal
  progress. Original validated-refresh backend and source history are preserved.
- Career outlook retains actual packaged BLS figures, broader mappings and
  separate MyCOL/DOSM context. Irrelevant AI month/scenario controls are absent.
- Self-ratings are optional details; the lazy chart displays only rated-group
  averages and requires three assessed groups. Unrated skills no longer depress
  this display toward zero. Matching and learning calculations are unchanged.
- Reused catalogue task-skill links and source observations; no datasets,
  backend formulas, authentication, saved snapshots or achievements were rebuilt.

### Actual verification

- Frontend-only and backend-connected TypeScript/Vite builds passed.
- Existing profile/avatar/CV and inclusive/current-role browser suites passed
  with the new radar entry points. New radar suite passed actual/missing dataset
  observations, initially collapsed percentages, keyboard navigation, current and
  future learning actions, selected-task filtering, confirmed-input preservation,
  assessed-only lazy charts, three languages and mobile overflow/layout checks.
- Existing parity passed: 9 future-role + 11 current-role + 20 completion-resource
  cases. Presentation changes did not alter TypeScript/Python scoring parity.
- Desktop and mobile screenshots were inspected. Tests use isolated Chrome
  sessions; no live source refresh or production database write was required.
- README updated. This is local implementation, not a Replit deployment; previous
  durable-hosting, native Malay review and Gemini limitations remain.


## 17. Visible five-group chart and centralized sources - 24 October 2026

User approved removing the large radar source/update block and restoring the
previous pentagonal skill visualization prominently, preserving simplified tabs.
This supersedes section 16's hidden-chart/three-assessed-group display requirement.

### Completed locally

- The original five groups (Data, Finance, Quality, People, Judgement) are fixed
  axes again. The self-assessed 1-5 chart is always visible beside the learning
  summary on desktop and stacked below it on mobile; Recharts remains lazy.
- Only rated skills contribute to group means. Not assessed is explicit in the
  chart legend. Partial profiles draw assessed points only; they do not fill a
  polygon through unknown groups or draw them as zero. All five rated groups
  produce the filled shape. Individual skill ratings remain available below.
- Custom radar shape avoids Recharts' default null-to-centre rendering. Tooltip,
  accessible chart label, visible legend and English/Malay/Chinese labels remain.
- Removed the large Sources, updates & how this works block from the radar page.
  Compact source/month context stays beside the content and links to the existing
  Evidence & sources dialog. Career outlook keeps its own BLS source/period.
- Extracted src/EvidenceDetails.tsx for the dialog: source/version metadata,
  refresh action, real check history, model explanation and optional latest-two-
  month matching comparison remain available. Public update status loads when
  the sources dialog opens; no private account API is used for this functionality.
- Matching, task evidence, scenario rules, saved plans, achievements and personal
  avatar model are unchanged. No dataset regeneration or live refresh fabricated.

### Actual verification

- Frontend-only and backend-connected TypeScript/Vite builds passed.
- Radar browser checks passed fixed five axes on sparse/full profiles, no filled
  shape for unrated groups, exact assessed-only averages (including two unequal
  ratings in one group), completed polygon, tab keyboard navigation, task data,
  both planning goals, centralized source dialog/refresh, three languages/mobile.
- Existing inclusive/current-role and profile/avatar/CV browser suites passed.
- Existing parity passed: 9 future-role + 11 current-role + 20 completion-resource
  cases. Desktop and Chinese mobile screenshots were inspected.
- README and continuity pointer updated. Local implementation only; Replit
  deployment, durable hosting, native Malay review and Gemini limitations remain.


## 18. Verified unused-file cleanup - 24 October 2026

User requested removing unused files and explicitly required normal website
operation to be preserved. Cleanup was limited to proven redundant/generated
files; unreferenced-at-runtime maintenance and evidence files were not assumed
useless merely because the frontend does not import them.

### Completed locally

- Audited source references, runtime fetches, build/deployment inputs, tests,
  maintenance scripts, documentation and asset hashes. All 10 frontend modules
  are reachable; all backend modules have runtime or test/maintenance purposes.
- Removed public/catalogue.json, an obsolete static copy never fetched by the
  current browser or backend. Canonical data/catalogue.json is unchanged, checked
  by SHA-256 before/after. React imports it and FastAPI provides /api/catalogue.
- Removed public/previews/BridgeNext-preview.jpg after confirming identical
  SHA-256 with retained BridgeNext-mascot-v2.jpg. Current chick-careers-v2.png,
  design provenance and one visual baseline reference remain.
- Cleared 24 temporary browser screenshots, 6 project .pyc files and the
  TypeScript incremental cache, plus their two empty Python cache directories.
  These may be regenerated by tools. Total initial files removed: 33.
- Catalogue generator now writes only data/catalogue.json, avoiding recreation
  of the unused public copy. The generator was NOT run; no curated data changed.
- Source packaging now prunes .test-tools as well as dependency/build/cache
  directories, excluding local check artifacts from source delivery. Factored
  package_source(out) permits verification in a temporary directory without
  overwriting the public download archive or writing a project database.
- Retained all app code, tests, manual import/build utilities, source evidence,
  licences, package-lock.json, .env.example, .replit, run-replit.sh and working
  dependencies/environments. No production data or deployments were modified.

### Actual verification

- Frontend-only and backend-connected TypeScript/Vite builds passed. Fresh dist
  does not contain the deleted static catalogue or duplicate preview.
- All 28 backend checks passed; 9 future-role + 11 current-role + 20 completion-
  resource parity cases passed. Existing Starlette/httpx deprecation stays.
- Chrome tests against the built frontend and a temporary FastAPI database passed
  prototype login/save/badge/reload, questionnaire/profile/avatar/CV/mobile flows,
  and real-cookie isolation from test collections. Test service was stopped.
- HTTP 200 verified for homepage, built JS/CSS, current mascot, retained visual
  reference, health and canonical catalogue API. No runtime code relies on either
  removed public file.
- Source archive audit passed: 54 source files at the time of the check, including
  Replit configuration, runtime assets, evidence and notices; tool/runtime caches
  excluded. Archive created only in a temporary directory, then cleaned up.
- README updated. No Replit deployment or live-source refresh was performed;
  existing deployment/persistence/Gemini limitations remain.


## 19. Pastel cards and lightweight interactions - 24 October 2026

Latest user approval: enrich the card colour palette and add animation and
interaction while retaining the existing website, mascot and technology stack.

### Completed locally

- Added src/interaction.css after the existing stylesheet. Six related pastel
  tones (sage, honey, sky, lavender, mint, peach) complement existing cream and
  forest-green colours. Home steps are enclosed colour cards; careers, task
  cards, interests, pathway steps, profile identity and saved collections share
  the palette. Colour is decorative, not a scoring or employment-risk signal.
- Home step actions use confirmed destinations or resume an unfinished draft.
  They do not replace unfinished input with fictional profiles or discard it.
- Skill-chart group buttons support keyboard/touch exploration, reveal actual
  self-ratings or explicit missing assessments, and highlight the selected point.
  Five axes and assessed-only averages remain; no profile mutation on exploration.
- Added short card/button hover and press feedback, selected-interest emphasis,
  page/tab/chip/dialog entry, progress transitions and step-completion feedback.
  A decorative ten-piece celebration occurs only after explicit badge collection,
  is hidden from assistive technology and creates no extra achievements.
- IntersectionObserver progressively reveals home panels; unsupported browsers
  retain visible content. Reduced-motion overrides disable animation/transition
  and keep all content/actions visible, including after preference changes.
- Existing personal chicks, English default and Malay/Chinese translations remain.
  New action/interaction labels have local translations. No new dependencies.
- Narrowed the mobile decorative orbit to eliminate a measured 9px horizontal
  overflow. Mobile card spacing and long-language controls were verified.

### Actual verification

- Frontend-only and backend-connected TypeScript/Vite builds passed.
- New presentation browser suite passed distinct card colours, real home actions,
  draft preservation, hover after entry animation, keyboard chart exploration,
  unchanged canonical self-ratings, honest completion/celebration, reduced motion
  and English/Malay/Chinese mobile layouts without horizontal overflow.
- Existing profile/avatar/CV, radar, saved-pathways, inclusive/current-role and
  achievement browser suites passed (six browser suites including the new one).
- Existing parity passed: 9 future-role + 11 current-role + 20 completion-resource
  cases. No scoring/data/backend formulas, authentication rules, storage semantics
  or deployment configuration changed.
- Desktop and Chinese/English mobile screenshots were inspected; local Vite
  preview is available on http://127.0.0.1:5173 for review. README updated.
- No Replit publication or live source refresh was performed. Existing backend,
  durable-hosting, Gemini and native Malay-review limitations remain.


## 20. Compact personal insights and task comparison - 24 October 2026

Latest user approval: use a task comparison chart plus personal strengths and
learning suggestions, retain the five-group chart, reduce empty card height, and
remove the three homepage display cards' footer actions. This supersedes the
home action links in section 19 and the older summary/task-card presentation.

### Completed locally

- Replaced the stretched current-work summary with two content-sized cards:
  Your strengths and Skills to strengthen. Cards align at the top and keep their
  own heights; the existing five-group snapshot remains alongside on desktop
  and stacks on smaller screens. Lazy chart loading reserves its normal space.
- Strengths show up to three current-work-relevant skills actually rated 4-5/5.
  Improvement suggestions show up to three assessed skills below 4/5, preserving
  the existing currentRole model's gap ordering and task/scenario relevance.
  Self-ratings are explicitly not certifications or measured future demand.
- Relevant unassessed skills have a separate Not yet assessed section and profile
  review action. They are not labelled weaknesses. Unconfirmed CV zero placeholders
  are excluded from rated lists, chart averages and plotted points; skill-priority
  rows also identify them as unrated. No scoring formulas or stored inputs changed.
- Grow in my current role opens the existing current-goal pathway with actual
  profile inputs and catalogue learning resources, clearing any saved snapshot.
  Existing guest profile gates and input-derived test access remain intact.
- Replaced repetitive task cards and identical expanders with one shared horizontal
  comparison chart. Each task shows original AI-led/working-together percentages,
  related skill chips and a Source action opening the existing evidence dialog.
  Legend and numerical labels make the chart usable without relying on colour.
- Missing observations remain unavailable, never zero. Selected tasks restrict the
  rows; absent tasks explicitly show catalogue examples. Conversation patterns
  are distinguished from capability, accuracy, job replacement and Malaysian
  adoption. Task-to-skill mappings are explicitly described as curated.
- Home's three pastel journey cards are static displays again: removed footer
  action buttons/arrows and hover navigation cues, preserving colour/entry effects.
  Main journey controls and unfinished-questionnaire continuation remain.
- Added English/Malay/Chinese strings, accessible task chart/source labels and
  responsive layouts. Five-group exploration, scenario controls, BLS context,
  centralized sources, original chick, reduced motion and technology stack remain.

### Actual verification

- Frontend-only and backend-connected TypeScript/Vite builds passed.
- New check_insights_ui browser suite passed compact card heights, relevant high
  ratings, assessed priorities, unassessed-only and fully rated cases, CV draft
  zero placeholders, actual current-role resources and unchanged profile inputs.
  Desktop, 900/768px tablet and 390px English/Malay/Chinese layouts passed; tests
  wait for the responsive chart to finish resizing before checking overflow.
- Existing radar, presentation, inclusive/current-role, profile/avatar/CV,
  saved-pathways and achievement browser suites passed (seven including insights).
  Real/missing task percentages, source access, both goals, partial/full chart,
  keyboard exploration, draft resumption and reduced motion remain covered.
- TypeScript/Python parity passed: 9 future-role + 11 current-role + 20 completion-
  resource cases. No backend, catalogue, evidence or scoring formulas changed.
- Desktop and Chinese mobile screenshots inspected. README and AGENTS continuity
  pointer updated. Local Vite preview: http://127.0.0.1:5173.
- No Replit publication or live-source refresh performed. Existing hosting,
  persistence, real-authentication, Gemini and native Malay-review limits remain.


## 21. Gemini extraction and computed-result explanations - 24 October 2026

User approved connecting Gemini for skill suggestions and result explanations.
The current local environment has no model credentials. User is unsure how to
activate the Replit integration; instructions and a live smoke-check command are
now supplied. Do not report real Gemini success or deployment until verified.

### Completed and verified locally

- Added backend/gemini.py for the existing server-side Replit integration. Default
  model remains gemini-2.5-flash; GEMINI_MODEL permits a compatible model override.
  Validates HTTPS configuration, uses structured JSON output, one attempt, a
  12-second HTTP timeout and 15-second overall deadline, and closes the async SDK
  client. Error responses expose no keys, endpoint, prompts or raw provider errors.
- Skill extraction accepts only controlled skill IDs, rejects malformed/extra
  fields and unknown IDs, deduplicates suggestions, and requires human review.
  It does not extract task IDs or infer confidence. The UI explicitly opts in to
  sending a description. With AI off, keyword matching remains local. Provider
  failure labels the keyword fallback; a valid empty AI result stays empty.
- Added POST /api/explanations. The backend validates the confirmed profile,
  selected role, period, scenario, goal and locale, then recomputes scores,
  priorities, resource order and time budget using unchanged shared engine code.
  Model wording cannot supply scoring fields or choose new resource/skill IDs.
  Numeric and URL claims in prose are rejected. Qualitative wording still needs
  human review; these checks do not prove every generated statement is factual.
- Explanation requests exclude names, free occupation/experience text and CVs.
  The UI sends only skills/ratings, interests, selected tasks and study settings.
  No provider prompt/response database storage or caching was added. Provider/host
  retention is governed separately by their service settings and terms.
- Highest-match results and live pathways offer Understand this recommendation.
  Only Ask Gemini to explain triggers a model request. Current/future goals and
  English/Malay/Chinese output are supported. Saved snapshots skip fresh AI text.
  Failed requests show labelled standard guidance; profile/goal/hours/evidence/
  language changes cancel requests and clear stale explanations.
- GET /api/ai/status reports configuration presence only, never live verification.
  AI endpoints share an in-process per-client limit of 12 requests/minute. These
  limits are a prototype safeguard, not a distributed production quota service.
- Added scripts/check-gemini.py: default checks configuration without model calls;
  --live makes two explicitly billable synthetic requests and succeeds only when
  both return genuine Gemini results and extraction finds a supported skill.
  It reads the packaged catalogue without modifying the application database.
- README includes Replit Agent activation instructions, server variable names,
  proxy compatibility checks, live verification and republishing steps. Updated
  .env.example; added local Vite /api proxy to FastAPI localhost:8000.
- Both frontend-only and backend-connected TypeScript/Vite builds passed.
  14 new Gemini backend checks plus 28 existing backend checks passed (42 total).
  Tests cover SDK HTTP routing/schema with mocked transport, invalid IDs, consent,
  configuration, privacy, both goals, no-step pathways, failure modes and limits.
- 40 TypeScript/Python parity cases passed: 9 future-role, 11 current-role and 20
  completion-resource. Matching weights, datasets and resource selection unchanged.
- New Gemini browser checks passed with clearly synthetic provider fixtures:
  opt-in/review, valid-empty result provenance, labelled failures, minimal payload,
  stale-response cancellation, both goals, three-language mobile and no private
  account calls. Passed again against the final connected build.
- Existing profile/avatar/CV and prototype suites passed against the temporary
  connected backend; radar, personal-insights and inclusive suites passed against
  the frontend-only preview. Presentation suite also passed pastel colours,
  static home cards, chart exploration, reduced motion and three-language layout.
  Existing Starlette/httpx and Python SDK deprecation notices remain.
- User later reported missing colours on localhost. Actual browser inspection of
  localhost:5173 verified home card backgrounds #fff6df / #edf5fa / #f4effa and no
  footer links. All six tones remain in source and built CSS. The shared task
  comparison currently uses a white outer card and coloured bars; individual
  pastel task backgrounds were lost when replacing the former six large cards.
  Explained this distinction; no further visual change was made without clarifying
  whether this is the area the user means. Screenshot: .test-tools/current-home-colours.png.

### Remaining external verification

- Enable Google Gemini via Replit AI Integrations in the user's own project,
  approve its managed integration prompt and compare its current Python example.
  Run python scripts/check-gemini.py --live there, then test both UI actions.
  No secrets should be sent in chat or placed in browser VITE_ variables.
- No genuine live model response has been verified locally. SDK and browser success
  tests use mocks and are not evidence of sponsor/model usage. No Replit deployment
  was performed. Native Malay review and durable hosting limits remain.


## 22. Localhost version mismatch diagnosed - 24 October 2026

- User supplied a screenshot of localhost:5000 without the pastel home panels.
  The prior colour check had inspected localhost:5173, a different server.
- Verified localhost:5000 serves the older Downloads/BridgeNext/dist build:
  index-cMoSqLUU.js and index-D1aB2hOk.css. That folder has no interaction.css;
  its backend defaults to port 5000. This explains the screenshot's missing colours.
- Current edited workspace is Downloads/BridgeNext-Replit/BridgeNext-Replit.
  Its Vite preview is localhost:5173; actual home backgrounds and presentation
  checks confirm the pastel panels. Its built CSS also contains all six tones.
- Both folders exist separately. Latest palette, compact insights and Gemini
  integration edits are in the current workspace. No files were copied between
  projects and no other project's server or data was changed for this diagnosis.


## 23. Primary project migrated to Downloads/BridgeNext - 24 October 2026

User explicitly approved merging the latest implementation into the existing
Downloads/BridgeNext repository. This directory is now the primary working copy.
Open it in VS Code for future changes. The full local app remains localhost:5000.
The former Downloads/BridgeNext-Replit/BridgeNext-Replit copy is retained as a
reference and must not be treated as the primary editable project.

### Completed and verified locally

- Backed up affected destination files, its previous dist build and a consistent
  SQLite snapshot at C:/Users/cminh/Downloads/BridgeNext-backup-20261024-104905.
  A manifest records the before hashes and which files were added/replaced.
- Merged 25 selected application, test and continuity files: six-tone palette,
  static homepage panels, compact strengths/priorities, five-group chart,
  task comparison and optional Gemini extraction/explanations. No blanket folder
  replacement, dependency copy, Git reset, commit, push or Replit publication.
- Preserved the destination's Git repository, favicon/index.html, package/lockfile,
  credentials, runtime storage, requirements (including its Replit compatibility
  pins), .replit workflows/Autoscale/uv configuration and post-merge/run hooks.
  Existing unused legacy public files remain; no destination file was deleted.
- Merged default backend port 5000 and a Vite /api proxy to localhost:5000.
  Built frontend-only and backend-connected variants in the external backup
  directory first. Switched dist to the verified connected build and restarted
  the destination backend. The old build remains in the backup directory.
- Verified HTTP 200 on the homepage, palette CSS, favicon, health and AI-status
  routes. Actual Chrome inspection of localhost:5000 confirms homepage card
  backgrounds #fff6df / #edf5fa / #f4effa and no card footer navigation.
  Screenshot: .test-tools/localhost-5000-colours.png in the primary directory.
- Python 3.12.10 destination environment passed all 42 backend checks and 40
  TypeScript/Python parity cases. Both production builds and git diff --check
  passed. Existing Node environment is 22.18; Replit target remains Node 24.
- Browser suites against localhost:5000 passed profile/avatar/CV, prototype
  save/badge/access flows, Gemini UI with explicit synthetic fixtures, and
  personal-insight behaviour. Radar, inclusive/current-role and presentation
  suites passed on an isolated frontend-only build because those suites expect
  offline refresh behaviour. Seven browser suites passed in total.
- An initial inclusive test against the connected service accidentally triggered
  a public evidence check. Reverted its catalogue/source-observation/audit changes
  to the pre-migration snapshot. All private tables were checked unchanged before
  and after, and all eight public/private table contents match the snapshot.
  The final database may have different SQLite file bytes due to the transaction;
  logical records and the preserved source JSON datasets are unchanged.
- README, AGENTS and replit.md point to the primary folder and Gemini instructions.
  Original working-copy documents also point here to prevent split edits.

### Remaining boundaries

- Gemini is still not configured locally; mocks prove request/validation/UI
  behaviour, not a live model or sponsor-resource connection. Enable and verify
  the integration in Replit using the documented --live smoke check.
- Local merging does not update an existing Replit deployment. The destination's
  pre-existing publishing/install and durable-storage limitations remain; do not
  claim them fixed by this merge. No real user study or native Malay review.
