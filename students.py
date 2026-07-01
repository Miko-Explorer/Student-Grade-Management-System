import streamlit as st
from datetime import date

from database import query
from components import page_head, crud


def page_students():
    page_head("Students", "Manage student information records")
    crud(
        table="students",
        cols=[
            "student_id", "user_id", "first_name", "last_name",
            "email", "phone", "date_of_birth",
        ],
        headers=[
            "Student ID", "User ID", "First Name", "Last Name",
            "Email", "Phone", "Date of Birth",
        ],
        pk="student_id",
        pk_range=(110000, 199999),
        fields=[
            {"name": "user_id", "label": "User ID",
             "type": "number", "min": 210000, "max": 299999},
            {"name": "first_name", "label": "First Name", "type": "text"},
            {"name": "last_name", "label": "Last Name", "type": "text"},
            {"name": "email", "label": "School Email", "type": "text"},
            {"name": "phone", "label": "Phone Number", "type": "text"},
            {"name": "date_of_birth", "label": "Date of Birth", "type": "date",
             "min_date": date(1956, 1, 1), "max_date": date(2010, 12, 31),
             "default": date(2000, 1, 1)},
        ],
        search_cols=["student_id", "first_name", "last_name", "email", "phone"],
        select_label_fn=lambda r: (
            f"{r['student_id']}  --  {r['first_name']} {r['last_name']}"
        ),
    )
