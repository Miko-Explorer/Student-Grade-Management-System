import streamlit as st
from datetime import date

from database import query
from components import page_head, crud


def page_grades():
    page_head("Grades", "Manage student grade records")

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
        table="grades",
        cols=[
            "grade_id", "enrollment_id", "grade_letter",
            "grade_percentage", "grade_date",
        ],
        headers=[
            "Grade ID", "Enrollment ID", "Letter", "Percentage", "Date",
        ],
        pk="grade_id",
        pk_range=(610000, 699999),
        fields=[
            {"name": "enrollment_id", "label": "Enrollment",
             "type": "select", "options": e_raw, "option_labels": e_lbl},
            {"name": "grade_letter", "label": "Letter Grade",
             "type": "select", "options": ["A", "B", "C", "D", "F"]},
            {"name": "grade_percentage", "label": "Percentage",
             "type": "decimal", "min": 50.0, "max": 99.9,
             "step": 0.1, "fmt": "%.1f"},
            {"name": "grade_date", "label": "Grade Date", "type": "date",
             "min_date": date(2001, 1, 1), "max_date": date.today()},
        ],
        search_cols=["grade_id", "enrollment_id", "grade_letter"],
        select_label_fn=lambda r: (
            f"{r['grade_id']}  --  Enrollment {r['enrollment_id']}: "
            f"{r['grade_letter']} ({r['grade_percentage']}%)"
        ),
    )
