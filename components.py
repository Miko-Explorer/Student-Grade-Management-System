import streamlit as st
import pandas as pd
from datetime import date

from database import query


def inject_css():
    st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="stApp"] { font-family: 'Inter', system-ui, sans-serif; }
    @keyframes drift {
        0% { background-position: 0% 0%; }
        50% { background-position: 100% 100%; }
        100% { background-position: 0% 0%; }
    }
    .stApp {
        background:
            radial-gradient(ellipse at 15% 10%, rgba(25,55,120,0.2) 0%, transparent 50%),
            radial-gradient(ellipse at 85% 20%, rgba(20,45,100,0.15) 0%, transparent 45%),
            radial-gradient(ellipse at 50% 80%, rgba(15,40,90,0.12) 0%, transparent 50%),
            radial-gradient(ellipse at 90% 90%, rgba(30,65,130,0.18) 0%, transparent 40%),
            linear-gradient(145deg, #121212 0%, #1a1a1a 35%, #222222 70%, #1e1e1e 100%);
        background-attachment: fixed;
        background-size: 200% 200%;
        animation: drift 30s ease-in-out infinite;
        min-height: 100vh;
    }
    [data-testid="stSidebarCollapseButton"] {
        background: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 8px !important;
        box-shadow: 0 1px 6px rgba(0,0,0,0.3) !important;
        transition: all 0.2s ease !important;
        width: 32px !important; height: 32px !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    [data-testid="stSidebarCollapseButton"]:hover {
        background: rgba(255,255,255,0.2) !important;
        border-color: rgba(255,255,255,0.3) !important;
    }
    [data-testid="stSidebarCollapseButton"] svg {
        color: #d4d4d4 !important; stroke: #d4d4d4 !important;
        fill: none !important; width: 18px !important; height: 18px !important;
    }
    [data-testid="stSidebarCollapsedControl"] {
        background: rgba(255,255,255,0.08) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3) !important;
        padding: 6px 10px !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="stSidebarCollapsedControl"]:hover {
        background: rgba(255,255,255,0.15) !important;
        border-color: rgba(255,255,255,0.25) !important;
    }
    [data-testid="stSidebarCollapsedControl"] svg {
        color: #d4d4d4 !important; stroke: #d4d4d4 !important;
        fill: none !important;
    }
    [data-testid="stSidebarCollapsedControl"] p,
    [data-testid="stSidebarCollapsedControl"] span { color: #d4d4d4 !important; font-weight: 500 !important; }
    [data-testid="stSidebar"] {
        background: rgba(18,18,18,0.88) !important;
        backdrop-filter: blur(28px);
        -webkit-backdrop-filter: blur(28px);
        border-right: 1px solid rgba(255,255,255,0.08) !important;
        box-shadow: 2px 0 30px rgba(0,0,0,0.4);
    }
    [data-testid="stSidebar"]::after {
        content:''; position:absolute; top:0; right:0; bottom:0; width:1px;
        background: linear-gradient(180deg, transparent 10%, rgba(255,255,255,0.06) 50%, transparent 90%);
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] .stMarkdown p { color: #e5e5e5 !important; }
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] > label {
        padding: 10px 14px !important;
        border-radius: 10px !important;
        margin-bottom: 2px !important;
        transition: background 0.15s;
        font-size: 0.9rem !important;
        color: #c0c0c0 !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] [role="radiogroup"] > label:hover {
        background: rgba(255,255,255,0.06);
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] [aria-checked="true"] > div {
        background: rgba(180,180,180,0.12) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        color: #e0e0e0 !important;
    }
    .stat {
        background: rgba(255,255,255,0.06);
        backdrop-filter: blur(14px);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 20px 16px;
        text-align: center;
        box-shadow: 0 1px 12px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.05);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .stat:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.3); }
    .stat-val { font-size: 1.9rem; font-weight: 700; color: #e0e0e0; line-height: 1.1; }
    .stat-lbl { font-size: 0.78rem; font-weight: 500; color: #a3a3a3; margin-top: 6px; text-transform: uppercase; letter-spacing: 0.06em; }
    .sec-title { font-size: 1.1rem; font-weight: 600; color: #e5e5e5; padding-bottom: 10px; margin-bottom: 14px; border-bottom: 1px solid rgba(255,255,255,0.06); }
    .hr { height: 1px; margin: 18px 0; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent); }
    .stButton > button {
        border-radius: 10px !important;
        font-weight: 500 !important;
        transition: all 0.15s !important;
        padding: 8px 18px !important;
        background: rgba(180,180,180,0.12) !important;
        color: #e5e5e5 !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 14px rgba(180,180,180,0.2);
        background: rgba(180,180,180,0.22) !important;
    }
    .stButton > button[data-testid="baseButton-primary"] {
        background: rgba(180,180,180,0.3) !important;
        border-color: rgba(180,180,180,0.2) !important;
    }
    .stTextInput > label, .stSelectbox > label,
    .stNumberInput > label, .stDateInput > label {
        color: #d4d4d4 !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }
    .stTextInput > div > div > input,
    .stSelectbox > div > div,
    .stNumberInput > div > div > input,
    .stDateInput > div > div > input {
        border-radius: 10px !important;
        border: 1.5px solid rgba(255,255,255,0.08) !important;
        background: rgba(255,255,255,0.07) !important;
        font-size: 0.9rem !important;
        color: #e5e5e5 !important;
        font-weight: 400 !important;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.3);
    }
    .stTextInput > div > div > input::placeholder { color: #6b6b6b !important; opacity: 1 !important; }
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div:focus-within,
    .stNumberInput > div > div > input:focus,
    .stDateInput > div > div > input:focus {
        border-color: rgba(180,180,180,0.4) !important;
        box-shadow: 0 0 0 3px rgba(180,180,180,0.1), inset 0 1px 3px rgba(0,0,0,0.3) !important;
    }
    [data-baseweb="select"] span { color: #e5e5e5 !important; }
    .stSelectbox > div > div > div > div { color: #e5e5e5 !important; }
    .stNumberInput > div > div > button {
        background: rgba(255,255,255,0.05) !important;
        border-color: rgba(255,255,255,0.08) !important;
        color: #d4d4d4 !important;
    }
    .stNumberInput > div > div > button:hover {
        background: rgba(180,180,180,0.12) !important;
        color: #e0e0e0 !important;
    }
    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.05);
    }
    .stDataFrame table { color: #e5e5e5 !important; }
    .stDataFrame thead th { background: rgba(26,26,26,0.6) !important; color: #e0e0e0 !important; }
    .stDataFrame tbody td { color: #c0c0c0 !important; }
    header[data-testid="stHeader"] {
        background: rgba(18,18,18,0.75) !important;
        backdrop-filter: blur(12px) !important;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    .stTabs [data-baseweb="tab-list"] { gap: 6px; }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px !important;
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        font-size: 0.88rem !important;
        color: #8a8a8a !important;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(180,180,180,0.12) !important;
        border-color: rgba(180,180,180,0.15) !important;
        font-weight: 600 !important;
        color: #e0e0e0 !important;
    }
    .streamlit-expanderHeader {
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        background: rgba(255,255,255,0.04) !important;
        border-radius: 12px !important;
        color: #d4d4d4 !important;
        border: 1px solid rgba(255,255,255,0.05);
    }
    .stAlert { border-radius: 12px !important; background: rgba(18,18,18,0.75) !important; backdrop-filter: blur(8px); border: 1px solid rgba(255,255,255,0.06); color: #e5e5e5 !important; }
    .stAlert p { color: #e5e5e5 !important; }
    #MainMenu, footer { visibility: hidden; }
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(180,180,180,0.2); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(180,180,180,0.4); }
    .pg-title { font-size: 1.6rem; font-weight: 700; color: #e5e5e5; margin: 0 0 2px; }
    .pg-sub { font-size: 0.88rem; color: #8a8a8a; margin: 0 0 20px; }
    .logo-box { text-align: center; padding: 24px 12px 8px; margin-bottom: 4px; }
    .logo-icon {
        width: 50px; height: 50px;
        background: linear-gradient(135deg, #6b6b6b, #9a9a9a);
        border-radius: 15px;
        display: inline-flex; align-items: center; justify-content: center;
        margin-bottom: 12px;
        box-shadow: 0 6px 20px rgba(120,120,120,0.35);
    }
    .logo-name { font-size: 1.35rem; font-weight: 700; color: #e5e5e5; letter-spacing: -0.02em; }
    .logo-tag { font-size: 0.68rem; color: #8a8a8a; text-transform: uppercase; letter-spacing: 0.12em; margin-top: 2px; }
    .stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown li { color: #c0c0c0 !important; }
    </style>""", unsafe_allow_html=True)


def hr():
    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)


def stat_card(val, lbl):
    st.markdown(
        f'<div class="stat"><div class="stat-val">{val}</div><div class="stat-lbl">{lbl}</div></div>',
        unsafe_allow_html=True,
    )


def sec_title(t):
    st.markdown(f'<div class="sec-title">{t}</div>', unsafe_allow_html=True)


def page_head(title, sub):
    st.markdown(f'<p class="pg-title">{title}</p><p class="pg-sub">{sub}</p>', unsafe_allow_html=True)
    hr()


def logo():
    st.markdown(
        '''<div class="logo-box">
        <div class="logo-icon">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none"
                 stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2Z"/>
                <line x1="8" y1="7" x2="16" y2="7"/>
                <line x1="8" y1="11" x2="13" y2="11"/>
            </svg>
        </div>
        <div class="logo-name">GradeVault</div>
        <div class="logo-tag">Grade Management System</div>
    </div>''',
        unsafe_allow_html=True,
    )
    hr()


def crud(table, cols, headers, pk, pk_range, fields, search_cols,
         select_label_fn=None):
    select_q = ", ".join(cols)
    base_sql = f"SELECT {select_q} FROM {table}"

    sc1, sc2 = st.columns([4, 1])
    with sc1:
        term = st.text_input(
            "Search", placeholder="Type to filter records...",
            key=f"srch_{table}",
        )
    with sc2:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        if st.button("Add New", type="primary", use_container_width=True,
                     key=f"add_{table}"):
            st.session_state[f"form_{table}"] = {"mode": "add"}
            st.rerun()

    if term:
        where = " OR ".join(
            [f"CAST({c} AS CHAR) LIKE %s" for c in search_cols]
        )
        rows = query(
            f"{base_sql} WHERE {where} ORDER BY {pk}",
            [f"%{term}%"] * len(search_cols),
        )
    else:
        rows = query(f"{base_sql} ORDER BY {pk}")

    if rows:
        df = pd.DataFrame(rows)
        df.columns = headers
        st.dataframe(df, use_container_width=True, hide_index=True, height=340)
        st.markdown(
            f"<p style='color:#94a3b8;font-size:0.78rem;margin-top:6px;'>"
            f"{len(rows)} record(s)</p>",
            unsafe_allow_html=True,
        )

        if select_label_fn:
            opts = {select_label_fn(r): r[pk] for r in rows}
        else:
            opts = {str(r[pk]): r[pk] for r in rows}

        hr()
        ec1, ec2, ec3 = st.columns([3, 1, 1])
        with ec1:
            sel = st.selectbox(
                "Select record", ["--"] + list(opts.keys()),
                key=f"sel_{table}",
            )
        with ec2:
            if st.button("Edit", use_container_width=True,
                         key=f"edit_{table}", disabled=(sel == "--")):
                rec = next(r for r in rows if r[pk] == opts[sel])
                st.session_state[f"form_{table}"] = {
                    "mode": "edit", "id": opts[sel], "data": rec,
                }
                st.rerun()
        with ec3:
            if st.button("Delete", use_container_width=True,
                         key=f"del_{table}", disabled=(sel == "--")):
                st.session_state[f"del_cf_{table}"] = opts[sel]
                st.rerun()

        del_id = st.session_state.get(f"del_cf_{table}")
        if del_id is not None:
            dc1, dc2, dc3 = st.columns([3, 1, 1])
            with dc1:
                st.warning(f"Confirm deletion of {pk} = {del_id}?")
            with dc2:
                if st.button("Confirm", type="primary", use_container_width=True,
                             key=f"del_y_{table}"):
                    query(f"DELETE FROM {table} WHERE {pk}=%s",
                          (del_id,), fetch=False)
                    st.session_state.pop(f"del_cf_{table}", None)
                    st.success("Record deleted.")
                    st.rerun()
            with dc3:
                if st.button("Cancel", use_container_width=True,
                             key=f"del_n_{table}"):
                    st.session_state.pop(f"del_cf_{table}", None)
                    st.rerun()
    else:
        st.info("No records found.")

    form_state = st.session_state.get(f"form_{table}")
    if form_state:
        edit_mode = form_state["mode"] == "edit"
        edit_data = form_state.get("data", {})

        with st.expander(
            f"{'Edit' if edit_mode else 'Add New'} Record", expanded=True
        ):
            vals = {}
            grid = st.columns(2)

            for i, f in enumerate(fields):
                with grid[i % 2]:
                    if edit_mode and f["name"] in edit_data:
                        dv = edit_data[f["name"]]
                    elif "default" in f:
                        dv = f["default"]
                    else:
                        dv = None

                    if f["type"] == "text":
                        vals[f["name"]] = st.text_input(
                            f["label"],
                            value=dv if dv is not None else "",
                            key=f"f_{table}_{f['name']}",
                        )

                    elif f["type"] == "number":
                        vals[f["name"]] = st.number_input(
                            f["label"],
                            value=dv if dv is not None else f.get("min", 0),
                            min_value=f.get("min"),
                            max_value=f.get("max"),
                            format=f.get("fmt", "%d"),
                            key=f"f_{table}_{f['name']}",
                        )

                    elif f["type"] == "decimal":
                        vals[f["name"]] = st.number_input(
                            f["label"],
                            value=float(dv) if dv is not None else f.get("min", 50.0),
                            min_value=f.get("min", 50.0),
                            max_value=f.get("max", 99.9),
                            step=f.get("step", 0.1),
                            format=f.get("fmt", "%.1f"),
                            key=f"f_{table}_{f['name']}",
                        )

                    elif f["type"] == "select":
                        raw_opts = f["options"]
                        labels = f.get("option_labels", [str(o) for o in raw_opts])
                        dv_str = str(dv) if dv is not None else None

                        if not labels:
                            st.warning(f"No '{f['label']}' options available. Please add related records first.")
                            vals[f["name"]] = None
                            continue

                        idx = (raw_opts.index(dv_str) if dv_str and dv_str in raw_opts else 0)
                        if idx >= len(labels):
                            idx = 0

                        chosen_label = st.selectbox(
                            f["label"], labels, index=idx,
                            key=f"f_{table}_{f['name']}",
                        )

                        if chosen_label is None:
                            vals[f["name"]] = None
                        else:
                            vals[f["name"]] = raw_opts[labels.index(chosen_label)]

                    elif f["type"] == "date":
                        min_val = f.get("min_date")
                        max_val = f.get("max_date")
                        default_val = f.get("default")

                        if edit_mode and f["name"] in edit_data and edit_data[f["name"]] is not None:
                            value = edit_data[f["name"]]
                        elif default_val is not None:
                            value = default_val
                        else:
                            value = date.today()

                        if min_val is not None and value < min_val:
                            value = min_val
                        if max_val is not None and value > max_val:
                            value = max_val

                        vals[f["name"]] = st.date_input(
                            f["label"],
                            value=value,
                            min_value=min_val,
                            max_value=max_val,
                            key=f"f_{table}_{f['name']}",
                        )

            hr()
            bc1, bc2 = st.columns(2)

            save_disabled = any(
                f["type"] == "select" and vals.get(f["name"]) is None
                for f in fields if f["type"] == "select"
            )

            with bc1:
                if st.button(
                    "Save", type="primary", use_container_width=True,
                    key=f"save_{table}", disabled=save_disabled
                ):
                    fnames = [f["name"] for f in fields]
                    if edit_mode:
                        set_sql = ", ".join([f"{n}=%s" for n in fnames])
                        sql = (f"UPDATE {table} SET {set_sql} "
                               f"WHERE {pk}=%s")
                        params = tuple(vals[n] for n in fnames) + (
                            form_state["id"],
                        )
                    else:
                        mx = query(f"SELECT MAX({pk}) AS m FROM {table}")
                        nid = ((mx[0]["m"] if mx and mx[0]["m"]
                                else pk_range[0] - 1) + 1)
                        if nid > pk_range[1]:
                            st.error("ID range exhausted.")
                            return
                        all_names = [pk] + fnames
                        placeholders = ", ".join(["%s"] * len(all_names))
                        sql = (f"INSERT INTO {table} "
                               f"({','.join(all_names)}) VALUES "
                               f"({placeholders})")
                        params = (nid,) + tuple(vals[n] for n in fnames)

                    res = query(sql, params, fetch=False)
                    if res is not None:
                        st.success(
                            f"Record {'updated' if edit_mode else 'created'}."
                        )
                        st.session_state.pop(f"form_{table}", None)
                        st.rerun()

            with bc2:
                if st.button("Cancel", use_container_width=True,
                             key=f"cancel_{table}"):
                    st.session_state.pop(f"form_{table}", None)
                    st.rerun()
