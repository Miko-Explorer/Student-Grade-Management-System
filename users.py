import streamlit as st
import pandas as pd

from database import query
from components import page_head, hr


def page_users():
    page_head("Users", "Manage system user accounts")

    sc1, sc2 = st.columns([4, 1])
    with sc1:
        term = st.text_input("Search", placeholder="Type to filter...",
                             key="srch_users")
    with sc2:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        if st.button("Add New", type="primary", use_container_width=True,
                     key="add_users"):
            st.session_state["form_users"] = {"mode": "add"}
            st.rerun()

    all_rows = query(
        "SELECT user_id, username, passwords, roles FROM users ORDER BY user_id"
    )
    if term:
        rows = [
            r for r in (all_rows or [])
            if term.lower() in str(r["user_id"]).lower()
            or term.lower() in r["username"].lower()
            or term.lower() in r["roles"].lower()
        ]
    else:
        rows = all_rows or []

    if rows:
        df = pd.DataFrame(rows)
        df.columns = ["User ID", "Username", "Password", "Role"]
        st.dataframe(df, use_container_width=True, hide_index=True, height=340)
        st.markdown(
            f"<p style='color:#94a3b8;font-size:0.78rem;margin-top:6px;'>"
            f"{len(rows)} record(s)</p>",
            unsafe_allow_html=True,
        )

        opts = {
            f"{r['user_id']}  --  {r['username']} ({r['roles']})": r["user_id"]
            for r in rows
        }
        hr()
        ec1, ec2, ec3 = st.columns([3, 1, 1])
        with ec1:
            sel = st.selectbox("Select record", ["--"] + list(opts.keys()),
                               key="sel_users")
        with ec2:
            if st.button("Edit", use_container_width=True, key="edit_users",
                         disabled=(sel == "--")):
                full = query("SELECT * FROM users WHERE user_id=%s",
                             (opts[sel],))
                if full:
                    st.session_state["form_users"] = {
                        "mode": "edit", "id": opts[sel], "data": full[0],
                    }
                    st.rerun()
        with ec3:
            if st.button("Delete", use_container_width=True, key="del_users",
                         disabled=(sel == "--")):
                st.session_state["del_cf_users"] = opts[sel]
                st.rerun()

        del_id = st.session_state.get("del_cf_users")
        if del_id is not None:
            dc1, dc2, dc3 = st.columns([3, 1, 1])
            with dc1:
                st.warning(f"Confirm delete user_id = {del_id}?")
            with dc2:
                if st.button("Confirm", type="primary",
                             use_container_width=True, key="del_y_users"):
                    query("DELETE FROM users WHERE user_id=%s",
                          (del_id,), fetch=False)
                    st.session_state.pop("del_cf_users", None)
                    st.success("User deleted.")
                    st.rerun()
            with dc3:
                if st.button("Cancel", use_container_width=True,
                             key="del_n_users"):
                    st.session_state.pop("del_cf_users", None)
                    st.rerun()
    else:
        st.info("No users found.")

    form_state = st.session_state.get("form_users")
    if form_state:
        edit_mode = form_state["mode"] == "edit"
        d = form_state.get("data", {})

        with st.expander(
            f"{'Edit' if edit_mode else 'Add New'} User", expanded=True
        ):
            g = st.columns(2)
            with g[0]:
                uname = st.text_input(
                    "Username",
                    value=d.get("username", "") if edit_mode else "",
                    key="f_users_username",
                )
            with g[1]:
                pwd = st.text_input(
                    "Password",
                    value=d.get("passwords", "") if edit_mode else "",
                    key="f_users_passwords",
                )
            with g[0]:
                role = st.selectbox(
                    "Role", ["Student", "Teacher", "Admin"],
                    index=(["Student", "Teacher", "Admin"].index(
                        d.get("roles", "Student")) if edit_mode else 0),
                    key="f_users_roles",
                )
            hr()
            bc1, bc2 = st.columns(2)
            with bc1:
                if st.button("Save", type="primary", use_container_width=True,
                             key="save_users"):
                    if edit_mode:
                        query(
                            "UPDATE users SET username=%s, passwords=%s, "
                            "roles=%s WHERE user_id=%s",
                            (uname, pwd, role, form_state["id"]),
                            fetch=False,
                        )
                    else:
                        mx = query("SELECT MAX(user_id) AS m FROM users")
                        nid = ((mx[0]["m"] if mx and mx[0]["m"]
                                else 209999) + 1)
                        if nid > 299999:
                            st.error("User ID range exhausted.")
                            return
                        query(
                            "INSERT INTO users (user_id, username, passwords, "
                            "roles) VALUES (%s,%s,%s,%s)",
                            (nid, uname, pwd, role),
                            fetch=False,
                        )
                    st.success(
                        f"User {'updated' if edit_mode else 'created'}."
                    )
                    st.session_state.pop("form_users", None)
                    st.rerun()
            with bc2:
                if st.button("Cancel", use_container_width=True,
                             key="cancel_users"):
                    st.session_state.pop("form_users", None)
                    st.rerun()
