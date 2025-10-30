import re
from pathlib import Path

TOPICS_FILE = Path("topics/topics.md")
README_FILE = Path("README.md")

ABOUT_START = "<!-- ABOUT START -->"
ABOUT_END = "<!-- ABOUT END -->"

def parse_topics():
    done, not_done = [], []
    with open(TOPICS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            topic = line.strip()
            if not topic or topic.startswith("#") or re.match(r"^\d+\.", topic):
                continue

            topic_clean = re.sub(r"^[*\-]\s*", "", topic)
            if "{done}" in topic:
                done.append(topic_clean.replace("{done}", "").strip())
            else:
                not_done.append(topic_clean.strip())
    return done, not_done

def make_progress_bar(done_count, total):
    percent = int((done_count / total) * 100) if total > 0 else 0
    filled = int(percent / 5)
    bar = "█" * filled + "░" * (20 - filled)
    return f"**Progress:** {percent}%  \n`[{bar}]` ({done_count}/{total})"

def update_readme():
    done, not_done = parse_topics()
    total = len(done) + len(not_done)

    progress_bar = make_progress_bar(len(done), total)

    done_list_md = "\n".join([f"- ✅ {item}" for item in done]) or "_No topics done yet._"
    not_done_list_md = "\n".join([f"- ❌ {item}" for item in not_done]) or "_All topics completed!_"

    completed_section = f"""
<details>
<summary><b>✅ Completed Topics ({len(done)})</b></summary>

{done_list_md}

</details>
""".strip()

    pending_section = f"""
<details>
<summary><b>❌ Pending Topics ({len(not_done)})</b></summary>

{not_done_list_md}

</details>
""".strip()

    tracker_section = f"""
---

# 📘 Study Progress Tracker

{progress_bar}

{completed_section}

{pending_section}

---

_Last updated automatically by `update_readme.py`_
""".strip()

    # Read existing README
    if README_FILE.exists():
        content = README_FILE.read_text(encoding="utf-8")
    else:
        content = f"{ABOUT_START}\n\nWrite about your repository here...\n\n{ABOUT_END}\n\n"

    # Ensure about markers
    if ABOUT_START not in content or ABOUT_END not in content:
        content = f"{ABOUT_START}\n\nWrite about your repository here...\n\n{ABOUT_END}\n\n"

    about_section = re.search(
        rf"{ABOUT_START}[\s\S]*?{ABOUT_END}", content
    ).group(0)

    new_readme = f"{about_section}\n\n{tracker_section}"

    README_FILE.write_text(new_readme, encoding="utf-8")
    print(f"✅ README.md updated! ({len(done)} of {total} done)")

if __name__ == "__main__":
    update_readme()
