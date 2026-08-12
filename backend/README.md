# Argus Backend

This is the production backend for Argus.

## Structure

```
backend/
├── app/
│   ├── core/        Global configuration
│   ├── retrieval/   Document retrieval logic
│   ├── routes/      FastAPI endpoints
│   ├── schemas/     Pydantic models
│   ├── services/    Business logic
│   ├── __init__.py
│   └── main.py      Application entry point
│
├── tests/           Unit and integration tests
├── data/            Raw, processed, and indexed data
├── notebooks/       Experiments (not production)
├── pyproject.toml   Python project configuration
└── README.md        This file
```

## Setup

1. Install dependencies:
   ```bash
   cd backend
   pip install -e .
   ```

2. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

3. Visit `http://localhost:8000/docs` for API documentation.

## Development

- Add production code to `app/`
- Add tests to `tests/`
- Use `notebooks/` only for experiments
- Store data in `data/` (not committed to Git)
