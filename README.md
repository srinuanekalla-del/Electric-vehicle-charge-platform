# EVCharge — EV Charging Platform (Full Stack)

Matches the exact user flow and database schema:

```
Home → Find Stations → Station Details → Select Charger →
Select Date & Time → Book Slot → Payment → Confirmation → Charging History
```

```
User → ChargingStation → Charger → Booking → Payment → ChargingHistory
```

## Tech Stack

- **Backend:** Python, Django, Django REST Framework, JWT auth
- **Database:** MySQL (default) — SQLite supported for quick local testing
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **API Docs:** Swagger UI at `/docs/`

## Project Structure

```
backend/
├── accounts/    # User model, register/login (JWT)
├── stations/    # ChargingStation, Charger models + APIs, seed command
├── bookings/    # Booking model — date/time, duration, price calc, overlap check
├── payments/    # Payment model — confirms booking, creates history entry
└── history/     # ChargingHistory model — read-only "Charging History" API

frontend/
├── index.html, signup.html, login.html
├── stations.html          # Find Charging Stations
├── station-detail.html    # Station Details + Select Charger
├── book.html               # Select Date & Time + Book Slot (live price estimate)
├── payment.html             # Booking summary + payment method + confirm
├── confirmation.html        # Booking Confirmation
├── bookings.html             # My Bookings (pay/cancel)
└── history.html               # Charging History
```

## How the flow works end-to-end

1. **Find Stations** (`stations.html`) — lists stations from the database, each
   showing a computed **Available/Busy** status based on its chargers.
2. **Station Details** (`station-detail.html`) — shows all chargers at that
   station with type, power, price/kWh, and status.
3. **Select Charger** — clicking an available charger goes to the booking page,
   carrying the charger's rate and power via the URL.
4. **Select Date & Time / Book Slot** (`book.html`) — pick date, start time,
   and duration. The estimated price updates live
   (`price_per_kwh × power_kw × hours`). Submitting creates a `Booking` with
   status `pending` — **the backend rejects overlapping bookings for the same
   charger**, this is the core business-logic feature.
5. **Payment** (`payment.html`) — shows the booking summary, lets you pick a
   payment method, and "Confirm Payment" creates a `Payment` row (simulated
   success — no real gateway), moves the `Booking` to `confirmed`, and
   automatically creates a `ChargingHistory` entry (`status: upcoming`).
6. **Booking Confirmation** (`confirmation.html`) — shows booking ID, station,
   charger, date/time, amount, and status.
7. **Charging History** (`history.html`) — lists all the user's sessions
   (upcoming/completed/cancelled) with energy consumed and amount paid.

## Setup — Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows

pip install -r requirements.txt
```

### Option A — Quick start with SQLite (no MySQL install needed)

A `.env` file is already included with `USE_SQLITE=True`, so this works
immediately:

```bash
python manage.py migrate
python manage.py seed_stations
python manage.py runserver
```

### Option B — Use MySQL (matches the project's intended stack)

1. Create a MySQL database:
   ```sql
   CREATE DATABASE evcharge_db;
   ```
2. Edit `.env` (copy from `.env.example` if needed):
   ```
   USE_SQLITE=False
   DB_NAME=evcharge_db
   DB_USER=root
   DB_PASSWORD=yourpassword
   DB_HOST=localhost
   DB_PORT=3306
   ```
3. Install the MySQL driver (needs MySQL dev headers on your machine):
   ```bash
   pip install mysqlclient
   ```
4. Run the same migrate/seed/runserver commands as above.

API runs at `http://127.0.0.1:8000/`. Swagger docs: `http://127.0.0.1:8000/docs/`

## Setup — Frontend

```bash
cd frontend
python -m http.server 5500
```
Open `http://127.0.0.1:5500/index.html`.

> `frontend/js/api.js` hardcodes the backend URL as `http://127.0.0.1:8000/api`
> — update this if your backend runs elsewhere.

## Key Design Notes

- **Booking conflict detection** compares the new booking's time range against
  all existing non-cancelled bookings for the same charger and date, rejecting
  any overlap — implemented in `bookings/serializers.py`.
- **Payment is simulated** (no real gateway) — on "success" it immediately
  confirms the booking and writes a `ChargingHistory` row. This is documented
  here rather than left unexplained, since there's no real hardware/gateway
  to integrate against in a portfolio-scope project.
- **Station "Available/Busy" status** is computed, not stored — a station is
  "Available" if at least one of its chargers has `status = available`.
