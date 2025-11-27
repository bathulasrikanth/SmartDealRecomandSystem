Smart Deal Recommendation System

A Machine Learning-based web application that predicts whether a user will redeem a promotional offer or coupon. The system analyzes user behavior, demographics, and contextual data to provide real-time recommendations.
This project integrates a trained ML model inside a Django-powered web interface.

🚀 Features

🔍 Performs feature preprocessing, cleaning, and encoding

🤖 Trained multiple ML models (Logistic Regression, Random Forest, XGBoost)

🏆 Final model selected using evaluation metrics and hyperparameter tuning

📈 Generates live prediction probability

🌐 Fully deployed using Django for real-time inference

🎨 Simple and user-friendly UI

🧠 Machine Learning Workflow

Data Cleaning & Preprocessing

Removed noisy/unnecessary columns

Handled missing values

Encoded categorical features

Scaled numerical fields

Exploratory Data Analysis

Visualized patterns and correlation

Identified key predictive features

Model Training

Logistic Regression (baseline)

Random Forest

XGBoost (final model)

Evaluation Metrics

Accuracy

Precision, Recall, F1

ROC-AUC

Model Saving

Saved using joblib.dump()

Stored model metadata for deployment

🏗️ Tech Stack
Component	Technology
Frontend	HTML, Bootstrap
Backend	Python, Django
Machine Learning	Scikit-learn, XGBoost, Pandas, NumPy
Deployment	Django model integration
📂 Project Structure
SmartDealRecommendationSystem/
├── deals/
│   ├── ml/
│   │   ├── model.pkl
│   │   └── model_metadata.pkl
│   ├── templates/
│   │   ├── home.html
│   │   └── result.html
│   ├── views.py
│   ├── urls.py
│   └── forms.py (optional)
├── SmartDealSystem/
│   └── settings.py
├── static/
├── README.md
├── manage.py
└── requirements.txt

▶️ How to Run
1️⃣ Clone the repository
git clone https://github.com/bathulasrikanth/SmartDealRecomandSystem.git
cd SmartDealRecomandSystem

2️⃣ Create Virtual Environment
python -m venv venv
source venv/Scripts/activate  # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run the Server
python manage.py runserver

5️⃣ Open in Browser
http://127.0.0.1:8000/

📊 Prediction Output Example

Probability: 0.83

Result: Eligible — High chance of redemption
