# Velora — Fashion Rental Platform

> **Velora** — *Rent the Look. Live the Moment.*
> An online fashion rental marketplace where customers rent clothing, accessories and event outfits, and sellers earn by sharing their wardrobe.

Built with **Django 5**, **SQLite**, and **SSLCommerz** for payments. All packages are installed inside the project `venv` — nothing leaks into your global Python.

---

## Project layout

```
project/
├── venv/                     # virtual environment (dependencies live here ONLY)
├── velora/                   # Django project (settings, root URLs)
├── accounts/                 # Custom User (customer / seller roles) + auth views
├── shop/                     # Products, categories, listing & detail pages
├── rentals/                  # Booking flow, status workflow
├── payments/                 # SSLCommerz init / success / fail / cancel / IPN
├── reviews/                  # Ratings & comments
├── templates/                # Global templates (base.html etc.)
├── static/                   # CSS / images
├── media/                    # User uploads (product images, avatars)
├── db.sqlite3                # Built-in database (auto-created on first migrate)
├── manage.py
├── requirements.txt
├── .env                      # Local config (copy of .env.example)
└── .env.example
```

---

## First-time setup

> Run every command from the project root with the venv activated.

```powershell
# 1. Activate the virtual environment
.\venv\Scripts\Activate.ps1

# 2. Install all dependencies INTO THE VENV ONLY
pip install -r requirements.txt

# 3. Apply database migrations (SQLite is created automatically)
python manage.py migrate

# 4. (Optional) Seed starter categories
python manage.py seed_velora

# 5. Create an admin / superuser
python manage.py createsuperuser
```

---

## Running the project

```powershell
python manage.py runserver
```

Then open:
- Customer site: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

Use the superuser you created (or sign up as a new customer/seller from the UI).

---

## Where to change what

| You want to change… | File |
|---|---|
| Brand colors, fonts, hero styling | `static/css/velora.css` |
| Logo / favicon | `static/img/favicon.svg`, `static/img/placeholder.svg` |
| Site title / tagline | `templates/base.html` |
| Email & secret key | `.env` (copy from `.env.example`) |
| SSLCommerz sandbox / live keys | `.env` — `SSLCOMMERZ_STORE_ID`, `SSLCOMMERZ_STORE_PASSWD`, `SSLCOMMERZ_IS_SANDBOX` |
| Allowed hosts / debug flag | `.env` |
| Database (currently SQLite) | `velora/settings.py` → `DATABASES` |
| Currency | `.env` → `SSLCOMMERZ_CURRENCY` (default `BDT`) |
| Rental status flow / roles | `rentals/models.py`, `rentals/views.py` |
| Product fields | `shop/models.py` |

---

## SSLCommerz integration

The project uses the `sslcommerz-lib` Python package.

1. Sign up at https://developer.sslcommerz.com/ and get your **Store ID** + **Store Password**.
2. Open `.env` and fill in:
   ```
   SSLCOMMERZ_STORE_ID=your_real_store_id
   SSLCOMMERZ_STORE_PASSWD=your_real_store_password
   SSLCOMMERZ_IS_SANDBOX=True     # set False in production
   ```
3. The success / fail / cancel URLs are auto-built from `request.build_absolute_uri()` in `payments/views.py` — they point to:
   - `/payments/success/`
   - `/payments/fail/`
   - `/payments/cancel/`
   - `/payments/ipn/` (server-to-server validation)

You can test end-to-end with SSLCommerz sandbox cards from the developer dashboard.

---

## User roles

- **Customer** — browses the wardrobe, books outfits, pays via SSLCommerz, reviews items.
- **Seller** — lists fashion items, approves/rejects rental requests, manages the lifecycle (active → returned → completed).
- Switch your role from `/accounts/profile/` or pick a role when signing up.

---

## Common commands cheat-sheet

```powershell
# Activate venv
.\venv\Scripts\Activate.ps1

# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Seed starter categories
python manage.py seed_velora

# Run the development server
python manage.py runserver

# Collect static files (for production)
python manage.py collectstatic
```

---

## Production notes (for later)

When you go live, edit `.env`:
```
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DJANGO_SECRET_KEY=a-very-long-random-string
SSLCOMMERZ_IS_SANDBOX=False
```
…and serve with Gunicorn + Nginx. SQLite is fine for small projects; switch to PostgreSQL by editing `velora/settings.py` → `DATABASES`.

— Velora © 2026 · Crafted with Django · Secured by SSLCommerz