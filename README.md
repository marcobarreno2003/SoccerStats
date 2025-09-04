
# ⚽ SoccerStats

A web application that uses **Machine Learning** to predict soccer match outcomes in real time.  
Built with **Flask, TensorFlow/Keras, Pandas, Joblib**, and live data from the **API-Football**.

---

## 🚀 Features
- Predicts Win/Draw/Loss with ~81% accuracy using a deep learning model.  
- Integrates live match data from API-Football.  
- Supports European leagues (Premier League, LaLiga, Bundesliga, Serie A, Ligue 1), UEFA cups, and South American leagues.  
- Flask frontend with custom HTML/CSS/JS.  
- Organized project structure: `api/` (logic + ML), `templates/` (HTML), `static/` (assets).

---

## 🗂 Project Structure
```

SoccerStats/
├─ app.py
├─ requirements.txt
├─ api/
│  ├─ data.py
│  ├─ get\_data.py
│  ├─ models/
│  │  ├─ soccer\_model.keras
│  │  ├─ scaler.save
│  │  └─ column\_transformer.save
├─ templates/
│  ├─ index.html
│  ├─ about.html
│  ├─ blog.html
│  ├─ live\_matches.html
│  └─ predict.html
└─ static/
├─ css/style.css
├─ js/app.js
└─ images/

````

---

## ⚙️ Installation
```bash
# Clone repository
git clone https://github.com/marcobarreno2003/SoccerStats.git
cd SoccerStats

# Create virtual environment
python -m venv .venv
# Activate
# Linux/Mac
source .venv/bin/activate
# Windows
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
````

---

## 🔑 Environment Variables

Create a `.env` file with your API-Football key:

```
API_FOOTBALL_KEY=your_api_key_here
```

---

## ▶️ Run the App

```bash
python app.py
```

Then open: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## 👤 Author

**Marco Barreno**
[LinkedIn](https://www.linkedin.com/in/marco-barreno-uh/) | [GitHub](https://github.com/marcobarreno2003)

