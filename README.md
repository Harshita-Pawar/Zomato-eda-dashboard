# 🍽️ Zomato India — EDA Dashboard

An interactive Exploratory Data Analysis dashboard built with **Streamlit** and **Plotly**, analysing restaurant trends across Indian cities using the Zomato dataset.

## 🔍 What This Dashboard Covers

| Section | Analysis |
|---|---|
| 📍 City Analysis | Top cities by restaurant count & avg rating |
| 🍜 Cuisine Trends | Most popular cuisines across India |
| 💰 Price vs Rating | Does expensive = better rated? |
| ⭐ Rating Distribution | Breakdown of restaurant quality bands |
| 🛵 Delivery & Booking | Online delivery & table booking adoption |
| 🏆 Top Chains | Most widely distributed restaurant chains |

## 🛠️ Tech Stack

- **Python** — Data processing
- **Pandas** — Data wrangling
- **Plotly** — Interactive visualizations
- **Streamlit** — Web app framework

## 🚀 How to Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/zomato-eda-dashboard.git
cd zomato-eda-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add the dataset
# Download zomato.csv and Country-Code.xlsx from:
# https://www.kaggle.com/datasets/shrutimehta/zomato-restaurants-data
# Place both files inside the /data folder

# 4. Run the app
streamlit run app.py
```

## 📁 Project Structure

```
zomato-eda-dashboard/
│
├── data/
│   ├── zomato.csv
│   └── Country-Code.xlsx
│
├── app.py              # Streamlit UI
├── analysis.py         # Plotly chart functions
├── requirements.txt
└── README.md
```

## 📊 Key Insights

1. **New Delhi** has the most restaurants but smaller cities often have higher average ratings
2. **North Indian and Chinese** cuisines dominate the Indian food market
3. **Price and rating have weak positive correlation** — budget restaurants can still rate highly
4. Only ~**35%** of listed restaurants offer online delivery, showing room for growth
5. **Cafe Coffee Day** and **Domino's** are the most widespread chains in India

## 📂 Dataset

[Zomato Restaurants Dataset — Kaggle](https://www.kaggle.com/datasets/shrutimehta/zomato-restaurants-data)

---

Built by **Harshita** | B.Tech Data Science, SPPU
