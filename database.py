import streamlit as st
import mysql.connector
from mysql.connector import Error


def get_connection():
    try:
        return mysql.connector.connect(
            host=st.secrets.get("db_host", "localhost"),
            user=st.secrets.get("db_user", "root"),
            password=st.secrets.get("db_password", "miko1605"),
            database=st.secrets.get("db_name", "student_db"),
        )
    except Error as e:
        st.error(f"Database connection failed: {e}")
        return None


def query(sql, params=None, fetch=True):
    conn = get_connection()
    if not conn:
        return [] if fetch else None
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params or ())
        if fetch:
            result = cur.fetchall()
        else:
            conn.commit()
            result = cur.lastrowid
        cur.close()
        conn.close()
        return result
    except Error as e:
        st.error(f"Query error: {e}")
        if not fetch:
            conn.rollback()
        cur.close()
        conn.close()
        return [] if fetch else None
