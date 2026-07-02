from datetime import date
from database import query
from components import page_head, crud

def page_attendance():
    page_head("Attendance", "Manage student attendance records")
    ens = query(
        """SELECT e.enrollment_id,
                  CONCAT(s.first_name,' ',s.last_name) AS student,
                  c.course_code
           FROM enrollments e
           JOIN students s ON e.student_id = s.student_id
           JOIN courses c ON e.course_id = c.course_id
           ORDER BY e.enrollment_id"""
    )
    e_raw = [str(e["enrollment_id"]) for e in ens] if ens else []
    e_lbl = (
        [f"{e['enrollment_id']} -- {e['student']} ({e['course_code']})"
         for e in ens]
        if ens else []
    )

    crud(
        table="attendance",
        cols=[
            "attendance_id", "enrollment_id",
            "attendance_date", "attendance_status",
        ],
        headers=["Attendance ID", "Enrollment ID", "Date", "Status"],
        pk="attendance_id",
        pk_range=(710000, 799999),
        fields=[
            {"name": "enrollment_id", "label": "Enrollment",
             "type": "select", "options": e_raw, "option_labels": e_lbl},
            {"name": "attendance_date", "label": "Attendance Date", "type": "date",
             "min_date": date(2001, 1, 1), "max_date": date.today()},
            {"name": "attendance_status", "label": "Status",
             "type": "select",
             "options": ["Absent", "Present", "Late", "Excused"]},
        ],
        search_cols=["attendance_id", "enrollment_id", "attendance_status"],
        select_label_fn=lambda r: (
            f"{r['attendance_id']}  --  Enrollment {r['enrollment_id']}: "
            f"{r['attendance_status']} on {r['attendance_date']}"
        ),
    )
