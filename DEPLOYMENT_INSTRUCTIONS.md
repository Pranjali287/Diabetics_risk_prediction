# Deployment Guide

This project is configured for deployment on platforms like **Render** or **Heroku**.
The application is set up as a unified deployment where the Flask backend serves the React frontend.

## Prerequisites

1.  **Git Repository**: Ensure your project is initialized as a git repository and pushed to GitHub.
2.  **Render Account**: Create an account at [render.com](https://render.com).

## Deployment Steps (Render)

### Option 1: Using render.yaml (Recommended)

1.  Log in to Render dashboard.
2.  Click **New +** -> **Blueprint**.
3.  Connect your GitHub repository.
4.  Render will automatically detect the `render.yaml` file in the root directory.
5.  Click **Apply**.

### Option 2: Manual Setup

1.  Log in to Render dashboard.
2.  Click **New +** -> **Web Service**.
3.  Connect your GitHub repository.
4.  If prompted for **Root Directory**, leave it empty (or set to `.`).
5.  **Build Command**:
    ```bash
    cd "snp mini/Diabetes_project/Frontend" && npm install && npm run build && cd ../Backend && pip install -r requirements.txt
    ```
6.  **Start Command**:
    ```bash
    cd "snp mini/Diabetes_project/Backend" && gunicorn app:app
    ```
7.  **Environment Variables**:
    -   Key: `PYTHON_VERSION`
    -   Value: `3.10.0` (or your preferred version)

## Local Testing

To test the production build locally:

1.  Navigate to `snp mini/Diabetes_project/Frontend`:
    ```bash
    cd "snp mini/Diabetes_project/Frontend"
    npm run build
    ```
2.  Navigate to `snp mini/Diabetes_project/Backend`:
    ```bash
    cd "../Backend"
    python app.py
    ```
3.  Open `http://localhost:5000`. You should see the React app served by Flask.

## Notes

-   **Frontend API URL**: The frontend is configured to use a relative path (`/predict`) in production, so it automatically points to the backend on the same domain.
-   **Static Files**: The Flask app is configured to serve static files from `../Frontend/build` (configured in `app.py`).