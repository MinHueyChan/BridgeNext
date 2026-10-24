## BridgeNext

> An explainable career-transition planner for Malaysian finance and operations workers whose jobs are being reshaped by AI: it maps their skills to nearby roles using dated AI-usage evidence, then builds a time-budgeted, SDG-linked learning plan.

<!-- TODO before submission: replace every "TODO" below, then delete these comments. -->

---

## Team Information

| Field                 | Details                                                        |
| --------------------- | -------------------------------------------------------------- |
| **Team Name**         | EyeScream                                                      |
| **Team Domain**       | Domain 1: Aiversecity Future-Ready Workforce                   |
| **SDG Track (1–17)**  | SDG 4: Quality Education (target 4.4); also SDG 8 (target 8.2) |
| **Team Leader**       | Yap Li Shan                                                    |
| **University**        | Asia Pacific University of Technology & Innovation (APU)       |
| **Number of Members** | 2                                                              |

## Links

| Resource          | Link                                                                                                     |
| ----------------- | -------------------------------------------------------------------------------------------------------- |
| GitHub Repository | https://github.com/MinHueyChan/BridgeNext                                                                |
| Live Demo         | https://bridge-next.replit.app/ (first load can take a few seconds while the Replit deployment wakes up) |
| RunPod Endpoint   | Not used (no GPU workload). See [How We Use RunPod](#how-we-use-runpod-required)                         |
| Slide Deck        | TODO                                                                                                     |
| Demo Video        | TODO (YouTube)                                                                                           |

---

## Overview

### Problem

AI is changing office work in Malaysia faster than workers are being trained for it. TalentCorp's impact study found that 620,000 jobs, or 18% of employees in 10 key sectors, are expected to face significant changes within three to five years ([Malay Mail, 18 Nov 2024](https://www.malaymail.com/news/malaysia/2024/11/18/hr-minister-proposes-upskilling-as-study-shows-620000-jobs-in-10-sectors-set-for-impact-soon-from-ai-digitalisation/157256)). According to the Hays Asia Salary Guide 2025, 56% of professionals in Malaysia already use AI tools, but only 26% have received any formal training ([People Matters, Jul 2025](https://sea.peoplemattersglobal.com/article/strategic-hr/ai-in-malaysian-workplaces-a-strategic-outlook-46436)). Finance and operations staff, such as accountants, administrative assistants and operations coordinators, can see that their tasks are changing. They rarely get a clear, evidence-based answer to the question "what should I learn next, and where can it take me?"

### Solution

BridgeNext starts from what a worker already does: their tools, tasks and self-rated skills. It shows:

- how people actually use AI for those tasks (AI-led vs working together), from the Anthropic Economic Index;
- which nearby roles fit them, with a match score they can open up and question;
- a free, time-budgeted learning pathway with SDG links.

Matching is deterministic and transparent. AI is used for one specific job: **Gemini 2.5 Flash** (via Replit AI Integrations) turns a free-text description of someone's work into catalogue skill suggestions. The user always reviews and confirms the suggestions, and invalid model output is rejected.

### Key Features (mapped to the Domain 1 requirements)

1. **Skill profile input:**

- A guided four-step questionnaire (occupation, tools/tasks/skills, 1–5 confidence, interests).
- CV import: PDF text extraction, or OCR for scans and images. Processing happens in the browser.
- A free-text description with Gemini skill suggestions.

2. **Updatable AI-trend signal layer:** task-level AI-usage observations from the Anthropic Economic Index (release 26 Jun 2026; April and May 2026 periods). Each observation is labelled with its source, month and caveat.

- The backend discovers new releases and validates the schema, periods and coverage before activating them.
- If a check fails, the last validated evidence is kept, and every check is recorded in an update history.
- Career outlook adds dated U.S. BLS 2025–2035 projections as context.

3. **Explainable match score and skill gaps:**

- `score = 70% skill fit + 20% interest fit + 10% scenario-adjusted skill fit`, with the breakdown shown for every direction.
- Strengths, learning priorities, "not assessed yet" labels and O\*NET occupation references.

4. **Learning pathway with time estimates:**

- Free resources (Microsoft Learn and Support, IFRS Foundation, COSO, practice activities) ordered by prerequisites.
- Hours and weeks recalculate from the user's weekly study time.
- Progress tracking and Markdown export.

5. **SDG mapping:** every career direction and every skill carries an SDG target and a short explanation.
6. **Two future scenarios:** "Today's work" (moderate) and "More AI-led work" (faster change) recalculate scores and learning priorities. Both are labelled as model assumptions, not predictions.

It also includes English / Bahasa Malaysia / 简体中文 UI, a mobile-responsive layout, a career comparison view and saved pathways.

### Tech Stack

| Layer         | Technology                                                                                                                         |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| Frontend      | React 19, TypeScript, Vite, Recharts, Lucide React, pdfjs-dist, tesseract.js                                                       |
| Backend       | Python 3.12, FastAPI, Pydantic, Uvicorn                                                                                            |
| Database      | SQLite (catalogue, evidence observations, update history)                                                                          |
| AI            | Gemini 2.5 Flash via Replit AI Integrations (`google-genai` SDK)                                                                   |
| Data          | Anthropic Economic Index, O\*NET OnLine, U.S. BLS Table 1.2, UN SDG targets; TalentCorp MyCOL and DOSM as linked Malaysian context |
| Hosting / Dev | Replit Deployments (Autoscale); Node 24                                                                                            |

---

## Judge Quick Tour (about 2 minutes)

1. Open the **Live Demo**. Choose **Start with my CV**, then **Use synthetic sample**, then **Review imported profile**.
2. Confirm the steps: rate each skill 1–5, pick interests, then **Confirm profile & see my top match**.
3. On **Your top direction**, choose **Explore more**:

- Open **Why this direction?** to see the score breakdown.
- Switch **Scenario** (Moderate / Faster change) and **Evidence period** (April / May 2026).

4. Open **Future skills radar**:

- In **Changes at work**, open **What does the data say?** for the AI-led vs working-together shares.
- In **Skills to build**, choose **Prepare for a new role** and open **What if AI takes on more routine work?**

5. Open **Learning pathway**:

- Change **My weekly time** and watch the hours and weeks recalculate.
- Check the SDG panel, then **Export my plan**.

6. Open **Evidence & sources**, then **Check for new source data**. It shows the active release and the last validated check.

---

## Project Structure

```
.
├── backend/                 # FastAPI app
│   ├── main.py              # API routes + serves the built React app
│   ├── engine.py            # Deterministic matching (mirrors src/engine.ts)
│   ├── signals.py           # Evidence release discovery + validation
│   ├── saved_pathways.py    # Server-side pathway snapshots (account API)
│   └── achievements.py      # Completion records (account API)
├── src/                     # React + TypeScript frontend
│   ├── main.tsx             # App, questionnaire, results, pathway
│   ├── engine.ts            # Browser matching engine
│   ├── FutureSkillsRadar.tsx
│   ├── EvidenceDetails.tsx
│   ├── cv.ts                # PDF text extraction + OCR
│   └── i18n.tsx, translations.ts   # EN / BM / ZH
├── data/
│   ├── catalogue.json       # Roles, skills, tasks, resources, SDG mappings
│   ├── aei_subset.json      # Raw Anthropic Economic Index rows used
│   └── market.json          # BLS 2025–2035 projection references
├── public/                  # Mascot, favicon, packaged catalogue
├── scripts/                 # run-replit.sh, data build/fetch, parity check
├── tests/                   # Python backend tests + browser checks
├── submission/              # TODO: add the PDFs below before submitting
│   ├── SDC2026_EyeScream_Preliminary.pdf
│   ├── SDC2026_EyeScream_TechDeclaration.pdf
│   └── SDC2026_EyeScream_Replit_POU.pdf
├── .env.example
├── .replit / replit.md      # Replit run + deployment configuration
├── requirements.txt / package.json
├── THIRD_PARTY_NOTICES.md
└── LICENSE                  # Apache-2.0
```

### Architecture

```
Browser (React + TypeScript · EN / BM / ZH)
  │  questionnaire · CV text/OCR (in browser) · results · learning pathway
  ▼
FastAPI on Replit Deployments ──► SQLite (catalogue, evidence, update history)
  │      │
  │      └──► Gemini 2.5 Flash via Replit AI Integrations
  │             (free text → catalogue skill IDs → user confirms)
  └──► Anthropic Economic Index on Hugging Face
         (release discovery → schema/period/coverage validation → activate or keep last valid)
```

### API

| Method | Path                    | Purpose                                                                |
| ------ | ----------------------- | ---------------------------------------------------------------------- |
| GET    | `/api/health`           | Service status and whether the model is configured                     |
| GET    | `/api/catalogue`        | Roles, skills, tasks, resources, active evidence                       |
| POST   | `/api/matches`          | Deterministic match scores for a confirmed profile, month and scenario |
| POST   | `/api/profile/extract`  | Gemini skill suggestions from a short description (consent required)   |
| POST   | `/api/evidence/refresh` | Check for a newer compatible evidence release (throttled)              |
| GET    | `/api/evidence/status`  | Active evidence and update history                                     |

The optional account endpoints (`/api/auth/*`, `/api/plan`, `/api/saved-pathways`, `/api/achievements`) are implemented and tested, but the presentation build stores test-workspace data in the browser session only.

---

## How to Run

### Option 1: Run on Replit (recommended)

1. Import this repository into Replit (**Create Repl → Import from GitHub**).
2. Optional: connect **Replit AI Integrations → Gemini**. This provides `AI_INTEGRATIONS_GEMINI_API_KEY` and `AI_INTEGRATIONS_GEMINI_BASE_URL` as server-side secrets. Without them, the app labels and uses its catalogue keyword fallback.
3. Click **Run**. `scripts/run-replit.sh` then:

- installs Node and Python dependencies;
- builds the frontend with `VITE_BACKEND_ENABLED=true`;
- starts FastAPI on port 5000, which serves both the app and the API.

### Option 2: Run locally (Node 24, Python 3.12)

```bash
git clone https://github.com/MinHueyChan/BridgeNext.git
cd BridgeNext
npm ci
VITE_BACKEND_ENABLED=true npm run build
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m backend.main                             # http://localhost:5000
```

For frontend-only development, use `npm run dev`. The browser engine runs the same matching formulas with the packaged data.

### Run Tests

```bash
pip install httpx
python tests/check_backend.py
python tests/check_signals.py
python tests/check_achievements.py
python tests/check_saved_pathways.py
node scripts/check-parity.mjs      # browser (TS) and server (Python) engines give identical results
```

---

## How We Use Replit _(Required)_

<!-- TODO: confirm the deployment type matches your Replit settings (.replit in this repo says autoscale). -->

- **Hosting:** the app is deployed with Replit Deployments (Autoscale) at the Live Demo link. A single FastAPI service serves the React build and the JSON API.
- **Run and build:** `.replit` runs `scripts/run-replit.sh` for preview and defines the deployment build (npm, uv and Vite) and run command.
- **AI:** Gemini is called through Replit AI Integrations. Credentials stay in server-side secrets and never reach the frontend or this repository.
- **Development:** TODO. Describe how the team used the Repl (e.g. editing, preview, Replit Agent).

📄 Proof of use: [`submission/SDC2026_EyeScream_Replit_POU.pdf`](submission/SDC2026_EyeScream_Replit_POU.pdf)

## How We Use RunPod _(Required)_

Not used. BridgeNext has no GPU workload:

- matching, scenarios and pathways are deterministic calculations on the CPU;
- CV OCR runs in the user's browser with tesseract.js;
- the only LLM call goes to Gemini through Replit AI Integrations.

<!-- TODO: confirm with the organisers on Discord whether Domain 1 teams without a GPU workload still need a RunPod proof of use. -->

---

## Risks, Limits and Fallbacks

| Risk                                         | What BridgeNext does                                                                                                                                                                       |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Gemini unavailable or returns invalid output | Only catalogue skill IDs are accepted, and invalid output is discarded. The app falls back to labelled keyword matching, and the user confirms every skill.                                |
| A new evidence release changes format        | Discovery validates schema, periods, percentages and task coverage. Incompatible releases are marked "review required" and the last validated evidence stays active.                       |
| Replit instance sleeps                       | The six-hourly check only runs while the instance is awake. **Check for new source data** runs a check on demand.                                                                          |
| Evidence is not Malaysian adoption data      | AI observations are global, sampled Claude conversations. They are labelled as such and only adjust the 10% scenario component. BLS figures are U.S. context and are excluded from scores. |
| Self-assessment bias                         | Ratings are labelled self-assessed. Unrated skills are shown as "not assessed", never as a lack of ability.                                                                                |

Scores support a human decision. They are not hiring probabilities or job-loss predictions.

## Data Sources and Attribution

- **Anthropic Economic Index** (release 2026-06-26), Hugging Face. Task-level automation and augmentation shares.
- **O\*NET OnLine** occupation pages, U.S. Department of Labor / ETA, used under CC BY 4.0. Task groups, skill weights and mappings are modified by the team and are not endorsed by USDOL/ETA.
- **U.S. Bureau of Labor Statistics**, Table 1.2, 2025–2035 projections (released 27 Aug 2026). Context only.
- **TalentCorp MyCOL 2024/2025** and **Department of Statistics Malaysia**. Linked as Malaysian context.
- **UN Sustainable Development Goals** targets.

Full licences and notices are in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

### AI tools declared

- Runtime: Gemini 2.5 Flash via Replit AI Integrations.
- Mascot: generated with OpenAI image generation from a text brief.
- TODO: list every AI assistant used for code, writing or design (for example, OpenAI Codex/ChatGPT, Replit Agent, Claude), matching the Technical Tools Declaration.

---

## Challenges & Learnings

<!-- TODO: rewrite in your own words. -->

- **Honest evidence:** AI-usage data describes how people use AI, not which jobs disappear. We label every figure with its source, month and caveat, and keep it out of the core skill score.
- **Safe updates:** automatic refresh is only useful if bad data cannot slip in. We validate each release and keep the last good version.
- **One engine, two runtimes:** the browser and server compute identical results, checked by parity tests.
- **Deployment:** getting Python dependencies to install on Replit Deployments took several attempts. TODO: describe what fixed it.

## Future Improvements

- [ ] Use Malaysian labour data in matching (DOSM, MyCOL critical occupations).
- [ ] Add HRD Corp e-LATiH courses and HRD Corp Claimable Course guidance to pathways.
- [ ] Expand beyond finance and operations directions.
- [ ] Add durable accounts and storage for saved plans.
- [ ] Track AI-usage trends across more Economic Index releases.
- [ ] Get a native-speaker review of Bahasa Malaysia.
- [ ] Add an HR/L&D and career-centre view.

## Team

| Name        | Role                                            | GitHub                                         |
| ----------- | ----------------------------------------------- | ---------------------------------------------- |
| Yap Li Shan | Team Leader · pitch deck, technical declaration | TODO                                           |
| TODO        | PRD · prototype (full stack)                    | [@MinHueyChan](https://github.com/MinHueyChan) |

---

## Submission Checklist

- [ ] Team name, domain and SDG track filled in
- [ ] Slide deck link added
- [ ] Demo video link added
- [ ] Replit used, with proof of use in `submission/`
- [ ] RunPod requirement confirmed with organisers (not used: no GPU workload)
- [ ] Preliminary submission completed (`SDC2026_EyeScream_Preliminary.pdf`)
- [ ] Technology declaration completed (`SDC2026_EyeScream_TechDeclaration.pdf`)
- [ ] "How to Run" steps verified
- [ ] No API keys or secrets committed to the repository

## License

This project is licensed under the [Apache License 2.0](LICENSE). Third-party data, fonts and linked content keep their own licences (see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)).
