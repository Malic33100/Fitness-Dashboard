# Fitness Analytics Dashboard

![Dashboard Preview](TBD)

Real-time workout tracking and analytics dashboard integrating Strava API with automated data pipelines and interactive visualizations.

##  Overview

Personal fitness analytics dashboard that automatically syncs workout data from Strava, processes it through a Python ETL pipeline, and visualizes training metrics in an interactive PowerBI dashboard.

**Live Dashboard:** [Link coming soon]

##  Features

- **Automated Data Pipeline:** OAuth 2.0 integration with Strava API
- **ETL Processing:** Python-based data extraction, transformation, and loading
- **Interactive Visualizations:** 10+ PowerBI charts tracking key metrics
- **Historical Analysis:** Retrieves Most recent 200 activities with customizable filters
- **Multi-Activity Support:** Tracks runs, rides, walks, strength training, and more
- **Performance Metrics:** Distance, pace, heart rate, elevation, calories

##  Tech Stack

**Backend & Data:**
- Python 3.13, pandas (data processing), requests (HTTP client)
- Strava API v3
- OAuth 2.0

**Visualization:**
- Microsoft PowerBI Desktop
- PowerBI Service (cloud hosting)

**Development:**
- python-dotenv (environment management)
- Git version control

## Dashboard Metrics

**Key Performance Indicators:**
- Total distance (km/miles)
- Total activities
- Average heart rate
- Total training time

**Visualizations:**
- Distance over time (line chart)
- Activity distribution (bar chart)
- Workout breakdown by type (donut chart)
- Weekly training schedule (heatmap)
- Pace analysis (trends)

###  Setup Instructions

### What you need

- Python 3.8+
- Strava account with API access
- PowerBI Desktop (Windows)

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/fitness-dashboard.git
cd fitness-dashboard
```

### 2. Install Dependencies & Create Virtual environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 3. Configure Strava API

**Create Strava API Application:**
1. Go to https://www.strava.com/settings/api
2. Click "Create an App"
3. Fill in details:
   - **Application Name:** Fitness Analytics Dashboard
   - **Category:** Visualizer
   - **Website:** `http://localhost`
   - **Authorization Callback Domain:** `localhost`
4. Click "Create"
5. Copy your **Client ID** and **Client Secret**
   Note: Please don't share these with anyone

### 4. Set Up Environment Variables

Create a `.env` file in the project root & add it to your git ignore if not already there:
```bash
STRAVA_CLIENT_ID=your_client_id_here
STRAVA_CLIENT_SECRET=your_client_secret_here
STRAVA_REFRESH_TOKEN=will_add_after_authorization
```

**Important:** Never commit your `.env` file to Git. It's already in `.gitignore`.

### 5. Get Refresh Token

Run the authorization script to get your refresh token:
```bash
python get_refresh_token.py
```

**Steps:**
1. Script will print an authorization URL
2. Copy and paste the URL into your browser
3. Click "Authorize" on Strava
4. You'll be redirected to `http://localhost/?code=ABC123...`
5. Copy the code from the URL (everything after `code=`)
6. Paste the code back into the terminal
7. Script will print your **Refresh Token**
8. Copy the refresh token and add it to your `.env` file:
```
   STRAVA_REFRESH_TOKEN=your_refresh_token_here
```

### 6. Run ETL Pipeline

Fetch your Strava data:
```bash
python fitness-script.py
```

**Output:**
- Creates `strava_data.csv` with your workout data
- Prints summary statistics
- Ready for PowerBI import

### 7. Build Dashboard (PowerBI)

1. Open PowerBI Desktop
2. **Get Data** → **Text/CSV**
3. Select `strava_data.csv`
4. Click **Load**
5. Build visualizations (see Architecture section)
6. **File** → **Publish** → Publish to PowerBI Service



## Project Structure
```
fitness-dashboard/
├── .env                      # Environment variables (not in repo)
├── .gitignore               # Git ignore rules
├── requirements.txt         # Python dependencies
├── README.md                # This file
├── fitness-script.py        # Main ETL pipeline
├── get_refresh_token.py     # OAuth setup script
├── strava_data.csv          # Generated data (not in repo)
└── screenshots/             # Dashboard images
    └── dashboard.png
```

## Architecture
```
┌─────────────┐
│  Strava API │
└──────┬──────┘
       │ OAuth 2.0
       ↓
┌─────────────────┐
│  Python ETL     │
│  (fitness-      │
│   script.py)    │
└────────┬────────┘
         │ CSV Export
         ↓
┌─────────────────┐
│  strava_data    │
│  .csv           │
└────────┬────────┘
         │ Import
         ↓
┌─────────────────┐
│  PowerBI        │
│  Dashboard      │
└────────┬────────┘
         │ Publish
         ↓
┌─────────────────┐
│  PowerBI        │
│  Service (Web)  │
└─────────────────┘
```

##  Updating Data

To refresh your dashboard with new workouts:
```bash
# Fetch latest data
python fitness-script.py

# Open PowerBI Desktop
# Home tab → Refresh
# File → Publish (to update web version)
```

##  Sample Output
```
Starting Strava ETL Pipeline

Getting fresh access token...
✓ Access token obtained
Fetching last 200 activities from Strava...
✓ Retrieved 142 activities
Processing activity data...
✓ Processed 142 activities
✓ Exported to strava_data.csv

==================================================
SUMMARY STATISTICS
==================================================
Total activities: 142
Date range: 2023-06-15 to 2024-12-01
Total distance: 487.3 km
Total time: 4234 minutes (70.6 hours)

Activities by type:
Run              98
WeightTraining   32
Walk             12
==================================================
```

##  Security Notes

- **Never commit `.env` file** - contains sensitive API credentials
- **Refresh tokens are long-lived** - treat them like passwords
- **Access tokens expire** - script automatically refreshes them
- **Scope:** Dashboard has read-only access to your activities

##  Future Enhancements

- [ ] Automated daily data refresh (Azure Functions)
- [ ] Database storage (Azure SQL / PostgreSQL)
- [ ] Mobile-responsive web dashboard
- [ ] Predictive analytics for training trends
- [ ] Goal tracking and progress alerts
- [ ] Integration with Apple Health / Garmin
- [ ] Multi-user support

### 📝 License

MIT License - feel free to use this for your own projects

###  Contributions

This is a personal portfolio project, but suggestions and feedback are welcome

### 📧 Contact

More about me: Malik Mertus
- Portfolio: [malikmertus.com](https://malikmertus.com)
- LinkedIn: [linkedin.com/in/malikmertus](https://linkedin.com/in/malikmertus)
- GitHub: [@malikmertus](https://github.com/malic33100)

---
