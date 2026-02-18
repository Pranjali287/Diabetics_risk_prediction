# Deploying to Streamlit Cloud

To deploy this application as a Streamlit app (instead of React + Flask):

1.  **Code Preparation**:
    I have created `streamlit_app.py` in the root directory. This single file contains the entire application logic (Frontend UI + Backend Calculation), ported from your React/Flask code.

2.  **Dependencies**:
    I have updated `requirements.txt` in the root directory to include `streamlit`.

3.  **Local Testing**:
    To run the app locally:
    ```bash
    pip install streamlit numpy pandas
    streamlit run streamlit_app.py
    ```

4.  **Deployment Steps (Streamlit Cloud)**:
    Since you cannot "host" the React parts on Streamlit Cloud, we will deploy the pure Python version (`streamlit_app.py`).

    1.  **Push to GitHub**: ensure `streamlit_app.py` and `requirements.txt` (the one in the root folder) are pushed to your GitHub repository.
    2.  **Sign in**: Go to [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub.
    3.  **Deploy**:
        -   Click **New app**.
        -   Select your **Repository**.
        -   Branch: `main` (or master).
        -   **Main file path**: `streamlit_app.py`.
        -   Click **Deploy!**.

This will launch your Diabetes Risk Prediction app completely in Python, without needing Node.js, React, or gunicorn.
