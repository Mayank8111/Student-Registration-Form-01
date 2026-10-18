from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional
import pyodbc

app = FastAPI(title="Student Registration API", version="1.0.0")

# Allow requests from your HTML files served via XAMPP
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Database connection ----------
def get_connection():
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=DESKTOP-K1O3CB1;"
        "DATABASE=StudentDB;"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(conn_str)


# ---------- Pydantic Models ----------
class StudentCreate(BaseModel):
    rol_no: str
    name: str
    email: EmailStr
    course: str

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    course: Optional[str] = None


# ---------- GET all students ----------
@app.get("/students")
def get_all_students():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT rol_no, name, email, course FROM studentdb")
        rows = cursor.fetchall()
        return [
            {"rol_no": r[0], "name": r[1], "email": r[2], "course": r[3]}
            for r in rows
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


# ---------- GET single student by roll number ----------
@app.get("/students/{rol_no}")
def get_student(rol_no: str):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT rol_no, name, email, course FROM studentdb WHERE rol_no = ?",
            (rol_no,)
        )
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail=f"Student '{rol_no}' not found")
        return {"rol_no": row[0], "name": row[1], "email": row[2], "course": row[3]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


# ---------- POST create new student ----------
@app.post("/students", status_code=201)
def create_student(student: StudentCreate):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO studentdb (rol_no, name, email, course) VALUES (?, ?, ?, ?)",
            (student.rol_no, student.name, student.email, student.course)
        )
        conn.commit()
        return {"message": "Student registered successfully", "rol_no": student.rol_no}
    except pyodbc.IntegrityError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


# ---------- PUT update existing student ----------
@app.put("/students/{rol_no}")
def update_student(rol_no: str, student: StudentUpdate):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Build update query dynamically based on what fields were sent
        fields = []
        values = []
        if student.name is not None:
            fields.append("name = ?")
            values.append(student.name)
        if student.email is not None:
            fields.append("email = ?")
            values.append(student.email)
        if student.course is not None:
            fields.append("course = ?")
            values.append(student.course)

        if not fields:
            raise HTTPException(status_code=400, detail="No fields provided to update")

        values.append(rol_no)
        sql = f"UPDATE studentdb SET {', '.join(fields)} WHERE rol_no = ?"
        cursor.execute(sql, values)

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Student '{rol_no}' not found")

        conn.commit()
        return {"message": f"Student '{rol_no}' updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()


# ---------- DELETE student ----------
@app.delete("/students/{rol_no}")
def delete_student(rol_no: str):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM studentdb WHERE rol_no = ?", (rol_no,))

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Student '{rol_no}' not found")

        conn.commit()
        return {"message": f"Student '{rol_no}' deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()
