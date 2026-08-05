# Indian Skincare Demand Intelligence

> Mapping consumer search signals to brand supply across 8 Indian skincare brands · 2021–2026

## What This Project Does

This project builds a demand intelligence system that identifies where Indian skincare consumer demand is shifting *before* it shows up in brand sales data.

By combining Google Trends search data (29 terms, 5 years) with Nykaa supply data (265 SKUs across 8 brands), it surfaces strategic gaps between what Indian consumers are searching for and what brands are actually offering.

## Key Findings

- **The Hyperpigmentation Shift** — Kojic acid (+391%) and niacinamide (+308%) are the fastest-growing ingredients in Indian skincare, both targeting hyperpigmentation — the dominant Indian skin concern. Brands that built around these ingredients early are riding the category's highest-growth demand.

- **The Attention Economy Flip** — Legacy brands Lakme (-34%) and Himalaya (-85%) are losing consumer mindshare despite dominant offline distribution, while D2C brands grew 275–1,273% in search volume. Consumer discovery moved online; legacy brands didn't follow.

- **The Price Parity Paradox** — D2C brands (Minimalist ₹358, Foxtale ₹407) price within 10–25% of legacy brands (Lakme ₹325, Himalaya ₹310) yet are winning disproportionately on search growth and reviews — signaling a shift from brand heritage to ingredient transparency as the primary purchase driver.

## Project Structure

**data_collection/**
- `trends_collection.ipynb` — Google Trends data pull and normalisation

**dashboard/**
- `app.py` — Streamlit dashboard
- `.streamlit/config.toml` — Theme configuration

**data/**
- `skincare_trends_master.xlsx` — Normalised Google Trends data (29 terms, 61 months)
- `nykaa_data.xlsx` — Nykaa supply data (8 brands, 4 categories)

**report/**
- `Indian_Skincare_Insight_Report.docx` — Full consulting-style insight report


## Methodology

**Data Collection**
- Google Trends: 29 search terms across 4 buckets (ingredients, product types, skin concerns, brand searches), geo-filtered to India, 5-year window
- Anchor normalisation: Vitamin C selected as anchor term based on lowest coefficient of variation (CV = 0.15) among candidate terms, ensuring cross-batch comparability
- Nykaa: Manual collection of SKU count, price range, bestseller price, average rating, and review volume across 8 brands × 4 categories

**Brand Selection**
8 brands selected to represent 3 competitive tiers:
- Ingredient-led D2C: Minimalist, Foxtale
- Broad mid-tier D2C: Dot & Key, Plum, Pilgrim
- Legacy mass market: Lakme, Himalaya
- International: Cetaphil

**Analysis**
- 5-year growth rates (first year vs last year average)
- Demand vs supply gap matrix (category search growth vs brand SKU count)
- Price tier positioning across brands and categories
- Reviews per SKU as consumer engagement proxy

## Dashboard

Built with Python + Streamlit + Plotly. Four interactive views:
- Ingredient demand trends over time
- Brand search growth comparison
- Demand vs supply gap matrix
- Price tier positioning

**To run locally:**

```bash
pip install streamlit plotly pandas openpyxl
cd dashboard
streamlit run app.py
```

## Tech Stack

| Component | Tool |
|-----------|------|
| Data collection | Python, Google Trends (manual export) |
| Data processing | Pandas, NumPy |
| Dashboard | Streamlit, Plotly |
| Report | Python-docx |

## Insight Report

A 8-section consulting-style report covering category overview, ingredient trend map, brand positioning analysis, gap analysis, and strategic implications by brand tier. Available in `/report/`.

## Author

**Saanvi Bhaskar**  
B.Tech Computer Science & AI, Plaksha University  

