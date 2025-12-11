ask-yerevan/
  backend/
    __init__.py
    bot.py              # Telegram բոտի հիմնական entrypoint-ը (polling)
    scheduler.py        # APScheduler runner, առավոտյան fixed job-ներ
    web_app.py          # FastAPI web service + healthcheck
    database.py         # SQLite connection + tables + helpers
    jobs.py             # scheduler job ֆունկցիաներ (weather, traffic, events...)
    languages.py        # HY/RU/EN տեքստեր, gettext helper
    utils/
      __init__.py
      logger.py         # logging setup
      helpers.py        # փոքր ընդհանուր օգնականներ
      keyboards.py      # inline / reply keyboard builders
      listings.py       # classified listings detection + DB helpers
    ai/
      __init__.py
      response.py       # generatereply + Perplexity ինտեգրացիա
      humor.py          # get_humor_advice և այլն (եթե օգտագործվում է)
    armenia/
      __init__.py
      weather.py        # OpenWeather API wrapper + եղանակի մեսեջ
      traffic.py        # Google Directions / խցանումներ
      events_sources.py # Tomsarkgh scraper-ներ (cinema/theatre/opera/party/festival)
      events.py         # get_week_premiere, get_next_day_films_and_plays,
                        # get_events_by_category, get_festival_events_7days
      recommend.py      # location-based recommendation logic (եթե ակտիվ է)
      news.py           # (այժմ դատարկ, ապագա news RSS API)
    config/
      __init__.py
      settings.py       # env config: BOTTOKEN, DB_PATH, TIMEZONE, API keys
    templates/
      index.html        # ապագա web dashboard template (հիմա կարա մնա դատարկ)
      dashboard.html
    data/
      askyerevan.db     # SQLite runtime DB (production-ում ստեղծվում է initdb-ով)
  .env.example          # env բանալիների օրինակ
  Procfile              # optional (եթե Render-ում չի օգտագործվում, մնում է placeholder)
  render.yaml           # optional Render IaC (կարող է մնալ դատարկ մինչև լրացնելը)
  requirements.txt
  README.md
