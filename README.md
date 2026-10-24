# BridgeNext — EyeScream interactive prototype

A guest-first career planning application for working adults. The first catalogue focuses on Malaysian financial operations and related administrative work. This revision adds a chick-led four-step questionnaire, CV import, career comparisons, a future skills radar, time-budgeted pathways, and a focused personal planning journey.

## Try it

1. Home → **Find my next direction**. Choose a current occupation, experience and weekly study time.
2. Add Tools / Work tasks / Skills by clicking or dragging. Task selections suggest catalogue skills; users review and rate them. Unknown descriptions are retained as notes and excluded from matching.
3. Rate every selected skill on the anchored 1–5 confidence scale. Select interests, review and confirm the profile to see its highest-matching direction.
4. The top-direction overview shows one highest match, strengths and learning priorities. Choose **View learning pathway** to start that direction, or **Explore more** to compare all five directions, score explanations, sources and SDG contributions. Two directions can be compared side by side.
5. In **Future skills radar**, start with a short current-work learning suggestion, then use **Changes at work**, **Skills to build** or **Career outlook**. Task cards explain AI usage patterns in words; raw percentages and sources expand on demand. Skills to build supports both current-work and future-career plans. The five-group self-rating chart is visible near the top. Model comparisons remain optional; source updates and month-to-month matching checks are available through **Evidence & sources**.
6. In **Learning pathway**, switch between **Grow in my current role** and **Prepare for a new role**. The current-role mode contains an expandable task/trend/skill-priority review; there is no separate current-role page. Change weekly hours, open provider resources, mark personal progress, save in the test prototype session, or export Markdown. Guest Save opens a login prompt; clicking **Log in** opens test with the current answers and completes that pending save. The notification links to **View saved pathways**.

The ready-made Mei/Aaron demo picker and workspace switcher have been removed. **Log in** now immediately opens an explicitly labelled **test prototype workspace**, using the user's current occupation, experience, skills, confidence, interests, weekly hours and personal chick. No email/password or backend login is performed. This is presentation access stored in sessionStorage, not real authentication or cloud persistence. Guest My Profile, Saved Pathways and My Achievements share the prompt; logging in opens the requested page. Closing it keeps the current page, answers and temporary progress. Login during the questionnaire or CV draft preserves those inputs and their unconfirmed status.

My Profile remains an independent read-only overview with inline Edit, Save and Cancel. The sidebar Review my answers action has been removed; use My Profile to edit after opening test. Continue questionnaire draft remains on Home for unfinished questionnaires. The avatar menu offers Exit prototype: it returns to guest access, keeping the answers and this session's test collections for re-entry. A fresh questionnaire keeps explicit prototype access if already active; it does not erase the existing library or achievements. Export is still available to guests. Legacy Mei/Aaron collections are not imported into test.

Personal chick appearance is stored as `avatarId` in the confirmed profile. Custom occupations explicitly use 0 (blue shirt/black trousers); target careers and scenarios never change it. Draft occupation changes apply only after confirmation. Legacy profiles migrate once at storage/API boundaries using exact preset titles, with default 0 for unknown titles.

## Current-role growth and inclusive design

The **Grow in my current role** mode within Learning pathway uses the user's selected tasks to determine relevant skills and their importance. If no tasks are selected, confirmed skills provide an explicitly labelled fallback. Custom occupations are never assigned requirements by guessing their title. Observed task signals are displayed separately from modelled learning priorities; no current-role match probability is invented. The shared catalogue supplies resources, prerequisites, time estimates and skill/role SDG explanations. `learningGoal` is persisted with account plans and defaults to `future` for older records. Completed learning remains available when switching goals.

English is the default UI; Bahasa Malaysia and Simplified Chinese are available from the language selector. Local dictionaries translate navigation, questionnaires, skills, explanations, current-role guidance, profiles, save prompts and learning instructions without calling a translation service or changing canonical IDs/data. Official course titles, source quotations and user-written content keep their original form; unrecognised external messages fall back to English. Language is a local device preference, not an account-profile save. Malay wording has not had a professional native-language review.

