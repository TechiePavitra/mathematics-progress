import os
import re
from pathlib import Path

TOPICS_FILE = Path("topics/topics.md")
PROGRESS_DIR = Path("progress")

def parse_topics():
    """Extract main topics and subtopics from topics.md"""
    topics = []
    current_topic = None

    with open(TOPICS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if re.match(r"^\d+\.\s", line):  # Main topic
                if current_topic:
                    topics.append(current_topic)
                title = re.sub(r"^\d+\.\s*", "", line)
                current_topic = {"title": title, "subs": []}
            elif line.startswith("*") or line.startswith("-"):
                if current_topic:
                    sub = re.sub(r"^[*\-]\s*", "", line)
                    sub = re.sub(r"\{done\}", "", sub).strip()
                    current_topic["subs"].append(sub)

    if current_topic:
        topics.append(current_topic)

    return topics

def slugify(name):
    """Make folder name safe"""
    return re.sub(r"[^a-zA-Z0-9_\-]", "_", name.strip())

def generate_next():
    topics = parse_topics()
    PROGRESS_DIR.mkdir(exist_ok=True)

    existing = {p.name for p in PROGRESS_DIR.iterdir() if p.is_dir()}

    for topic in topics:
        topic_slug = slugify(topic["title"])
        if topic_slug not in existing:
            topic_path = PROGRESS_DIR / topic_slug
            topic_path.mkdir(exist_ok=True)

            # Create subtopic files/folders if needed
            for sub in topic["subs"]:
                sub_slug = slugify(sub)
                (topic_path / f"{sub_slug}.md").write_text(
                    f"# {sub}\n\nNotes go here.", encoding="utf-8"
                )

            print(f"✅ Created new topic folder: {topic_slug}")
            print(f"   → {len(topic['subs'])} subtopics generated.")
            return  # Stop after one topic

    print("🎉 All topics already generated!")

if __name__ == "__main__":
    generate_next()
