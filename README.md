# i243095 - AI Lab 06

## Informed Search Techniques in Python

This repository contains the completed submission for AI Lab 06. It implements and compares heuristic search techniques on weighted graphs and includes an interactive Streamlit visualization.

**GitHub repository:** https://github.com/nafayhassan799/i243095_lab_06

### Submission files

- `i243095_lab_06.ipynb` - completed and executed Jupyter notebook
- `streamlit_app.py` - interactive GBFS and A* Streamlit application
- `requirements.txt` - Python dependencies required by the notebook and app

### Completed tasks

1. Euclidean heuristic design for a warehouse robot
2. Greedy Best-First Search for airport baggage handling
3. A* search for a hospital emergency-supply robot
4. Weighted A* for an autonomous delivery drone
5. GBFS and A* search with multiple charging-station goals
6. 8-puzzle heuristic evaluation (ungraded practice)
7. GBFS on a weighted grid (ungraded practice)

Every graph visualization highlights the returned solution path. The notebook includes its executed outputs as required by the lab instructions.

### Run locally

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Launch the Streamlit application:

```bash
streamlit run streamlit_app.py
```

Then open the local address displayed by Streamlit, normally `http://localhost:8501`.

### Streamlit Community Cloud deployment

Use the following settings when deploying this repository:

- Repository: `i243095_lab_06`
- Branch: `main`
- Main file path: `streamlit_app.py`

No secrets or environment variables are required.
