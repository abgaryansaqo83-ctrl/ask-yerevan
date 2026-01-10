askyerevan/
├── backend/
│   ├── bot.py                # Telegram բոտի entrypoint, handlers, spam filter, news menu
│   ├── scheduler.py          # APScheduler job runner՝ weather/traffic/events ուղարկելու համար
│   ├── jobs.py               # Scheduler job-երի սահմանումներ
│   ├── database.py           # DB connection և schema init/helpers
│   ├── languages.py          # HY/RU/EN թարգմանություններ և gettext helper
│   ├── news_scraper.py       # Հայաստանի նորությունների scraping/RSS logic
│   ├── web_app.py            # FastAPI web app (HTML էջեր + healthcheck)
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py       # Environment settings (BOTTOKEN, DBPATH, TIMEZONE, API keys)
│   │
│   ├── ai/
│   │   ├── __init__.py
│   │   └── response.py       # AI/Perplexity integration for AskYerevan replies
│   │
│   ├── armenia/
│   │   ├── __init__.py
│   │   ├── events.py         # Event selection logic (week premiere, category news, festivals)
│   │   ├── events_sources.py # Tomsarkgh.am scraper (cinema/theatre/opera/party/festival)
│   │   ├── recommend.py      # Recommendation logic for places/events
│   │   ├── traffic.py        # Traffic/status (e.g. Google Directions)
│   │   └── weather.py        # OpenWeather API wrapper for Armenia/Yerevan
│   │
│   └── utils/
│       ├── __init__.py
│       ├── helpers.py        # Common helper functions
│       ├── keyboards.py      # Telegram reply/inline keyboards
│       ├── listings.py       # Classified listings detection (sell/rent/search/job)
│       └── logger.py         # Logging setup
│
├── static/
│   ├── css/
│   │   ├── main.css          # Main site styles (header, navigation, hero, footer)
│   │   └── winter.css        # Seasonal/winter theme overrides
│   │
│   └── img/
│       ├── logo/             # Logos, Telegram icon, rug-texture background
│       ├── churches/         # Armenian churches & monasteries imagery
│       ├── sights/           # Armenia & Yerevan sights/landscapes
│       ├── places/           # Restaurants, bars, clubs, spa & getaway photos
│       └── seasonal/         # New Year / seasonal icons (tree, Santa, lights)
│
├── templates/
│   ├── base.html             # Base layout (header, nav, footer)
│   ├── index_hy.html         # Home page (HY)
│   ├── index_en.html         # Home page (EN)
│   ├── sights_hy.html        # Sights & nature (HY)
│   ├── sights_en.html        # Sights & nature (EN)
│   ├── churches_hy.html      # Churches & monasteries (HY)
│   ├── churches_en.html      # Churches & monasteries (EN)
│   ├── places_hy.html        # Places: food, bars, getaways (HY)
│   ├── places_en.html        # Places: food, bars, getaways (EN)
│   ├── news_hy.html          # News & events list (HY)
│   ├── news_en.html          # News & events list (EN)
│   ├── news_detail_hy.html   # Single news/event detail (HY)
│   ├── news_detail_en.html   # Single news/event detail (EN)
│   ├── about_hy.html         # About AskYerevan (HY)
│   └── about_en.html         # About AskYerevan (EN)
│
├── sitemap.xml               # XML sitemap for search engines
├── Procfile                  # Process types for Render/Heroku-style deploys
├── render.yaml               # Render.com service configuration
├── requirements.txt          # Python dependencies
├── .env                      # Local environment configuration (not committed)
└── .env.example              # Example env file for setup
