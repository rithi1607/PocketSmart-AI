# PocketSmart AI

PocketSmart AI is a FastAPI-based AI budget and recommendation assistant.

It supports:

- Home Interior Planning
- Party Budget Planning
- Jewelry Recommendations
- Optional jewelry outfit image upload
- Gemini AI integration
- Mock AI mode
- User registration
- User login
- JWT authentication
- Recommendation history
- SQLite database
- Responsive web interface


## Project Structure

```text
PocketSmart_AI/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── recommendations.py
│   │   ├── history.py
│   │   └── session.py
│   │
│   ├── services/
│   │   ├── gemini.py
│   │   ├── mock_ai.py
│   │   └── recommendations.py
│   │
│   ├── templates/
│   │
│   └── static/
│
├── tests/
├── uploads/
├── requirements.txt
├── .env.example
├── run.py
└── README.md