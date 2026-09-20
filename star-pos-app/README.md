# Star POS API

A fast, lightweight Point of Sale (POS) backend API built for Star Supermarket.
This system handles cashiers, product catalog inventory, shopping cart
checkouts, and payment tracking across multiple counters.

## Project Structure

```
pos_app/
└── app/
    ├── core/          # config (env settings) and security (JWT, hashing, role guards)
    ├── models/        # Database tables (SQLAlchemy)
    ├── schemas/       # Request/Response validation (Pydantic)
    ├── repositories/  # Database queries
    ├── services/      # Business logic & math calculations
    ├── routers/       # API endpoints (FastAPI Routes)
    ├── database.py    # Database connection setup
    └── main.py        # App entry point & automatic table creator
seed.py                # Demo admin/cashier + sample catalog data
tests/                 # Pytest suite (see "Running the tests" below)
.github/workflows/tests.yml  # CI: runs the suite on every push/PR
```

## How to Setup & Run Locally

**1. Install Dependencies**

```bash
pip install -r requirements.txt
```

**2. Configure Environment Variables**

Create a file named `.env` in the root folder and add your PostgreSQL
connection string, e.g.:

```
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/pos_db
SECRET_KEY=change-this-to-a-long-random-string
```

**3. (Optional) Seed demo data**

```bash
python seed.py
```

**4. Start the Server**

The application will automatically create all required database tables in
PostgreSQL on startup:

```bash
python -m uvicorn app.main:app --reload
```

## Testing the API

Open the interactive Swagger UI playground to try all endpoints:
**http://127.0.0.1:8000/docs**

**Available Modules:**
- Employee Management (`/users`) — register staff, log in, open counter shifts.
- Catalog Lookups (`/catalog`) — set up categories and suppliers.
- Inventory Control (`/products`) — add products, restock inventory, scan barcodes.
- Sales Checkout (`/sales`) — submit shopping carts and compute totals safely.
- Payments & Receipts (`/payments`) — process customer payments and look up receipts.

## Running the automated test suite locally

The test suite uses **pytest** with an isolated **in-memory SQLite** database —
it never touches whatever your `.env` points at (your real PostgreSQL dev
database). Every test function gets a fresh, empty set of tables, so tests
never leak state into one another and can run in any order.

```bash
pip install -r requirements-dev.txt   # app deps + pytest/httpx
pytest                                 # run the whole suite
pytest -v                              # verbose, one line per test
pytest tests/test_sales_and_payments.py  # just the checkout business-logic tests
```

Coverage, per major module (users/auth, catalog, products, sales, payments):
successful CRUD operations, validation errors (422), missing-resource errors
(404), permission errors (401/403), and the core checkout business rules —
stock deduction, tax/discount math, insufficient-stock rejection,
underpayment rejection, voiding a sale restoring stock, and receipt lookup.

## Continuous Integration

`.github/workflows/tests.yml` runs on every push and on every pull request
(opened or updated), on every branch. It checks out the repo, sets up
Python 3.12, installs `requirements-dev.txt`, and runs `pytest -v`. The
workflow — and the PR check / commit status — fails if any test fails.
There is no deployment step; this workflow is CI only.
