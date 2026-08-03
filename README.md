# Bank Marketing — Streamlit App

Web front-end for the term-deposit subscription model. Lets a non-technical user enter a client profile, get a subscription probability back, and see why the model produced it.

**Live:** https://bankmarketingstreamlit-production.up.railway.app

Part of a three-repo project:

| Component | Repo |
|---|---|
| Analysis & modelling | [`bankmarketing_jupyter`](https://github.com/Itaru2018/bankmarketing_jupyter) |
| Prediction API | [`bank_marketing_fastapi`](https://github.com/Itaru2018/bank_marketing_fastapi) |
| Web app (this repo) | [`bank_marketing_streamlit`](https://github.com/Itaru2018/bank_marketing_streamlit) |

## What it does

The app is a thin client. It collects input, calls the FastAPI service, and presents the result — it holds no model and no business logic of its own. That separation is deliberate: the model can be retrained and redeployed without touching the UI.

**Two input modes:**

- **Quick demo (4 features)** — enter only the handful of features that dominate the prediction. The remaining fields are filled from a sensible default profile, so a visitor can get a result in a few seconds.
- **Full input** — all model features exposed, for exploring how each one moves the prediction.

Both modes ship with pre-populated demo payloads so the app is immediately usable without domain knowledge.

**Output:** subscription probability, the model's decision at the tuned threshold (not the naïve 0.5 — see the API repo), and an explanation of what drove that particular prediction.

## Pages
bank_streamlit_app.py   Entry point / router
demo_4_features.py      Quick demo: 4 key features, rest defaulted
full_input_demo.py      Full feature input form
about_project.py        The modelling problem, data, and approach
about_app.py            How the app and API fit together
contact.py              Contact

## Running locally

The app needs a reachable API. Either point it at the deployed one or run [`bank_marketing_fastapi`](https://github.com/Itaru2018/bank_marketing_fastapi) locally first.

```bash
git clone https://github.com/Itaru2018/bank_marketing_streamlit.git
cd bank_marketing_streamlit

python3.11 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -r requirements.txt
streamlit run bank_streamlit_app.py
```

## Other files
The input options are driven by JSON config rather than hard-coded in the forms, so the UI stays in sync with the model's expected schema by editing one file.

## Stack

Python · Streamlit · requests · Railway

## Author

**Itaru Yasumura** — Basel, Switzerland
[GitHub](https://github.com/Itaru2018) · [LinkedIn](https://www.linkedin.com/in/itaru-yasumura-27b05a1b2/)
