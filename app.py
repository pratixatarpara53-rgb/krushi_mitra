from flask import Flask, render_template

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Static crop data – no database needed
# ---------------------------------------------------------------------------
CROPS = [
    {
        "id": "cotton",
        "name": "Cotton",
        "gujarati": "કપાસ",
        "season": "Kharif",
        "soil": "Black Cotton Soil",
        "image": "cotton.jpg",
        "short_desc": "Major cash crop of Gujarat, grown across sandy loam and black soils.",
        "details": {
            "suitable_season": "Kharif (June – November)",
            "soil_info": "Deep black cotton soil or medium loamy soil with good drainage.",
            "irrigation": "Requires moderate irrigation. Drip irrigation preferred. Avoid water-logging.",
            "growth_stages": ["Germination (0–10 days)", "Vegetative (10–50 days)",
                              "Flowering (50–90 days)", "Boll Development (90–130 days)", "Harvesting (130–180 days)"],
            "harvesting": "Harvest when bolls fully open (white fluffy fibre visible). Multiple pickings required.",
            "tips": ["Use certified Bt cotton seeds.", "Maintain row spacing of 60–90 cm.",
                     "Monitor for pink bollworm and whitefly.", "Apply balanced NPK fertiliser."]
        }
    },
    {
        "id": "groundnut",
        "name": "Groundnut",
        "gujarati": "મગફળી",
        "season": "Kharif",
        "soil": "Sandy Loam",
        "image": "groundnut.jpg",
        "short_desc": "Primary oilseed crop, well adapted to light sandy loam soils.",
        "details": {
            "suitable_season": "Kharif (June – October)",
            "soil_info": "Well-drained sandy loam soil, pH 6.0–7.0. Avoid heavy clay soils.",
            "irrigation": "Requires 400–600 mm water. Critical stages: flowering and pod filling.",
            "growth_stages": ["Sowing (0–7 days)", "Vegetative (7–30 days)",
                              "Pegging (30–50 days)", "Pod Development (50–90 days)", "Maturity (90–120 days)"],
            "harvesting": "Harvest when leaves turn yellow and pods have firm shells. Lift carefully.",
            "tips": ["Treat seeds with Rhizobium culture before sowing.", "Maintain spacing 30×10 cm.",
                     "Avoid excess nitrogen; crop fixes its own nitrogen.", "Ensure good calcium availability."]
        }
    },
    {
        "id": "wheat",
        "name": "Wheat",
        "gujarati": "ઘઉં",
        "season": "Rabi",
        "soil": "Loam / Clay Loam",
        "image": "wheat.jpg",
        "short_desc": "Staple food grain crop grown in the cool winter season across India.",
        "details": {
            "suitable_season": "Rabi (November – March)",
            "soil_info": "Well-drained loam or clay loam soils, pH 6.0–7.5.",
            "irrigation": "4–6 irrigations needed. Critical stages: crown root initiation and grain filling.",
            "growth_stages": ["Germination (0–7 days)", "Tillering (20–45 days)",
                              "Jointing (45–65 days)", "Heading (65–80 days)", "Grain Filling & Maturity (80–120 days)"],
            "harvesting": "Harvest when grains turn golden yellow and moisture drops to ~12–14%.",
            "tips": ["Sow on time (Nov 1–15) for best yield.", "Use improved varieties like GW-496.",
                     "Apply urea in split doses.", "Watch for rust diseases."]
        }
    },
    {
        "id": "bajra",
        "name": "Bajra",
        "gujarati": "બાજરો",
        "season": "Kharif",
        "soil": "Sandy / Light Loam",
        "image": "bajra.jpg",
        "short_desc": "Drought-tolerant millet crop, ideal for drier regions with light soils.",
        "details": {
            "suitable_season": "Kharif (June – September)",
            "soil_info": "Light sandy to loamy soils, pH 6.5–8.0. Tolerates low fertility.",
            "irrigation": "Drought tolerant. 2–3 irrigations sufficient. Avoid water-logging.",
            "growth_stages": ["Germination (0–5 days)", "Vegetative (5–35 days)",
                              "Booting (35–50 days)", "Heading (50–65 days)", "Grain Maturity (65–80 days)"],
            "harvesting": "Harvest when panicle turns greyish-brown and grains are hard.",
            "tips": ["Use hybrid seeds for higher yield.", "Thin seedlings to 15 cm spacing.",
                     "Suitable for low-rainfall areas (300–500 mm).", "Rotate with legumes for soil health."]
        }
    },
    {
        "id": "maize",
        "name": "Maize",
        "gujarati": "મકાઈ",
        "season": "Kharif / Rabi",
        "soil": "Well-drained Loam",
        "image": "maize.jpg",
        "short_desc": "Versatile cereal crop used for food, fodder, and industrial purposes.",
        "details": {
            "suitable_season": "Kharif (June–Sept) and Rabi (Oct–Feb)",
            "soil_info": "Deep well-drained loam soil, pH 6.0–7.5. Cannot tolerate water-logging.",
            "irrigation": "Requires 500–800 mm water. Critical: tasselling and grain filling stages.",
            "growth_stages": ["Germination (0–7 days)", "Vegetative V1–V6 (7–30 days)",
                              "Tasselling (30–55 days)", "Silking & Pollination (55–70 days)", "Maturity (70–100 days)"],
            "harvesting": "Harvest when husks turn brown and kernels show a black layer at tip.",
            "tips": ["Maintain spacing 60×25 cm.", "Apply zinc sulphate to prevent deficiency.",
                     "Side-dress with nitrogen at knee-high stage.", "Keep field weed-free for first 30 days."]
        }
    },
    {
        "id": "cumin",
        "name": "Cumin",
        "gujarati": "જીરૂ",
        "season": "Rabi",
        "soil": "Sandy Loam",
        "image": "cumin.jpg",
        "short_desc": "High-value spice crop of Gujarat and Rajasthan, grown in cool dry conditions.",
        "details": {
            "suitable_season": "Rabi (November – February)",
            "soil_info": "Well-drained sandy loam soil, pH 7.0–8.0. Poor drainage causes wilt.",
            "irrigation": "3–4 light irrigations. Avoid overhead irrigation to reduce blight risk.",
            "growth_stages": ["Germination (0–10 days)", "Seedling (10–30 days)",
                              "Branching (30–55 days)", "Flowering (55–70 days)", "Seed Maturity (70–110 days)"],
            "harvesting": "Harvest when 70% plants turn yellowish-brown. Dry thoroughly before threshing.",
            "tips": ["Sow in cool weather (Oct–Nov).", "Avoid high humidity and foggy conditions.",
                     "Use disease-resistant varieties.", "Apply light mulch after sowing."]
        }
    },
    {
        "id": "chilli",
        "name": "Chilli",
        "gujarati": "મરચું",
        "season": "Kharif / Rabi",
        "soil": "Loam / Sandy Loam",
        "image": "chilli.jpg",
        "short_desc": "Important spice and vegetable crop with both fresh and dry market value.",
        "details": {
            "suitable_season": "Kharif (June–Nov) and Rabi transplant (Sept–Oct)",
            "soil_info": "Fertile loam or sandy loam, pH 6.0–7.0. Good drainage essential.",
            "irrigation": "Regular irrigation every 7–10 days. Drip irrigation recommended.",
            "growth_stages": ["Nursery (0–30 days)", "Transplanting & Establishment (30–50 days)",
                              "Flowering (50–80 days)", "Fruit Setting (80–110 days)", "Harvesting (110–180 days)"],
            "harvesting": "Harvest green chillies at full size; red chillies when fully red.",
            "tips": ["Raise nursery in raised beds.", "Transplant 25–30 day old seedlings.",
                     "Stake plants to support heavy fruit load.", "Monitor for thrips and mites."]
        }
    },
    {
        "id": "onion",
        "name": "Onion",
        "gujarati": "ડુંગળી",
        "season": "Rabi / Kharif",
        "soil": "Well-drained Loam",
        "image": "onion.jpg",
        "short_desc": "Essential vegetable crop with strong demand in domestic and export markets.",
        "details": {
            "suitable_season": "Rabi (Oct–April) is most common; Kharif sowing also practised.",
            "soil_info": "Well-drained fertile loamy soil, pH 6.0–7.5. Avoid saline soils.",
            "irrigation": "Frequent light irrigation. Stop irrigation 15 days before harvest for curing.",
            "growth_stages": ["Nursery (0–40 days)", "Transplanting (40–60 days)",
                              "Bulb Initiation (60–90 days)", "Bulb Development (90–120 days)", "Maturity (120–150 days)"],
            "harvesting": "Harvest when 50–75% of neck tops fall over. Cure in field for 5–7 days.",
            "tips": ["Transplant 6-week-old seedlings.", "Apply potash for good bulb quality.",
                     "Avoid excess nitrogen to reduce bolting.", "Store in well-ventilated conditions."]
        }
    },
]

