import streamlit as st
import pandas as pd

from database import query
from components import inject_css, hr, stat_card, sec_title, page_head, logo

from students import page_students
from teachers import page_teachers
from courses import page_courses
from enrollments import page_enrollments
from grades import page_grades
from attendance import page_attendance
from users import page_users


def page_dashboard():
    page_head("Dashboard", "System overview and key metrics")

    counts = {}
    for tbl in ["students", "teachers", "courses", "enrollments", "grades"]:
        r = query(f"SELECT COUNT(*) AS c FROM {tbl}")
        counts[tbl] = r[0]["c"] if r else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: stat_card(counts["students"], "Students")
    with c2: stat_card(counts["teachers"], "Teachers")
    with c3: stat_card(counts["courses"], "Courses")
    with c4: stat_card(counts["enrollments"], "Enrollments")
    with c5: stat_card(counts["grades"], "Grades")

    hr()
    lc, rc = st.columns(2)

    with lc:
        sec_title("Recent Enrollments")
        data = query(
            """SELECT e.enrollment_id, CONCAT(s.first_name,' ',s.last_name) AS Student,
                       c.course_code AS Course, e.enrollment_status AS Status,
                       e.enrollment_date AS Date
                FROM enrollments e
                JOIN students s ON e.student_id = s.student_id
                JOIN courses c ON e.course_id = c.course_id
                ORDER BY e.enrollment_date DESC LIMIT 6"""
        )
        if data:
            st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True, height=270)
        else:
            st.info("No enrollments yet.")

    with rc:
        sec_title("Recent Grades")
        data = query(
            """SELECT g.grade_id, CONCAT(s.first_name,' ',s.last_name) AS Student,
                       c.course_code AS Course, g.grade_letter AS Letter,
                       g.grade_percentage AS Percentage, g.grade_date AS Date
                FROM grades g
                JOIN enrollments e ON g.enrollment_id = e.enrollment_id
                JOIN students s ON e.student_id = s.student_id
                JOIN courses c ON e.course_id = c.course_id
                ORDER BY g.grade_date DESC LIMIT 6"""
        )
        if data:
            st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True, height=270)
        else:
            st.info("No grades recorded yet.")


def page_reports():
    page_head("Report Cards", "View student report card details and summaries")

    sts = query(
        "SELECT student_id, CONCAT(first_name,' ',last_name) AS n "
        "FROM students ORDER BY student_id"
    )
    s_map = {str(s["student_id"]): s["n"] for s in sts} if sts else {}
    s_labels = ["All Students"] + [
        f"{sid} -- {s_map[sid]}" for sid in s_map
    ]

    sel = st.selectbox("Filter by Student", s_labels, key="rc_filter")
    sel_id = None if sel == "All Students" else sel.split(" -- ")[0]

    tab1, tab2 = st.tabs(["Report Card Details", "Summary"])

    with tab1:
        if sel_id:
            data = query(
                "SELECT * FROM final_report_card_summary "
                "WHERE Student_ID=%s ORDER BY Semester, Course_Code",
                (int(sel_id),),
            )
        else:
            data = query(
                "SELECT * FROM final_report_card_summary "
                "ORDER BY Student_ID, Semester, Course_Code"
            )
        if data:
            st.dataframe(
                pd.DataFrame(data), use_container_width=True,
                hide_index=True, height=420,
            )
            st.markdown(
                f"<p style='color:#94a3b8;font-size:0.78rem;margin-top:6px;'>"
                f"{len(data)} record(s)</p>",
                unsafe_allow_html=True,
            )
        else:
            st.info("No report card data available.")

    with tab2:
        if sel_id:
            data = query(
                "SELECT * FROM report_card_summary "
                "WHERE Student_ID=%s ORDER BY Semester",
                (int(sel_id),),
            )
        else:
            data = query(
                "SELECT * FROM report_card_summary "
                "ORDER BY Student_ID, Semester"
            )
        if data:
            st.dataframe(
                pd.DataFrame(data), use_container_width=True,
                hide_index=True, height=420,
            )
        else:
            st.info("No summary data available.")


def main():
    st.set_page_config(
        page_title="GradeVault",
        page_icon="",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_css()

    with st.sidebar:
        logo()
        page = st.radio(
            "Navigation",
            [
                "Dashboard", "Students", "Teachers", "Courses",
                "Enrollments", "Grades", "Attendance", "Users",
                "Report Cards",
            ],
            label_visibility="collapsed",
        )
        hr()
        st.markdown(
            '<p style="color:#94a3b8;font-size:0.72rem;text-align:center;">'
            'GradeVault v1.0</p>',
            unsafe_allow_html=True,
        )

    routes = {
        "Dashboard": page_dashboard,
        "Students": page_students,
        "Teachers": page_teachers,
        "Courses": page_courses,
        "Enrollments": page_enrollments,
        "Grades": page_grades,
        "Attendance": page_attendance,
        "Users": page_users,
        "Report Cards": page_reports,
    }
    routes[page]()


if __name__ == "__main__":
    main()
