# Vehicle Service (FastAPI + sqlite3)

Simple CRUD web service for vehicles using Python's built-in sqlite3 module.

## Schema

Table `vehicles`:
- vin (TEXT, primary key) — unique, stored uppercase (case-insensitive uniqueness)
- manufacturer (TEXT)
- description (TEXT)
- horse_power (INTEGER)
- model_name (TEXT)
- model_year (INTEGER)
- purchase_price (REAL)
- fuel_type (TEXT)

## Quickstart (Windows / macOS / Linux)

```bash
python -m venv .venv
# activate:
# macOS / Linux:
source .venv/bin/activate
# Windows PowerShell:
.venv\Scripts\activate

pip install -r requirements.txt
uvicorn main:app --reload
```

Open http://127.0.0.1:8000/docs for interactive API docs.

## API Endpoints

- `GET /vehicle` - list all vehicles (200)
- `POST /vehicle` - create vehicle (201) — body must be valid JSON; malformed JSON => 400; invalid fields => 422
- `GET /vehicle/{vin}` - retrieve vehicle by VIN (case-insensitive) (200)
- `PUT /vehicle/{vin}` - update vehicle fields (200)
- `DELETE /vehicle/{vin}` - delete vehicle (204)

## Tests

```bash
pytest
```

## Notes

- VIN uniqueness is enforced case-insensitively by storing VINs uppercased on insert and checking with UPPER() queries.
- Validation handled by Pydantic: malformed JSON => 400; schema violations => 422.
