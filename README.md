# Insta Sugar Intelligence

Instagram performance analytics for Sugar Cosmetics, built with Python and Streamlit.

## What this project does
Analyses 50,000 Instagram post records to show which formats, campaigns, posting days
and hashtags are associated with higher engagement, and includes a Content Recipe Lab
that tests whether any content "recipe" is truly better than average.

## Data
- Source: dataset provided by the LabMatics mentor (50,000 rows, 14 columns, 19 Apr 2024 to 19 Apr 2025).
- Limitations: no caption or post ID, the data looks synthetic, and results show association, not cause.
- Engagement rate (project definition) = (Likes + Comments + Shares + Saves) / Reach x 100.

## Project type
Descriptive analytics. No predictive model is used.

## How to run
1. Install: `pip install -r requirements.txt`
2. Run: `streamlit run app.py`

## Folders
- `app.py`: the Streamlit app
- `data/`: raw and cleaned data
- `notebooks/`: Google Colab notebook (data preparation)
- `assets/`: logos

## Author
YOUR NAME, LabMatics internship project
