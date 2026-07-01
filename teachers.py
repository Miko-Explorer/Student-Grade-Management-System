import streamlit as st
from datetime import date

from database import query
from components import page_head, crud


def page_teachers():
    page_head("Teachers", "Manage teacher information records")
    crud(
        table="teachers",
        cols=[
            "teacher_id", "user_id", "first_name", "last_name",
            "email", "phone", "hire_date",
        ],
        headers=[
            "Teacher ID", "User ID", "First Name", "Last Name",
            "Email", "Phone", "Hire Date",
        ],
        pk="teacher_id",
        pk_range=(310000, 399999),
        fields=[
            {"name": "user_id", "label": "User ID",
             "type": "number", "min": 210000, "max": 299999},
            {"name": "first_name", "label": "First Name", "type": "text"},
            {"name": "last_name", "label": "Last Name", "type": "text"},
            {"name": "email", "label": "School Email", "type": "text"},
            {"name": "phone", "label": "Phone Number", "type": "text"},
            {"name": "hire_date", "label": "Hire Date", "type": "date",
             "min_date": date(1970, 1, 1), "max_date": date.today()},
        ],
        search_cols=["teacher_id", "first_name", "last_name", "email", "phone"],
        select_label_fn=lambda r: (
            f"{r['teacher_id']}  --  {r['first_name']} {r['last_name']}"
        ),
    )
