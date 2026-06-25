import streamlit as st
import json
import os
from scheduler import STUDY_DAYS, save_schedule
from agent import generate_ai_schedule

def load_schedule():
    if not os.path.exists("data/study_log.json"):
        return None
    with open("data/study_log.json", "r") as f:
        return json.load(f)

def save_updated_schedule(data):
    with open("data/study_log.json", "w") as f:
        json.dump(data, f, indent=2)

st.set_page_config(page_title="AI Study Scheduler", page_icon="📚", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: #0a0c13;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    /* ── HEADER ── */
    .app-header {
        background: linear-gradient(135deg, #1a1f35 0%, #0d1021 100%);
        border: 1px solid #2a2f4a;
        border-radius: 16px;
        padding: 28px 32px;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .app-title {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00d4ff, #7c5cfc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .app-subtitle {
        color: #6b7280;
        font-size: 0.9rem;
        margin: 4px 0 0;
    }
    .badge {
        background: linear-gradient(135deg, #7c5cfc, #00d4ff);
        color: white;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 6px 14px;
        border-radius: 999px;
        letter-spacing: 0.05em;
    }

    /* ── DAY HEADER ── */
    .day-header {
        color: #FF6B35;
        font-size: 1rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin: 20px 0 10px;
        padding-bottom: 6px;
        border-bottom: 1px solid #1e2540;
    }

    /* ── SESSION CARDS ── */
    .session-card {
        background: linear-gradient(135deg, #141828 0%, #1a1f35 100%);
        border: 1px solid #2a2f4a;
        border-left: 4px solid #00d4ff;
        padding: 12px 16px;
        border-radius: 10px;
        margin-bottom: 8px;
        transition: all 0.2s ease;
    }
    .session-card:hover {
        border-color: #7c5cfc;
        border-left-color: #7c5cfc;
    }
    .session-complete {
        background: #0f1320;
        border: 1px solid #1a2030;
        border-left: 4px solid #00ff88;
        padding: 12px 16px;
        border-radius: 10px;
        margin-bottom: 8px;
        opacity: 0.5;
    }
    .subject-name {
        color: #e2e8f0;
        font-weight: 600;
        font-size: 0.95rem;
    }
    .subject-name-done {
        color: #4b5563;
        font-weight: 600;
        font-size: 0.95rem;
        text-decoration: line-through;
    }
    .subject-time {
        color: #6b7280;
        font-size: 0.8rem;
        margin-top: 2px;
    }
    .priority-badge-1 {
        display: inline-block;
        background: rgba(124, 92, 252, 0.2);
        color: #7c5cfc;
        font-size: 0.68rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 999px;
        margin-left: 6px;
        letter-spacing: 0.05em;
    }
    .priority-badge-2 {
        display: inline-block;
        background: rgba(0, 212, 255, 0.15);
        color: #00d4ff;
        font-size: 0.68rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 999px;
        margin-left: 6px;
    }
    .priority-badge-3 {
        display: inline-block;
        background: rgba(107, 114, 128, 0.2);
        color: #9ca3af;
        font-size: 0.68rem;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 999px;
        margin-left: 6px;
    }

    /* ── SIDEBAR ── */
    [data-testid="stSidebar"] {
        background: #0d1021;
        border-right: 1px solid #1e2540;
    }
    [data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #7c5cfc, #00d4ff);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 700;
        padding: 12px;
        width: 100%;
        font-size: 0.9rem;
        transition: opacity 0.2s;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        opacity: 0.85;
    }

    /* ── PROGRESS BAR ── */
    .stProgress > div > div {
        background: linear-gradient(90deg, #7c5cfc, #00d4ff);
        border-radius: 999px;
    }
    .stProgress > div {
        background: #1e2540;
        border-radius: 999px;
    }

    
    }
    .stButton > button:hover {
        background: #00d4ff;
        color: #0a0c13;
        border-color: #00d4ff;
    }

    /* ── METRIC ── */
    [data-testid="stMetric"] {
        background: #141828;
        border: 1px solid #2a2f4a;
        border-radius: 10px;
        padding: 12px 16px;
    }
    [data-testid="stMetricValue"] {
        color: #00d4ff !important;
        font-weight: 800 !important;
    }

    /* ── DIVIDER ── */
    hr {
        border-color: #1e2540 !important;
    }

    /* ── INFO BOX ── */
    .stInfo {
        background: #141828;
        border: 1px solid #2a2f4a;
        color: #9ca3af;
        border-radius: 10px;
    }

    /* ── WEEK LABEL ── */
    .week-label {
        color: #6b7280;
        font-size: 0.85rem;
        margin-bottom: 20px;
        padding: 8px 14px;
        background: #141828;
        border: 1px solid #1e2540;
        border-radius: 8px;
        display: inline-block;
    }
    </style>
""", unsafe_allow_html=True)
toggle = st.toggle("Done", key=f"{day}_{i}", value=session["completed"])
                        if toggle != session["completed"]:
                            idx = data["schedule"].index(session)
                            data["schedule"][idx]["completed"] = toggle
                            save_updated_schedule(data)
                            st.rerun()
# ── HEADER ──
st.markdown("""
    <div class="app-header">
        <div>
            <div class="app-title">📚 AI Study Scheduler</div>
            <div class="app-subtitle">Your personalized weekly learning plan — powered by Claude AI</div>
        </div>
        <div class="badge">✦ CLAUDE AI</div>
    </div>
""", unsafe_allow_html=True)

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("### ⚙️ Controls")
    if st.button("🤖 Generate New AI Schedule", use_container_width=True):
        with st.spinner("Claude is building your schedule..."):
            schedule = generate_ai_schedule()
            save_schedule(schedule)
            st.success("✅ Schedule ready!")
            st.rerun()

    st.divider()
    st.markdown("### 📊 Weekly Progress")

    data = load_schedule()
    if data:
        total = len(data["schedule"])
        completed = len([s for s in data["schedule"] if s["completed"]])
        remaining = total - completed
        pct = int((completed / total * 100)) if total > 0 else 0

        st.metric("Sessions Completed", f"{completed} / {total}")
        st.progress(completed / total if total > 0 else 0)
        st.markdown(f"<div style='color:#6b7280;font-size:0.8rem;margin-top:6px;'>{pct}% complete — {remaining} sessions remaining</div>", unsafe_allow_html=True)

        st.divider()
        st.markdown("### 🗓️ Subjects")
        subjects = list(set([s["subject"] for s in data["schedule"]]))
        for subj in subjects:
            subj_sessions = [s for s in data["schedule"] if s["subject"] == subj]
            subj_done = len([s for s in subj_sessions if s["completed"]])
            st.markdown(f"<div style='color:#9ca3af;font-size:0.82rem;margin-bottom:4px;'>📖 {subj}: <span style='color:#00d4ff;font-weight:700;'>{subj_done}/{len(subj_sessions)}</span></div>", unsafe_allow_html=True)

    st.divider()
    if st.button("🔄 Reset All Progress", use_container_width=True):
        data = load_schedule()
        if data:
            for s in data["schedule"]:
                s["completed"] = False
            save_updated_schedule(data)
            st.rerun()

# ── MAIN ──
data = load_schedule()

if data is None:
    st.info("👈 Click **Generate New AI Schedule** in the sidebar to get started!")
else:
    st.markdown(f'<div class="week-label">📅 Week of: {data["week_start"]}</div>', unsafe_allow_html=True)

    cols = st.columns(3)
    days_per_col = 2

    for col_idx, col in enumerate(cols):
        with col:
            for day_idx in range(days_per_col):
                day_num = col_idx * days_per_col + day_idx
                if day_num >= len(STUDY_DAYS):
                    break

                day = STUDY_DAYS[day_num]
                st.markdown(f'<div class="day-header">📆 {day}</div>', unsafe_allow_html=True)

                sessions = [s for s in data["schedule"] if s["day"] == day]
                sessions.sort(key=lambda x: x["priority"])

                for i, session in enumerate(sessions):
                    priority = session.get("priority", 3)
                    badge_class = f"priority-badge-{min(priority, 3)}"
                    priority_label = "HIGH" if priority == 1 else "MED" if priority == 2 else "LOW"

                    if session["completed"]:
                        st.markdown(f"""
                            <div class="session-complete">
                                <span class="subject-name-done">{session['subject']}</span>
                                <span class="{badge_class}">{priority_label}</span><br>
                                <span class="subject-time">⏱ {session['minutes']} mins &nbsp;✓ Done</span>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                            <div class="session-card">
                                <span class="subject-name">{session['subject']}</span>
                                <span class="{badge_class}">{priority_label}</span><br>
                                <span class="subject-time">⏱ {session['minutes']} mins</span>
                            </div>
                        """, unsafe_allow_html=True)
                        toggle = st.toggle("Done", key=f"{day}_{i}", value=session["completed"])
if toggle != session["completed"]:
    idx = data["schedule"].index(session)
    data["schedule"][idx]["completed"] = toggle
    save_updated_schedule(data)
    st.rerun()