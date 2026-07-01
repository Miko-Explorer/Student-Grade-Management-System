import streamlit as st
from datetime import date

from database import query
from components import page_head, crud


def page_enrollments():
    page_head("Enrollments", "Manage student course enrollments")

    sts = query(
        "SELECT student_id, CONCAT(first_name,' ',last_name) AS n "
        "FROM students ORDER BY student_id"
    )
    s_raw = [str(s["student_id"]) for s in sts] if sts else []
    s_lbl = [f"{s['student_id']} -- {s['n']}" for s in sts] if sts else []

    crs = query("SELECT course_id, course_code FROM courses ORDER BY course_id")
    c_raw = [str(c["course_id"]) for c in crs] if crs else []
    c_lbl = [f"{c['course_id']} -- {c['course_code']}" for c in crs] if crs else []

    crud(
        table="enrollments",
        cols=[
            "enrollment_id", "student_id", "course_id",
            "enrollment_date", "enrollment_status",
        ],
        headers=[
            "Enrollment ID", "Student ID", "Course ID", "Date", "Status",
        ],
        pk="enrollment_id",
        pk_range=(510000, 599999),
        fields=[
            {"name": "student_id", "label": "Student",
             "type": "select", "options": s_raw, "option_labels": s_lbl},
            {"name": "course_id", "label": "Course",
             "type": "select", "options": c_raw, "option_labels": c_lbl},
            {"name": "enrollment_date", "label": "Enrollment Date", "type": "date",
             "min_date": date(2001, 1, 1), "max_date": date.today()},
            {"name": "enrollment_status", "label": "Status",
             "type": "select",
             "options": ["Enrolled", "Completed", "Dropped", "On hold"]},
        ],
        search_cols=["enrollment_id", "student_id", "course_id",
                     "enrollment_status"],
        select_label_fn=lambda r: (
            f"{r['enrollment_id']}  --  Student {r['student_id']}, "
            f"Course {r['course_id']}"
        ),
    )
