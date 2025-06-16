# 📱 MoMo Data Analysis Project

This project is part of a summative assignment to demonstrate the design and development of an enterprise-level fullstack application. The objective is to process and analyze SMS data in XML format from Rwanda’s MTN Mobile Money service (MoMo).

We were provided with over 1600 SMS messages in XML format. Our task was to clean and categorize the data, store it in a relational database, and build a frontend dashboard to visualize key insights. This assignment showcases our skills in backend data processing, database design, and interactive frontend development.

---

## 🎥 Video Walkthrough
[Link to your 5-minute demo video]

## 🎥 Project Documentation
https://docs.google.com/document/d/1v3U3EK26Hcnx3EHVm8vg6OPHNibJhqVMNEmuRD1uOaU/edit?usp=sharing

## ✨ Features

- Parse and categorize MTN SMS XML data
- Store structured results in SQLite
- Filter, search, and view transactions in a web dashboard
- Display charts and summary stats using Chart.js
- Responsive and mobile-friendly interface

---

## 🧾 Transaction Types

- Incoming Money  
- Payment Completed  
- Airtime Payment  
- Agent Withdrawal  
- Internet Bundle  
- Bank Transfer  

---

## ⚙️ Setup Instructions

### 1. Requirements

- Python 3.8+
- Web browser

### 2. Install Dependencies

```bash
cd MoMo-Summative
python -m venv venv
venv\Scripts\activate  # or: source venv/bin/activate
pip install -r requirements.txt
```

### 3. Add Your SMS Data

Put your XML file here:

```
data/modified_sms_v2.xml
```

### 4. Run the Processor

```bash
cd backend
python process_data.py
```

This creates `sms_database.db` and logs to `processing.log`.

### 5. Open the Dashboard

**Option A: Without Flask**  
Just open `frontend/index.html` in your browser.

**Option B: With Flask API**  
```bash
python app.py
```

Then open `frontend/index.html`.

---

## 🖥️ Dashboard Highlights

- 🔎 Search by keyword or name  
- 📂 Filter by transaction type  
- 📊 Charts for monthly trends and type distribution  
- 🕵️ View full message details in a modal  

---

## 👥 Contributors

- **Chris Hirwa**
  (c.hirwa@alustudent.com)

- **Promess Irakoze**
  (p.irakoze2@alustudent.com)

- **Christopher Dushimimana**
  (d.christoph@alustudent.com)