The Data saver toggle and alternate low-data mode have been removed. The skill chart is visible at the top of Future Skills Radar and loads on demand when that page opens. It keeps the original five groups (Data, Finance, Quality, People, Judgement). Group averages exclude unrated skills. Unrated groups are labelled Not assessed and have no plotted score; a filled polygon appears only when all five groups have ratings. This presentation change does not alter the matching model. PDF/OCR libraries also load on demand. PDF/image processing requests confirmation before potentially large downloads; manual/pasted text remains available. The current OCR engine recognises English, while typed descriptions and catalogue search support selected English/Malay/Chinese keywords. The UI is mobile responsive; this is not a complete offline PWA.


## Reading the simplified Future Skills Radar

The page starts with up to three current-work learning suggestions alongside a visible five-group skill chart (stacked on mobile). The chart uses a self-assessed 1-5 scale, shows assessed points for partial profiles, and draws a filled shape only when all five groups are rated. Individual ratings remain available in a details section. The default **Changes at work** view uses selected tasks and self-ratings. With no selected tasks, it explicitly uses rated skills for suggestions and labels the task cards as catalogue examples, never inferring duties from an occupation title. Task cards describe whether AI-led or collaborative interaction patterns are more common in the chosen sample. **What does the data say?** reveals the original automation/augmentation percentages, month and source observation. These describe sampled Claude use, not AI capability, accuracy, job replacement or Malaysian adoption.

**Skills to build** presents up to three learning priorities with self-ratings or an explicit not-rated label. Choose current-role growth or a future career, then **Build my learning plan** opens that exact goal and clears any previously opened saved snapshot. The optional **What if AI takes on more routine work?** section compares **Today’s work** (existing moderate scenario) and **More AI-led work** (existing fast scenario). Both remain model assumptions with the original weights; shared-priority claims still require sufficient evidence. There is no new demand forecast or scoring formula.

**Career outlook** keeps the dated U.S. BLS references, broader occupation mappings and separate Malaysian context. AI month/scenario controls are not shown on this tab because they do not change BLS projections. The large **Sources, updates & how this works** block has been removed from the radar page. A compact source/month link stays with the content. The existing **Evidence & sources** dialog retains source metadata, validated release checks, actual update history and a nested latest-two-month matching comparison. The comparison explicitly checks recommendation stability rather than personal improvement. No new source data or live refresh was fabricated for the simpler presentation.

## Saved Pathways

**Save my plan** adds a pathway to **Saved pathways**, available from the sidebar or the learning page. Save multiple current-role and future-role routes; each card shows its target, resource steps, estimated hours, weekly time budget and saved progress. Saving the same goal/target/resource set updates its entry rather than adding duplicates. Progress/time changes are retained when explicitly saved again.

Opening a saved route restores its resource snapshot, schedule, goal and progress without replacing the current personal profile or occupation chick. The saved banner identifies historical steps; **Use latest recommendations** returns to live calculations using the current profile. Selecting a new career or learning goal also leaves snapshot mode. Removing a saved route requires confirmation and does not delete earned achievements.

The test library stays in sessionStorage only and survives reload in the same browser session. It never reads or writes private account APIs, including when the browser has a real account cookie. Unsaved progress is temporary; explicitly save changes to retain them with a pathway snapshot. Separate browser sessions do not share test collections. The backend's real account library still supports protected GET/POST/DELETE `/api/saved-pathways`, server-generated resource snapshots, ownership checks and one-time valid legacy-plan migration. These APIs remain separate from the current prototype frontend.

## My Achievements

Complete every resource in a non-empty pathway, then choose **Complete pathway & collect badge**. Write a short reflection (10-1000 characters) and confirm completion to receive a commemorative badge. Badges explicitly record **self-reported completion**; they do not certify skills, attendance or professional competence, and they never automatically increase skill ratings.

**My achievements** lists each completed pathway, date (Malaysia time), original estimated hours, covered skills, SDGs, reflection, resource links and evidence. Completion records are snapshots stored independently of the current plan. Changing targets or saving/deleting a current plan does not replace the collection. The same goal, target and set of resources can be collected once; changing weekly hours or evidence versions alone cannot duplicate a badge.