TIPS = [
    {
        "id": "soil-preparation",
        "title": "Soil Preparation",
        "icon": "🌍",
        "summary": "Proper soil preparation creates the ideal seedbed and improves nutrient availability.",
        "points": [
            "Deep plough to 20–30 cm depth before the monsoon.",
            "Add well-decomposed farmyard manure (FYM) @ 10–15 tonnes/hectare.",
            "Level the field to ensure uniform water distribution.",
            "Perform soil testing every 2–3 years to understand nutrient status.",
            "Incorporate crop residue by ploughing it back into the soil.",
        ]
    },
    {
        "id": "seed-selection",
        "title": "Seed Selection",
        "icon": "🌱",
        "summary": "High-quality seeds are the foundation of a successful crop.",
        "points": [
            "Always buy certified seeds from government-approved sources.",
            "Check seed germination rate (should be >85%).",
            "Choose varieties suited to your local agro-climatic zone.",
            "Treat seeds with fungicide/bio-agent before sowing to prevent soil-borne diseases.",
            "Store unused seeds in a cool, dry, airtight container.",
        ]
    },
    {
        "id": "sowing",
        "title": "Sowing Techniques",
        "icon": "🌾",
        "summary": "Correct sowing time, spacing, and depth ensure uniform crop establishment.",
        "points": [
            "Follow recommended sowing time for each crop and season.",
            "Maintain proper row and plant spacing as per crop requirement.",
            "Sow seeds at the correct depth (usually 2–4 cm for most crops).",
            "Use a seed drill for uniform spacing and better germination.",
            "Thin out extra seedlings within 10–15 days of germination.",
        ]
    },
    {
        "id": "irrigation",
        "title": "Irrigation Management",
        "icon": "💧",
        "summary": "Efficient water management increases yield and reduces water waste.",
        "points": [
            "Adopt drip or sprinkler irrigation for water efficiency.",
            "Irrigate at critical crop growth stages (flowering, grain filling).",
            "Avoid over-irrigation; it leads to water-logging and root diseases.",
            "Mulch the soil to reduce evaporation.",
            "Schedule irrigation during cooler parts of the day (morning/evening).",
        ]
    },
    {
        "id": "weed-management",
        "title": "Weed Management",
        "icon": "🌿",
        "summary": "Controlling weeds early protects nutrients and prevents yield loss.",
        "points": [
            "Keep the field weed-free for the first 30–45 days (critical period).",
            "Use intercultivation tools for mechanical weeding between rows.",
            "Mulching with paddy straw or plastic film suppresses weed growth.",
            "Follow crop rotation to break weed cycles.",
            "Hand-weeding is effective for small plots and labour-available farms.",
        ]
    },
    {
        "id": "harvesting",
        "title": "Harvesting & Post-Harvest",
        "icon": "🌻",
        "summary": "Timely harvesting and proper post-harvest handling minimise losses.",
        "points": [
            "Harvest at the right maturity stage to maximise quality and yield.",
            "Avoid harvesting during rain or high humidity to prevent mould.",
            "Dry produce to safe moisture levels before storage.",
            "Use clean, dry containers or bags for storage.",
            "Grade and sort produce before selling to get better market price.",
        ]
    },
]

