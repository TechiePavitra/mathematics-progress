import os
import re
import json

TOPIC_FILE = "topics/topics.md"
PROGRESS_DIR = "progress"
PROGRESS_JSON = os.path.join(PROGRESS_DIR, "progress.json")

def sanitize(name):
    return re.sub(r'[<>:"/\\|?*]', '', name).strip()

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def write_readme(path, text):
    readme_path = os.path.join(path, "README.md")
    if not os.path.exists(readme_path):
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(f"# {text}\n\nNotes and progress for this topic go here.\n")

def main():
    if not os.path.exists(TOPIC_FILE):
        print(f"❌ File not found: {TOPIC_FILE}")
        return

    create_folder(PROGRESS_DIR)

    if os.path.exists(PROGRESS_JSON):
        with open(PROGRESS_JSON, "r", encoding="utf-8") as f:
            progress_data = json.load(f)
    else:
        progress_data = {}

    with open(TOPIC_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    current_main = None
    total_folders = 0

    for line in lines:
        main_match = re.match(r"^\d+\.\s+(.*)", line)
        sub_match = re.match(r"^[\*\-]\s+(.*)", line)

        if main_match:
            main_topic = sanitize(main_match.group(1))
            current_main = os.path.join(PROGRESS_DIR, main_topic)
            create_folder(current_main)
            write_readme(current_main, main_topic)
            print(f"📁 Created main folder: {main_topic}")
            total_folders += 1

            if main_topic not in progress_data:
                progress_data[main_topic] = {}

        elif sub_match and current_main:
            subtopic = sanitize(sub_match.group(1))
            sub_path = os.path.join(current_main, subtopic)
            create_folder(sub_path)
            write_readme(sub_path, subtopic)
            print(f"  📂 Subfolder: {subtopic}")
            total_folders += 1

            main_topic_name = os.path.basename(current_main)
            progress_data[main_topic_name][subtopic] = progress_data[main_topic_name].get(subtopic, False)

    with open(PROGRESS_JSON, "w", encoding="utf-8") as f:
        json.dump(progress_data, f, indent=4, ensure_ascii=False)

    print(f"\n✅ Created {total_folders} folders and updated progress.json successfully!")

if __name__ == "__main__":
    main()
