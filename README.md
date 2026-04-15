# Birthday Paradox Monte Carlo Demo

This project is a small Streamlit app that demonstrates the birthday paradox with a Monte Carlo simulation.

## Run locally

1. Create and activate a virtual environment.
2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Start the app:

```powershell
streamlit run birthday_paradox_demo.py
```

## Publish to GitHub

If Git is installed:

```powershell
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
git push -u origin main
```

If Git is not installed, you can also:

1. Create a new empty repository on GitHub.
2. Click **Add file** -> **Upload files**.
3. Upload `birthday_paradox_demo.py`, `requirements.txt`, `.gitignore`, and `README.md`.
4. Commit the files to the `main` branch.

## Deploy on Streamlit Community Cloud

1. Push this folder to a GitHub repository.
2. Go to https://share.streamlit.io/
3. Sign in with GitHub.
4. Click **Create app**.
5. Choose your repository and branch.
6. Set the main file path to `birthday_paradox_demo.py`.
7. Click **Deploy**.

## Notes

- `requirements.txt` is required so Streamlit Cloud knows what to install.
- This app only needs `streamlit` and `matplotlib`; the rest comes from Python's standard library.
