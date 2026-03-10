# Grab Decision Studio

A redesigned Streamlit dashboard for Grab with:
- Hidden filters in a compact "Refine view" drawer
- Problem-led navigation instead of generic analytics tabs
- Stakeholder-friendly sections: What is happening, Why it is happening, What is likely next, What we should do
- Dynamic decision cards in the prescriptive layer
- Grab-inspired light theme using brand green

## Files
- `app.py` — main Streamlit application
- `grab_superapp_synthetic.csv` — synthetic source dataset
- `requirements.txt` — dependencies
- `.streamlit/config.toml` — Grab-inspired theme

## Repo structure
```text
repo/
├── app.py
├── grab_superapp_synthetic.csv
├── requirements.txt
└── .streamlit/
    └── config.toml
```

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Design logic
The app is organized around the three business problems from the Grab case:
1. Driver Trust and Failed Bookings
2. Super-App Growth and Single-Service Dependency
3. Pricing Fairness, Surge Shock, and Hidden Fees

Each problem page is broken into four business-readable blocks so non-technical stakeholders can understand the narrative from symptom to decision.
