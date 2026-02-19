🌍 ClimaSenseAI
AI-Powered Air Quality & Health Impact Prediction System

ClimaSenseAI is an end-to-end Machine Learning web application that predicts health risks based on air quality conditions and provides automated alerts to users.
The system integrates data processing, model training, backend APIs, and a responsive frontend interface.

🚀 Features

📊 Air Quality Health Impact Prediction using ML
🧠 Trained Machine Learning model (Pickle-based deployment)
🌐 REST API for prediction requests
📧 Automated Email Notification System
👥 Subscriber Management System
📁 Full-stack integration (Frontend + Backend)
📦 Model training and retraining pipeline

Project Architecture
ClimaSenseAI/
│
├── api.py                # API routes for prediction
├── app.py                # Main application server
├── ml_model.py           # ML model logic
├── train_model.py        # Model training pipeline
├── disease_logic.py      # Health risk analysis logic
├── email_service.py      # Email alert system
├── health_model.pkl      # Trained ML model
├── air_quality_health_impact_data.csv  # Dataset
├── subscribers.csv       # User subscriber database
├── requirements.txt      # Project dependencies
└── frontend/             # UI components

🛠️ Tech Stack
Languages: Python, HTML, CSS, JavaScript
Libraries & Frameworks: Pandas, NumPy, Scikit-learn, SMTP (for email service)
Tools: Git & GitHub, VS Code

📊 Model Details

Supervised Learning Model
Trained on air quality health impact dataset
Saved as health_model.pkl
Integrated into backend for real-time predictions

📧 Email Alert System

Stores subscribers in subscribers.csv
Sends automated alerts based on prediction results
Helps users take preventive health measures

⚙️ Installation & Setup
git clone https://github.com/Gagan-AIML/ClimaSenseAI.git
cd ClimaSenseAI
pip install -r requirements.txt
python app.py

📌 Future Improvements

Deploy to cloud (AWS/Render/Heroku)
Add real-time AQI API integration
Improve model accuracy using advanced algorithms
Add dashboard analytics
Implement database instead of CSV storage

👨‍💻 Author
Developed as a Minor Year Project in B.Tech CSE(Artificial Intelligence & Machine Learning).