Guests can explore pathways and mark temporary progress. My Achievements and badge collection use the same prototype login prompt. Logging in from a completed pathway resumes reflection/attestation; it never awards a badge automatically. Closing the prompt preserves the pathway and progress. Test collections stay in sessionStorage and are never copied to real accounts. The retained backend APIs still enforce authorization, Origin, per-account storage and server-side completeness validation. There are no pre-earned badges.

For a presentation: complete the questionnaire -> view a suggested/current-role pathway -> Save my plan -> Log in to test -> View saved pathways -> My Profile -> open the saved pathway -> mark steps complete -> reflect/attest -> My Achievements. Explain that progress is demonstrated self-reporting and test saves last only for this browser session.

Optional connected browser check: build with `VITE_BACKEND_ENABLED=true`, run `python tests/serve_test_backend.py` in a separate terminal, then run `node tests/check_account_achievements_ui.mjs`. The harness serves on localhost:8011 and uses an independent temporary database. It creates a real synthetic backend account via API, then verifies that the browser's test workspace does not call private account APIs or write that account's plan/library/achievements despite its cookie. It also checks local reload, exit/re-entry and protected endpoints after server logout. Stop the harness when finished. This is local verification, not deployed account continuity.

## Stack and running

React, TypeScript, Vite, Recharts and Lucide React frontend; Python FastAPI, Pydantic, Uvicorn, SQLite and Google GenAI backend. Exact JavaScript versions are in package-lock.json; Python versions are in requirements.txt. Use Node 24 and Python 3.12.

```sh
bash scripts/run-replit.sh
```

The included .replit starts the same command. It builds with `VITE_BACKEND_ENABLED=true` and serves React and the JSON API from one FastAPI service on port 5000. Python dependencies install into Replit's project package directory using `uv`, avoiding the read-only system Python. For local frontend-only review use `npm ci` and `npm run dev`.

The static frontend runs the same browser matching formulas and packaged data. The current source provides test prototype access and browser-session collections without requiring Python. Replit runs the FastAPI service alongside the frontend when configured. A previously published hosted preview does not automatically receive local changes; this revision has not been deployed.

## Gemini

The optional adapter uses `gemini-2.5-flash` through Replit AI Integrations. Enable that integration and configure server-side `AI_INTEGRATIONS_GEMINI_API_KEY` and `AI_INTEGRATIONS_GEMINI_BASE_URL` as supplied by Replit. Keep values out of the repository. Verify the workspace's current generated integration example before a live demonstration.

The model suggests controlled skill IDs from a short work description; invalid IDs are rejected. Suggestions require user review. Without a model connection the UI labels its catalogue keyword fallback. Current result explanations are deterministic templates. A real Gemini response has not been tested in this environment.

## CV import

`pdfjs-dist` extracts text from the first three PDF pages. For scanned PDFs the first two pages are rendered for OCR; `tesseract.js` recognises English text from those page images or an uploaded image. Limit: 8 MB. OCR engine, worker and language assets may download on first use and require network access. Extracted CV text is mapped locally by catalogue keywords. It is not a semantic full-CV parser. A review screen prefills title, years and supported skill candidates. Confidence, interests and learning time require review/input. Pasted text and a synthetic sample remain available if extraction fails. Only an explicitly submitted short description goes to optional Gemini; files are not uploaded by this implementation.

## Accounts and storage

The current frontend uses explicit `guest | prototype` provenance. The displayed test identity does not authorize a backend session, and there is no frontend account signup/password form in this presentation flow. Real account services remain available separately in FastAPI:
- `POST /api/auth/signup`, `POST /api/auth/login`, `POST /api/auth/logout`
- `GET /api/auth/me`
- `PUT /api/plan`, `GET /api/plan`
- `GET /api/achievements`, `POST /api/achievements`
- `GET /api/saved-pathways`, `POST /api/saved-pathways`, `DELETE /api/saved-pathways/{id}`