CALENDAR = {
    "Kharif": {
        "period": "June – November",
        "description": "Crops sown at the onset of the South-West monsoon (June–July) and harvested in autumn.",
        "color": "#2d8a4e",
        "crops": ["Cotton", "Groundnut", "Bajra", "Maize", "Soybean", "Moong", "Chilli", "Sesame"],
        "key_activities": ["Land preparation (April–May)", "Sowing (June–July)",
                           "Top dressing (July–Aug)", "Irrigation management (Aug–Sept)", "Harvesting (Oct–Nov)"]
    },
    "Rabi": {
        "period": "October – March",
        "description": "Cool-season crops sown after the monsoon retreats and harvested in spring.",
        "color": "#b5830a",
        "crops": ["Wheat", "Cumin", "Mustard", "Gram (Chickpea)", "Onion", "Potato", "Linseed", "Fennel"],
        "key_activities": ["Soil preparation (Sept–Oct)", "Sowing (Oct–Nov)",
                           "Irrigation (Nov–Feb)", "Fertiliser application (Nov–Dec)", "Harvesting (Feb–Mar)"]
    },
    "Zaid": {
        "period": "March – June",
        "description": "Short-duration summer crops grown between Rabi and Kharif seasons.",
        "color": "#c0522a",
        "crops": ["Watermelon", "Muskmelon", "Cucumber", "Pumpkin", "Moong", "Sunflower", "Fodder Maize"],
        "key_activities": ["Sowing (Feb–Mar)", "Frequent irrigation (Mar–May)",
                           "Harvesting (May–June)", "Land preparation for Kharif (June)"]
    }
}


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    featured = CROPS[:6]
    return render_template("index.html", crops=featured)


@app.route("/crops")
def crops():
    return render_template("crops.html", crops=CROPS)


@app.route("/crops/<crop_id>")
def crop_details(crop_id):
    crop = next((c for c in CROPS if c["id"] == crop_id), None)
    if crop is None:
        return render_template("404.html"), 404
    return render_template("crop_details.html", crop=crop)


@app.route("/tips")
def tips():
    return render_template("tips.html", tips=TIPS)


@app.route("/calendar")
def calendar():
    return render_template("calendar.html", calendar=CALENDAR)


if __name__ == "__main__":
    app.run(debug=True)
