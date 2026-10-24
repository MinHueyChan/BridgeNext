## BridgeNext

An explainable career-planning prototype for working adults adapting to AI-related task changes, initially focused on Malaysian financial operations and administrative support: it maps their skills to nearby roles using dated AI-usage evidence, then builds a time-budgeted, SDG-linked learning plan.


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
| Live Demo         | https://Bridge-Next.replit.app |
| RunPod Endpoint   | Not used (no GPU workload)                       |
| Slide Deck        | https://canva.link/ahcnzn791me9p6m                                                                                                     |
| Demo Video        | https://www.youtube.com/watch?v=p5X6IO9a-JY&feature=youtu.be                                                                                          |

---

## Overview

### Problem

AI is changing office work in Malaysia faster than workers are being trained for it. TalentCorp's impact study found that 620,000 jobs, or 18% of employees in 10 key sectors, are expected to face significant changes within three to five years ([Malay Mail, 18 Nov 2024](https://www.malaymail.com/news/malaysia/2024/11/18/hr-minister-proposes-upskilling-as-study-shows-620000-jobs-in-10-sectors-set-for-impact-soon-from-ai-digitalisation/157256)). According to the Hays Asia Salary Guide 2025, 56% of professionals in Malaysia already use AI tools, but only 26% have received any formal training ([People Matters, Jul 2025](https://sea.peoplemattersglobal.com/article/strategic-hr/ai-in-malaysian-workplaces-a-strategic-outlook-46436)). Finance and operations staff, such as accountants, administrative assistants and operations coordinators, can see that their tasks are changing. They rarely get a clear, evidence-based answer to the question "what should I learn next, and where can it take me?"

### Solution

BridgeNext starts from what a worker already does: their tools, tasks and self-rated skills. It shows:
- how people actually use AI for those tasks (AI-led vs working together), from the Anthropic Economic Index;
- which nearby roles fit them, with a match score they can open up and question;
- a free, time-budgeted learning pathway with SDG links.
  
Matching is deterministic and transparent. The preliminary demonstration uses catalogue keyword matching and standard explanations; live Gemini activation will be fully activated at Phase 2. Optional Gemini 2.5 Flash integration code is already presented for catalogue skill suggestions and explanations of computed results. It cannot determine scores or select new resources. Users review profile suggestions before adding them.

### Key Features (mapped to the Domain 1 requirements)

1. Skill profile input:
   - A guided four-step questionnaire (occupation, tools/tasks/skills, 1–5 confidence, interests and weekly study time).
   - CV import: PDF text extraction, or OCR for scans and images. Processing happens in the browser.
   - A free-text description with catalogue keyword suggestions. Optional Gemini assistance is prepared for Phase 2.
     
2. Updatable AI-trend signal layer: task-level AI-usage observations from the Anthropic Economic Index (release 26 Jun 2026; April and May 2026 periods). Each observation is labelled with its source, month and caveat.
   - The backend discovers new releases and validates the schema, periods and coverage before activating them.
   - If a check fails, the last validated evidence is kept, and every check is recorded in an update history.
   - Career outlook adds dated U.S. BLS 2025–2035 projections as context.
     
3. Explainable match score and skill gaps:
   - score = 70% skill fit + 20% interest fit + 10% scenario-adjusted skill fit, with the breakdown shown for every direction.
   - If any compared role has compatible evidence for fewer than half of its linked tasks, the 10% component is omitted for all roles; remaining weights become approximately 77.8% skills and 22.2% interests. Missing evidence is not zero exposure.
   - Strengths, learning priorities, "not assessed yet" labels and O*NET occupation references.
     
4. Learning pathway with time estimates:
   - Free resources (Microsoft Learn and Support, IFRS Foundation, COSO, practice activities) ordered by prerequisites.
   - The estimated study hours belong to the selected activities; changing weekly study time recalculates their week ranges and total duration in weeks.
   - Progress tracking and Markdown export.
    
5. SDG mapping: every career direction and every skill carries an SDG target and a short explanation.
   
6. Two future scenarios: "Today's work" (moderate) and "More AI-led work" (faster change) recalculate scores and learning priorities. Both are labelled as model assumptions, not predictions.
   