The retained account API uses a unique salt and PBKDF2-HMAC-SHA256 (600,000 rounds). Session tokens are random, hashed in SQLite, and sent in HttpOnly SameSite=Strict cookies; Secure is set behind HTTPS. State-changing account operations validate Origin. Auth attempts are rate limited. SQL uses bound parameters; saved plans are validated and isolated by account. There is no email verification or password recovery. Guest and test prototype actions do not write server profiles, plans or collections. Account storage requires actual authorized API requests.

SQLite tables: public `catalogue` and `source_observations`; public `evidence_updates`; optional private `users`, `sessions`, `plans`, `achievements`, `saved_pathways`. Choose durable storage appropriate to the eventual Replit deployment before relying on account retention; this task does not provision that storage. Do not commit runtime SQLite files or secrets. Platform-level logs remain controlled by the host.

## Matching model

`score = 100 × (0.70 × baseline skill fit + 0.20 × interest fit + 0.10 × scenario-adjusted skill fit)`

All weights are prototype choices for validation. Baseline skill fit is weighted self-assessed confidence, not certified competence. Interests are catalogue overlaps; no preference uses a neutral 0.5.

For reviewed routine skills, direction d = −1; checking/oversight d = +1; otherwise d = 0. Each compatible task observation a (automation-pattern share divided by 100) supplies a small evidence factor `1 + 0.1 × d × a`. Linked-task factors are averaged. Moderate uses that evidence factor. Faster also multiplies reviewed routine skill importance by 0.8 and oversight by 1.2. Other skills remain unchanged. Role weights are normalised afterwards. These are assumptions about skill importance, not estimates of AI adoption. The entire adjustment is confined to the supplementary 10% score component.

Missing observations do not become zero. If any compared role has evidence for fewer than half its linked tasks, the trend component is omitted for all compared roles and the remaining weights renormalise to 70/90 and 20/90. Cross-scenario labels are withheld when evidence is insufficient. Shared priorities are the intersection of both scenarios' top three positive weighted skill gaps.

The Focus control changes card ordering (shorter plan / SDG 12 contribution), not matching scores.

## Evidence and update boundaries

- **Anthropic Economic Index**, release 26 June 2026. Packaged April/May observations retain task IDs and real values. These are global sampled Claude conversation patterns, not Malaysian adoption rates or job-loss probabilities. `data/aei_subset.json` preserves raw selected rows.
- **U.S. BLS Table 1.2**, released 27 August 2026: 2025–2035 projections, imported into `data/market.json`. Geography, horizon and broader-parent mappings are labelled. A parent-group rate is not a BI- or sustainability-specific rate. Context only, excluded from matching scores.
- **O*NET occupation pages** inform curated occupational references. This is not a full O*NET database import or official task/skill crosswalk.
- **TalentCorp MyCOL**, **DOSM** and **UN SDGs** are linked context. No live DOSM salary feed or numeric MyCOL growth estimate is claimed.

`POST /api/evidence/refresh` discovers releases from the official Anthropic Economic Index repository, pins downloads to an immutable commit, and validates compatible CSV schemas, monthly periods, finite percentages, duplicate metrics, collaboration totals and task/role coverage. Compatible releases update the active SQLite catalogue atomically with an audit record; unsupported schemas require review, and failures retain the last valid evidence. Historical periods keep their own source/release links. Discovery does not guarantee that future formats or metric definitions are compatible.

The backend checks every six hours while the process is running; configure `BRIDGENEXT_SIGNAL_INTERVAL_SECONDS` (minimum 300 seconds). The first automatic check is after that interval; manual checks are available immediately, with a five-minute throttle. This is an in-process scheduler, not a platform wake-up service: stopped or sleeping Replit instances cannot run checks. `GET /api/evidence/status` exposes the latest history and active metadata. The radar shows check status, discovered releases and actual observation changes. New periods are accepted by matching and account-plan validation. BLS remains a dated reference, not a live job-market feed.

