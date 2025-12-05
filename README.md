ask-yerevan/
├── backend/
│   ├── __init__.py
│   ├── bot.py              # Telegram bot main entrypoint, handlers
│   ├── database.py         # SQLite՝ events table, save/get helpers
│   ├── scheduler.py        # APScheduler runner (weekly/daily jobs)
│   ├── jobs.py             # Job wrapper-ներ, կանչում են armenia.* մոդուլները
│   ├── languages.py        # Multi-language support (HY/RU/EN)
│   ├── web_app.py          # Փոքր web app / healthcheck (կոդ կա)
│   │
│   ├── ai/
│   │   ├── __init__.py
│   │   └── response.py     # AI պատասխանների helper-ներ
│   │
│   ├── armenia/
│   │   ├── __init__.py
│   │   ├── weather.py      # Եղանակի API wrapper
│   │   ├── traffic.py      # Խցանումների հաշվարկ և հաղորդագրություններ
│   │   ├── events_sources.py  # Tomsarkgh scraper + DB refresh logic
│   │   ├── events.py       # Event formatting + /news, weekly events
│   │   ├── news.py         # Քաղաքային news digest
│   │   └── recommend.py    # Location-based առաջարկներ (մինչև city-level)
│   │
│   └── utils/
│       ├── listings.py     # Ցանկերի, pagination-ի helpers
│       ├── logger.py       # Logging setup
│       ├── helpers.py      # Ընդհանուր small utilities
│       └── keyboards.py    # Inline / reply կոճակներ Telegram-ի համար
│
├── config/
│   ├── __init__.py
│   └── settings.py         # ENV-based config (tokens, DB, timezone և այլն)
│
├── templates/
│   ├── index.html          # Skeleton (դեռ դատարկ կամ նախնական)
│   └── dashboard.html      # Skeleton dashboard
│
├── data/                   # Runtime տվյալների / DB ֆայլի համար
│
├── .env                    # Local secrets (ignored from VCS)
├── .env.example            # Env փոփոխականների օրինակ
├── requirements.txt        # Python dependencies
├── Procfile                # Դեռ դատարկ՝ կարելի է լրացնել Heroku/Render commands-ով
├── render.yaml             # Render config (skeleton, պետք է լցնել ըստ ծառայության)
└── README.md               # Նախագծի փաստաթուղթ (այս ֆայլը)

Project overview
AskYerevan-ը Telegram բոտ է Երևանի համար․ ցույց է տալիս եղանակ, խցանումներ, Tomsarkgh-ից քաշած event-ներ (կինո, թատրոն, օպերա, փաբ/փարթի, այլ), և ունի scheduler, որը շաբաթվա ընթացքում ավտոմատ հրապարակումներ է անում։