It also includes English / Bahasa Malaysia / 简体中文 UI, a mobile-responsive layout, a career comparison view, current-role development and saved pathways. Profile drafts, saved plans and achievements in the presentation interface use browser session storage; this is not production account storage.

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
├── backend/
│   ├── main.py              # FastAPI routes, SQLite setup and built frontend hosting
│   ├── engine.py            # Deterministic matching and current-role calculations
│   ├── signals.py           # Evidence discovery, validation and refresh
│   ├── saved_pathways.py    # Snapshots for separate account APIs
│   ├── achievements.py      # Server-side completion validation
│   ├── gemini.py            # Optional model adapter; live use deferred to Phase 2
│   └── explanations.py      # Validated skill extraction and result explanations
├── src/
│   ├── main.tsx             # Main interface and guided questionnaire
│   ├── engine.ts            # Matching, priorities, pathways and keyword suggestions
│   ├── FutureSkillsRadar.tsx
│   ├── EvidenceDetails.tsx
│   ├── SkillChart.tsx
│   ├── DescriptionMatches.tsx # Keyword suggestions and optional Gemini control
│   ├── AIExplanation.tsx    # Optional explanation interface
│   ├── ai.ts               # AI request and failure handling
│   ├── cv.ts               # Browser PDF extraction and English OCR
│   ├── saved-pathways.ts    # Browser session pathway snapshots
│   ├── achievements.ts     # Browser completion records
│   ├── i18n.tsx
│   ├── translations.ts     # English, Malay and Chinese interface text
│   ├── style.css
│   └── interaction.css
├── data/
│   ├── catalogue.json      # Five roles, 18 skills, six tasks and eight resources
│   ├── aei_subset.json     # Selected source rows and provenance
│   └── market.json         # Dated BLS context; excluded from match scores
├── public/
│   ├── assets/             # Chick character sheet and design note
│   ├── previews/           # Project preview images
│   └── favicon.svg
├── scripts/
│   ├── run-replit.sh
│   ├── post-merge.sh
│   ├── build_catalogue.py
│   ├── fetch_evidence.py
│   ├── package-replit.py
│   ├── check-parity.mjs
│   └── check-gemini.py      # Optional live-model diagnostic, not needed for prelim
├── tests/                  # Python checks and browser verification scripts
├── submission/              # TODO: add the PDFs below before submitting
│   ├── SDC2026_EyeScream_Preliminary.pdf
│   ├── SDC2026_EyeScream_TechDeclaration.pdf
│   └── SDC2026_EyeScream_Replit_POU.pdf
├── .env.example
├── .gitignore
├── .replit                 # Replit runtime and deployment settings
├── .replitignore
├── replit.md               # Replit project notes
├── index.html
├── package.json
├── package-lock.json
├── requirements.txt
├── tsconfig.json
├── vite.config.ts
├── README.md
├── THIRD_PARTY_NOTICES.md
└── LICENSE                 # Apache-2.0
```

### Architecture

```
User
 │
 ▼
Browser — React + TypeScript
 │  Interface: English / Bahasa Malaysia / 简体中文
 │  Questionnaire + profile review
 │  Local CV text extraction / English OCR
 │  Catalogue keyword matching
 │  Browser matching + learning pathways
 │  Session storage: profile, saved plans, achievements
 │
 ▼
Replit — Python FastAPI
 │  Hosts the built React application
 │  Validates requests + calculates career matches
 │
 ├──► SQLite
 │      Catalogue + dated observations + update history
 │      Separate account APIs also support saved user data
 │
 ├──► Hugging Face — Anthropic Economic Index
 │      Discover → download → validate
 │      Update evidence or retain last valid version
 │
 ├──► Gemini via Replit AI Integrations [Phase 2]
 │      Optional skill suggestions + result explanations
 │      Not enabled for the preliminary demonstration
 │
 └──► API responses returned to browser
        Career scores + skill gaps + evidence
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

### Option 1: Run on Replit (recommended)

1. Import this repository into Replit (**Create Repl → Import from GitHub**).
2. For the preliminary demo, leave Gemini credentials unset. `model_configured: false` is expected. The optional AI controls can return an unavailable message or standard fallback; they are not evidence of a live model call.
3. Click **Run**. `scripts/run-replit.sh` then:

- installs JavaScript and Python project dependencies;
- builds the frontend with `VITE_BACKEND_ENABLED=true`;
- starts FastAPI on port 5000, which serves both the app and the API.

### Option 2: Run locally (Node 24, Python 3.12)

These commands use **Windows CMD**. If the repository is already on your computer, open that folder and skip cloning.

```bash
git clone https://github.com/MinHueyChan/BridgeNext.git
cd BridgeNext
npm ci
py -3.12 -m venv .venv
set PIP_TARGET=
set PIP_USER=false
.venv\Scripts\python.exe -m pip install -r requirements.txt
set VITE_BACKEND_ENABLED=true
npm run build
set PORT=5000
.venv\Scripts\python.exe -m backend.main
```
Open http://localhost:5000. Keep the terminal running. The backend-enabled frontend build must be rebuilt after frontend changes.

For frontend-only development:

```bat
set VITE_BACKEND_ENABLED=false
npm run dev
```

