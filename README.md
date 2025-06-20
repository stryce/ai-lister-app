# AI Lister Web App

A simple Flask web app that generates eBay-style titles, descriptions, and keywords from uploaded item photos using OpenAI GPT-4 Vision.

---

## Run locally

1️⃣ Install dependencies:
```
pip install -r requirements.txt
```

2️⃣ Set your OpenAI API key:
```
export OPENAI_API_KEY=your_api_key
```

3️⃣ Start app:
```
python app.py
```

4️⃣ Go to: http://localhost:5000

---

## Deploy to Render

1️⃣ New web service  
2️⃣ Connect this repo  
3️⃣ Build command: `pip install -r requirements.txt`  
4️⃣ Start command: `python app.py`  
5️⃣ Add env var: `OPENAI_API_KEY`
