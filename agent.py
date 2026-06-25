import anthropic
import json
import os
from dotenv import load_dotenv
from scheduler import SUBJECTS, STUDY_DAYS, save_schedule

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def generate_ai_schedule():
    subjects_text = "\n".join([
        f"- {s['name']}: {s['weekly_hours']} hours/week, priority {s['priority']}"
        for s in SUBJECTS
    ])
   
    prompt = f"""You are a study schedule assistant. Create a weekly study schedule based on these subjects and requirements:

{subjects_text}

Study days: {', '.join(STUDY_DAYS)}

Rules:
- Each subject gets exactly 60 minutes per day, every study day
- Higher priority subjects (priority 1) should be scheduled earlier in the day
- Vary the order of subjects each day to keep things fresh
- Return ONLY a JSON array of sessions, no other text

Each session should look like this:
{{"day": "Monday", "subject": "Python", "minutes": 60, "priority": 1, "completed": false}}
""" 

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
   
    response_text = message.content[0].text
    print("RAW RESPONSE:", response_text)  # debug line

    # Strip markdown code fences if Claude added them
    response_text = response_text.strip()
    response_text = response_text.replace("```json", "").replace("```", "").strip()

    schedule = json.loads(response_text)
    return schedule

if __name__ == "__main__":
    print("🤖 Generating AI schedule...")
    schedule = generate_ai_schedule()
   
    for day in STUDY_DAYS:
        print(f"\n--- {day} ---")
        sessions = [s for s in schedule if s["day"] == day]
        for s in sessions:
            print(f"  {s['subject']}: {s['minutes']} mins")
   
    save_schedule(schedule)
    print("\n✅ AI schedule saved!")