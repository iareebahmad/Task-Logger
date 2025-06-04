import streamlit as st
import sqlite3
from datetime import date, datetime

# ✅ Connect to SQLite (creates DB if not exists)
def get_connection():
    # Use singleton pattern to keep connection open during Streamlit session
    if 'conn' not in st.session_state:
        st.session_state.conn = sqlite3.connect("task_log.db", check_same_thread=False)
    return st.session_state.conn

# ✅ Create table if not exists
def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS task_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Action_Day TEXT,
            Task_Name TEXT,
            Start_Time TEXT,
            End_Time TEXT,
            Language TEXT,
            Platform TEXT
        )
    """)
    conn.commit()

# ✅ Insert a new task
def log_task(Action_Day, Task_Name, Start_Time, End_Time, Language, Platform):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO task_log (Action_Day, Task_Name, Start_Time, End_Time, Language, Platform)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        Action_Day.isoformat() if isinstance(Action_Day, date) else Action_Day,
        Task_Name,
        Start_Time.strftime("%H:%M:%S") if hasattr(Start_Time, "strftime") else Start_Time,
        End_Time.strftime("%H:%M:%S") if hasattr(End_Time, "strftime") else End_Time,
        Language,
        Platform
    ))
    conn.commit()

# ✅ Fetch today's logs with duration calculation
def fetch_today_logs():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Task_Name, Start_Time, End_Time, Language, Platform
        FROM task_log
        WHERE Action_Day = ?
    """, (date.today().isoformat(),))
    rows = cursor.fetchall()

    results = []
    time_fmt = "%H:%M:%S"
    for task_name, start_str, end_str, language, platform in rows:
        try:
            start_dt = datetime.strptime(start_str, time_fmt)
            end_dt = datetime.strptime(end_str, time_fmt)
            duration_min = (end_dt - start_dt).total_seconds() / 60
        except Exception:
            duration_min = None  # In case of parsing errors
        results.append((task_name, start_str, end_str, duration_min, language, platform))
    return results

# 🔧 Set up DB table once at startup
create_table()

# 🧠 Streamlit UI
st.title("🧠 Crush It - Daily Task Logger")

with st.form("log_form"):
    task_name = st.text_input("Task Name")
    start_time = st.time_input("Start Time")
    end_time = st.time_input("End Time")
    language = st.text_input("Language")
    platform = st.text_input("Platform")
    action_day = st.date_input("Action Day", value=date.today())

    submitted = st.form_submit_button("Log Task")
    if submitted:
        if not task_name.strip():
            st.error("⚠️ Please enter a task name.")
        elif start_time >= end_time:
            st.error("⚠️ End time must be after start time.")
        else:
            log_task(action_day, task_name.strip(), start_time, end_time, language.strip(), platform.strip())
            st.success("✅ Task logged successfully!")

st.subheader("📋 Today's Log")
if st.button("Show Today's Logs"):
    logs = fetch_today_logs()
    if logs:
        st.table([
            {
                "Task": t,
                "Start": s,
                "End": e,
                "Total (min)": round(tm, 2) if tm is not None else "-",
                "Language": l,
                "Platform": p
            } for t, s, e, tm, l, p in logs
        ])
    else:
        st.info("No tasks logged today yet.")
