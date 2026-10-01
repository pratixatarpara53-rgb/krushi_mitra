# 🌾 KhedutMitra – Smart Farming Guide

A simple, attractive, and beginner-friendly agricultural information website built with **Python Flask**.

## 📁 Project Structure

```
KhedutMitra/
├── app.py                   # Flask application & crop data
├── requirements.txt         # Python dependencies
├── templates/
│   ├── base.html            # Shared layout (navbar + footer)
│   ├── index.html           # Home page
│   ├── crops.html           # Crop Guide (searchable)
│   ├── crop_details.html    # Individual crop page
│   ├── tips.html            # Farming Tips
│   └── calendar.html        # Crop Calendar (Kharif/Rabi/Zaid)
└── static/
    ├── style.css            # All styles (green/cream theme)
    ├── script.js            # Search, mobile nav, animations
    └── images/              # (optional) local crop images
```

## 🚀 How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the server

```bash
python app.py
```

### 3. Open your browser

```
http://127.0.0.1:5000
```

## 📄 Pages

| URL | Page |
|---|---|
| `/` | Home – hero, stats, featured crops, features |
| `/crops` | Crop Guide – 8 crop cards with live JS search |
| `/crops/<id>` | Crop Details – soil, irrigation, growth stages, tips |
| `/tips` | Farming Tips – 6 guide cards |
| `/calendar` | Crop Calendar – Kharif, Rabi, Zaid seasons |

## 🌾 Crops Covered

Cotton · Groundnut · Wheat · Bajra · Maize · Cumin · Chilli · Onion

## 🖼️ Adding Local Images

Drop `.jpg` images into `static/images/` with these exact filenames:

```
cotton.jpg  groundnut.jpg  wheat.jpg  bajra.jpg
maize.jpg   cumin.jpg      chilli.jpg  onion.jpg
```

If an image file is missing, the app automatically shows a coloured placeholder.

## 🛠️ Technology

- **Backend:** Python 3 + Flask (1 file, no database)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **No APIs, no login, no payment, no external services**

## 📖 Viva Points

1. **Flask routing** – `@app.route()` decorators map URLs to Python functions
2. **Jinja2 templating** – `{% extends %}` / `{% block %}` for DRY HTML
3. **Static data** – crop info stored as Python list of dictionaries (`app.py`)
4. **JavaScript search** – filters cards client-side, no server round-trip
5. **Responsive design** – CSS Grid + media queries, mobile-friendly
6. **Scroll animations** – `IntersectionObserver` API for reveal on scroll
