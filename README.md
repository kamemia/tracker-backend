# Getting Started

## Prerequisites

- Python 3.10+
- PostgreSQL
- Git

## Setup

1. Clone the repository and enter the project directory:

```bash
   git clone https://github.com/kamemia/tracker-backend.git
   cd tracker-backend
```

2. Create and activate the virtual environment:

```bash
   python -m venv .venv

   # Windows (PowerShell)
   .venv\Scripts\activate

   # macOS / Linux
   source .venv/bin/activate
```

3. Install dependencies:

```bash
   pip install -r requirements.txt
```

4. Copy the example env file and fill in your values:

```bash
   # macOS / Linux
   cp .env.example .env

   # Windows (PowerShell)
   copy .env.example .env
```

5. Apply migrations:

```bash
   python manage.py migrate
```

6. Start the development server:

```bash
   python manage.py runserver
```

   The API is available at http://127.0.0.1:8000/.

## Running Tests

```bash
python manage.py test
```

The tests cover ticket creation, the status filter with pagination, status updates via PATCH, and the stats endpoint.

## API Endpoints

| Method | Endpoint             | Description                                                |
| ------ | -------------------- | ---------------------------------------------------------- |
| POST   | `/api/tickets/`           | Create a ticket                                            |
| GET    | `/tickets/`           | List tickets (`?status=`, `?page=`, `?page_size=`)             |
| PATCH  | `/tickets/:id/`       | Update a ticket's status or priority                       |
| GET    | `/tickets/stats/`     | Count of tickets grouped by status                         |

## Decisions & Tradeoffs

### Backend

- **Viewset:** Plain `ModelViewSet` with a small `get_queryset` override for the `?status=` filter. This keeps the backend short, but it also exposes PUT, DELETE and retrieve endpoints the spec doesn't ask for.
- **Filtering:** Done by hand instead of with `django-filter`, so an invalid status returns an empty list rather than a 400.
- **Pagination:** Page-number based, with a `page_size` parameter to match the spec, capped at 100.
- **Indexing:** Composite index on `(status, -created_at)` to serve the filtered list and the stats query.
- **Stats:** The endpoint always returns every status, including zero counts, so the frontend cards never handle missing keys.
- **Security:** No authentication or permission layer.

### Frontend

- **Vuetify:** Used for the UI so I could rely on ready-made components (data table, dialog, menu, chips, select) instead of building and styling them myself. This sped up development and keeps the look consistent, at the cost of a larger bundle and less control over custom styling.
- **Server-side table:** `v-data-table-server` delegates pagination to the API, so the client never loads the full ticket list.
- **Single dialog:** One `TicketDialog` component handles both create and edit, decided by whether a ticket is passed in. This avoids duplicated form code.
- **Quick status change:** Status chips in the table open a menu that sends a PATCH with only the status, so a full edit dialog isn't needed for the most common change.
- **Data flow:** Stat cards and table are refetched after every create or update instead of updating local state. This is simpler but costs an extra request.
- **Error handling:** Errors are only logged to the console, with no user-facing messages.

### With more time

- Validate the status filter and return a 400 on invalid values.
- Restrict the viewset to the required methods.
- Add frontend tests.
- Show error toasts on the frontend.
- Work more on the visual aspect of the UI, not bare visuals as is.
- Work on the system architecture aspect, consider building things to scale.
- Create probably load test, setup metrics and monitoring tools