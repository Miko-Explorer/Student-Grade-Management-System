from database import query
from components import page_head, crud

def page_courses():
    page_head("Courses", "Manage course records")

    teachers = query(
        "SELECT teacher_id, CONCAT(first_name,' ',last_name) AS n "
        "FROM teachers ORDER BY teacher_id"
    )
    t_raw = [str(t["teacher_id"]) for t in teachers] if teachers else []
    t_lbl = [f"{t['teacher_id']} -- {t['n']}" for t in teachers] if teachers else []

    crud(
        table="courses",
        cols=[
            "course_id", "course_code", "course_name",
            "units", "teacher_id", "semester",
        ],
        headers=[
            "Course ID", "Code", "Name", "Units", "Teacher ID", "Semester",
        ],
        pk="course_id",
        pk_range=(410000, 499999),
        fields=[
            {"name": "course_code", "label": "Course Code", "type": "text"},
            {"name": "course_name", "label": "Course Name", "type": "text"},
            {"name": "units", "label": "Units",
             "type": "number", "min": 1, "max": 6},
            {"name": "teacher_id", "label": "Teacher",
             "type": "select", "options": t_raw, "option_labels": t_lbl},
            {"name": "semester", "label": "Semester",
             "type": "select", "options": ["1st", "2nd", "3rd"]},
        ],
        search_cols=["course_id", "course_code", "course_name", "semester"],
        select_label_fn=lambda r: (
            f"{r['course_id']}  --  {r['course_code']}  {r['course_name']}"
        ),
    )
