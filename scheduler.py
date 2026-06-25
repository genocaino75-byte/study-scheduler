import json
import os
from datetime import datetime, timedelta

# Our subjects and how many hours per week we want to study each
SUBJECTS = [
    {"name": "Python", "weekly_hours": 6, "priority": 1},
    {"name": "LLM/Agents", "weekly_hours": 6, "priority": 1},
    {"name": "JavaScript", "weekly_hours": 6, "priority": 2},
    {"name": "HTML/CSS", "weekly_hours": 6, "priority": 3},
]

# Days of the week you plan to study
STUDY_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

def generate_schedule():
    schedule = []
    for subject in SUBJECTS:
        daily_minutes = round((subject["weekly_hours"] * 60) / len(STUDY_DAYS))
        for day in STUDY_DAYS:
            session = {
                "day": day,
                "subject": subject["name"],
                "minutes": daily_minutes,
                "priority": subject["priority"],
                "completed": False
            }
            schedule.append(session)
    return schedule

def print_schedule(schedule):
    print("\n📅 YOUR WEEKLY STUDY SCHEDULE\n")
    for day in STUDY_DAYS:
        print(f"--- {day} ---")
        sessions = [s for s in schedule if s["day"] == day]
        sessions.sort(key=lambda x: x["priority"])
        for s in sessions:
            print(f"  {s['subject']}: {s['minutes']} mins")
        print()

def save_schedule(schedule):  # ✅ now at correct indentation level
    data = {
        "week_start": datetime.now().strftime("%Y-%m-%d"),
        "schedule": schedule,
        "log": []
    }
    os.makedirs("data", exist_ok=True)
    with open("data/study_log.json", "w") as f:
        json.dump(data, f, indent=2)
    print("✅ Schedule saved to data/study_log.json")

def load_schedule():
    if not os.path.exists("data/study_log.json"):
        print("No saved schedule found.")
        return None
    with open("data/study_log.json", "r") as f:
        return json.load(f)

if __name__ == "__main__":
    schedule = generate_schedule()
    print_schedule(schedule)
    save_schedule(schedule)
    loaded = load_schedule()
    print(f"\n✅ Loaded {len(loaded['schedule'])} sessions from file")