# Web-Based Trading System

Welcome to our real-time trading dashboard built with **Streamlit**. This project integrates machine learning models to provide live trading predictions, visual analytics, and backtesting strategies based on historical stock data.

---

## Features

- **Live Stock Dashboard**  
  Fetches and displays stock data from the SimFin API.

- **ML Price Predictions**  
  Uses a classification model to predict if the price will go up/down. Also includes a regression model to forecast the next-day close.

- **Backtesting Simulator**  
  Simulates portfolio performance using historical predictions.

- **ML Model Explanation Page**  
  Showcases how the models were trained, including feature engineering, metrics (accuracy, precision, recall, F1), and model insights (XGBoost).

---

## Tech Stack

- `Streamlit` – Web app framework  
- `Pandas / Numpy` – Data handling  
- `Scikit-learn / LR, RF, XGBoost, XGBRegressor` – Machine learning  
- `Plotly / Matplotlib / Streamlit-Lightweight` – Visualizations  
- `SimFin API` – Real-time stock data  

---

## Project Structure
Python_Group_Project/
│
├── app.py                    # Main Streamlit file
├── pages/                    # Multi-page Streamlit setup
│   ├── A_Home.py
│   ├── B_Live_Trading.py
│   ├── C_About_ML.py
│   └── D_Backtesting.py
│
├── data/                     # CSV files: processed stock data
│   ├── ml_predictions.csv
│   ├── processed_data_enhanced.csv
│   └── processed_data.csv
│
├── test/                     # Pytest unit tests
│   ├── test_B_Live_Trading.py
│   ├── test_C_About_ML.py
│   └── test_D_Backtesting.py
│
├── ETL_batch.ipynb
├── ML_methods.ipynb
├── ML_Price_Predictions.ipynb
├── SimFin_API_ETL.ipynb
├── SIMFIN_API_TEST.ipynb
├── requirements.txt
└── README.md

---

## Installation & Setup

### Prerequisites
Make sure you have Python ≥ 3.9 installed.

### Clone & Run
```bash
git clone https://github.com/roko020801/Python_Group_Project.git
cd Python_Group_Project
pip install -r requirements.txt
streamlit run app.py

---

### Authors

**Group 2**  
*Ana Cortés*
*Hiromitsu Fujiyama*
*Robert Koegel*
*Tomás Luz*
*Tomas Valbuena*

> *This project was developed as part of the Python for Data Analysis II course at IE University.*

---

### Deployment

The application is deployed on **Streamlit Cloud** and can be accessed at the following link:

[Live Web App](https://pythongroupproject-9gypnjexs7mwdygigsyg8x.streamlit.app)

> The app runs entirely in the browser — no installation required.