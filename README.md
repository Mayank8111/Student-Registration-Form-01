# Student Registration Form

A student registration and search system built with FastAPI and SQL Server, with HTML frontends served via XAMPP/Apache.

## Tech Stack

- **Backend:** FastAPI (Python) with full CRUD operations (GET, POST, PUT, DELETE)
- **Frontend:** HTML + JavaScript (fetch API)
- **Database:** Microsoft SQL Server (StudentDB)
- **Server:** Uvicorn (API on port 8000) + Apache/XAMPP (HTML files)

## Project Structure

```
├── main.py             # FastAPI backend with all endpoints
├── Student_form.html   # Registration form (POST)
├── search.html         # Search form (GET)
├── delete.html         # Delete form (DELETE)
├── index.css           # Styles
└── trial01.py          # Experimental scripts
```

## API Endpoints

| Method   | Endpoint              | Description            |
|----------|-----------------------|------------------------|
| `GET`    | `/students`           | Get all students       |
| `GET`    | `/students/{rol_no}`  | Get a student by roll number |
| `POST`   | `/students`           | Register a new student |
| `PUT`    | `/students/{rol_no}`  | Update a student       |
| `DELETE` | `/students/{rol_no}`  | Delete a student       |

Interactive API docs are available at `http://localhost:8000/docs` when the server is running.

## How to Run

### 1. Start the FastAPI server

```powershell
pip install "fastapi[all]" pyodbc
uvicorn main:app --reload --port 8000
```

### 2. Serve the HTML files

Place the project folder in `C:\xampp\htdocs\` and start Apache via XAMPP Control Panel.

### 3. Open the forms in your browser

- Registration: `http://localhost/form_POST/Student_form.html`
- Search: `http://localhost/form_POST/search.html`
- Delete: `http://localhost/form_POST/delete.html`
- API Docs: `http://localhost:8000/docs`

## Database Setup

The app connects to SQL Server using Windows Authentication. Update the connection string in `main.py` if your server name or database name is different:

```python
def get_connection():
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=DESKTOP-K1O3CB1;"
        "DATABASE=StudentDB;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str)
```

Create the table in SQL Server:

```sql
CREATE TABLE studentdb (
    rol_no  VARCHAR(50)  NOT NULL PRIMARY KEY,
    name    VARCHAR(100) NOT NULL,
    email   VARCHAR(100) NOT NULL,
    course  VARCHAR(100)
);
```