Open the URL printed by Vite. This preview uses bundled data; server refresh and account APIs are unavailable. For Vite development with FastAPI, run the backend in a separate terminal and set `VITE_BACKEND_ENABLED=true` before starting Vite. The Vite configuration proxies `/api` to port 5000.

### Run Tests

```bat
npm run check
npm run build
.venv\Scripts\python.exe -m pip install httpx
.venv\Scripts\python.exe -m unittest discover -s tests -p "check_*.py"
set BRIDGENEXT_PYTHON=%CD%\.venv\Scripts\python.exe
node scripts/check-parity.mjs
```

The Python suite includes mocked Gemini checks; it does not need a live model. Browser scripts in `tests/` require their browser-test setup. `scripts/check-gemini.py` is a separate live integration diagnostic for Phase 2, not a prerequisite for the preliminary demo.

---

## How We Use Replit _(Required)_

- **Hosting:** the app is deployed with Replit Deployments (Autoscale) at the Live Demo link. A single FastAPI service serves the React build and the JSON API.
- **Run and build:** `.replit` runs `scripts/run-replit.sh` for preview and defines the deployment build (npm, uv and Vite) and run command.
- **Development:** The team uses VS Code and GitHub for source changes, and Replit for application configuration, preview and deployment. Replit Agent assisted with environment and deployment configuration.

📄 Proof of use: [`submission/SDC2026_EyeScream_Replit_POU.pdf`](submission/SDC2026_EyeScream_Replit_POU.pdf)

## How We Use RunPod _(Required)_

Not used. BridgeNext has no GPU workload:

- matching, scenarios and pathways are deterministic calculations on the CPU;
- CV OCR runs in the user's browser with tesseract.js;
- the only LLM call goes to Gemini through Replit AI Integrations.

---

## Risks, Limits and Fallbacks

| Risk | What BridgeNext does |
| --- | --- |
| Gemini unavailable or returns invalid output | Only catalogue skill IDs are accepted, and invalid output is discarded. The app falls back to labelled keyword matching, and the user confirms every skill. |
| A new evidence release changes format | Discovery validates schema, periods, percentages and task coverage. Incompatible releases are marked "review required" and the last validated evidence stays active. |
| Replit instance sleeps | The six-hourly check only runs while the instance is awake. **Check for new source data** runs a check on demand. |
| Evidence is not Malaysian adoption data | AI observations are global, sampled Claude conversations. They are labelled as such and only adjust the 10% scenario component. BLS figures are U.S. context and are excluded from scores. |
| Self-assessment bias | Ratings are labelled self-assessed. Unrated skills are shown as "not assessed", never as a lack of ability. |

Scores support a human decision. They are not hiring probabilities or job-loss predictions.

## Data Sources and Attribution

- **Anthropic Economic Index** (release 2026-06-26), Hugging Face. Task-level automation and augmentation shares.
- **O\*NET OnLine** occupation pages, U.S. Department of Labor / ETA, used under CC BY 4.0. Task groups, skill weights and mappings are modified by the team and are not endorsed by USDOL/ETA.
- **U.S. Bureau of Labor Statistics**, Table 1.2, 2025–2035 projections (released 27 Aug 2026). Context only.
- **TalentCorp MyCOL 2024/2025** and **Department of Statistics Malaysia**. Linked as Malaysian context.
- **UN Sustainable Development Goals** targets.

Full licences and notices are in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

### AI tools declared

- Preliminary runtime: pre-trained Tesseract English OCR; no live Gemini call.
- Planned Phase 2 runtime: Gemini 2.5 Flash via Replit AI Integrations.
- Mascot: generated with OpenAI image generation from a text brief.
- Development assistance: ChatGPT / OpenAI Codex for code and testing; Claude for document and project review; Replit Agent for environment and deployment configuration, as recorded in the Technical Tools Declaration.

---

## Challenges & Learnings

- **Honest evidence:** AI-usage data describes how people use AI, not which jobs disappear. We label every figure with its source, month and caveat, and keep it out of the core skill score.
- **Safe updates:** automatic refresh is only useful if bad data cannot slip in. We validate each release and keep the last good version.
- **One engine, two runtimes:** the browser and server compute identical results, checked by parity tests.
- **Deployment:** the checked-in Replit workflow builds the React frontend and installs Python dependencies into the project package directory before starting one FastAPI service.

## Future Improvements

- [ ] Activate and validate Gemini-assisted skill interpretation and result explanations in Phase 2.
  
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
| Yap Li Shan | Team Leader · pitch deck, technical declaration | [@lishan0311](https://github.com/lishan0311)  |
| Chan Min Huey       | PRD · prototype (full stack)                    | [@MinHueyChan](https://github.com/MinHueyChan) |

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