Live read-only validation on 23 October 2026 discovered six releases, selected 2026-06-26 at commit `4e5f69fab13a9c3f7d0dcc31a6f893a9818738f6`, downloaded and validated its observations, and found zero changed fields. No new release, rank change or persistent deployment update was claimed. Future-release and failure cases are tested with explicitly synthetic CSV fixtures, never mixed into application evidence. `scripts/fetch_evidence.py` is the older pinned offline import utility; the running backend uses `backend/signals.py`.

Evidence switching and scenario switching recalculate actual scores and priorities. No rank changes are manufactured.

## Learning, SDGs and estimates

Resources are catalogue-selected from Microsoft Learn/Support, IFRS, COSO public materials and team-authored synthetic practice. Each has a provider/source link or labelled original practice. Free means selected introductory content; optional software, certificates and publications may cost extra. Durations include estimated practice, not provider promises. A small team-defined prerequisite map inserts spreadsheet foundations before BI/sustainability when needed and verification before controls when confidence is low. Steps then follow in order; weekly schedules recompute from total study hours and the weekly budget.

Each role and skill has an SDG target plus a specific intended contribution. These mappings do not constitute measured SDG impact. All skill recommendations open occupational evidence and relevant SDG references.

## Validation

```sh
npm run build
python tests/check_backend.py
python tests/check_signals.py
python tests/check_achievements.py
python tests/check_saved_pathways.py
node scripts/check-parity.mjs
```

Backend validation includes 12 contract/account checks, 7 signal checks, 4 achievement checks and 5 saved-pathway checks (28 total). TypeScript/Python parity covers 9 future-role, 11 current-role and 20 completion-resource cases. Browser checks use real questionnaire inputs rather than prepared identities: test login and page destinations; automatic pending-save continuation; profile edit/cancel and chick consistency; CV draft preservation; saved snapshots/progress and collection reload; badge reflection, attestation and deduplication; guest gates and exit/re-entry; no private browser account API calls; English/Malay/Chinese and mobile layouts. The dedicated radar browser suite also checks real/missing observations, hidden details, keyboard tabs, both planning goals, selected-task scope and visible partial/full five-group charts, assessed-only averages and the centralized evidence dialog. The connected-cookie check above verifies that a real account does not receive prototype saves.

Optional local browser checks (start `npm run dev` first):

```powershell
npm.cmd install --prefix .test-tools --no-package-lock --no-save playwright
$env:BRIDGENEXT_CHROME = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
node tests/check_ui.mjs
node tests/check_inclusive.mjs
node tests/check_achievements_ui.mjs
node tests/check_saved_pathways_ui.mjs
node tests/check_prototype_ui.mjs
node tests/check_radar_ui.mjs
```

Set `BRIDGENEXT_URL` to override the default `http://127.0.0.1:5173`. On other systems set `BRIDGENEXT_CHROME` to the browser executable, or install Playwright Chromium. Test screenshots and tools stay in ignored `.test-tools/`. Backend tests also need `httpx` in the Python test environment.

Local validation on 23 October 2026 used Node 22.18 and an isolated Python 3.14 environment (3.12 was unavailable); Replit remains targeted at Node 24/Python 3.12. The latest split frontend build has no large-chunk advisory; Starlette's httpx deprecation notice remains. No Replit deployment or live Gemini test was performed.

## Declaration additions for this revision

Update the team's Technical Tools Declaration to reflect actual use of `pdfjs-dist`, `tesseract.js` (including its worker/OCR assets), Lucide React, Google Fonts DM Sans/Manrope, OpenAI image generation from the supplied mascot reference, BLS Table 1.2, and prototype accounts. Original declaration statements about no stored profiles must distinguish guest processing from explicitly saved account plans. No RunPod/GPU service is used. The prototype does not verify competition attendance, submission status or Replit deployment.

## Mascot revision

The current six-outfit character sheet is a newly generated design from a text brief, not an image edit of the supplied example. The brief changes the silhouette, face proportions, oval teal eyes, feather crest, light face patch, linework and wing poses while retaining the broad concept of a friendly yellow chick. Asset: public/assets/chick-careers-v2.png. Generated using the built-in OpenAI image tool.
