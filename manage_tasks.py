import json
import os
import sys
import re

TASKS_FILE = 'tasks.json'
HTML_FILE = 'kanban.html'

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def sync_to_html():
    tasks = load_tasks()
    data_str = json.dumps(tasks, ensure_ascii=False, indent=2)
    
    if not os.path.exists(HTML_FILE):
        print(f"Error: {HTML_FILE} not found.")
        return

    with open(HTML_FILE, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Injects data into the INITIAL_TASKS constant
    new_html = re.sub(
        r'const INITIAL_TASKS = \[.*?\];',
        f'const INITIAL_TASKS = {data_str};',
        html,
        flags=re.DOTALL
    )
    
    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f"HTML updated with {len(tasks)} tasks.")

def add_task(title, status="TO DO", progress="0%", category="Task"):
    tasks = load_tasks()
    task_id = title.lower().replace(" ", "-")
    tasks.append({
        "id": task_id,
        "title": title,
        "status": status,
        "progress": progress,
        "category": category
    })
    save_tasks(tasks)
    sync_to_html()
    print(f"Task added: {title}")

def update_task(task_id, status=None, progress=None):
    tasks = load_tasks()
    found = False
    for task in tasks:
        if task['id'] == task_id or task['title'] == task_id:
            if status: task['status'] = status
            if progress: task['progress'] = progress
            found = True
            break
    if found:
        save_tasks(tasks)
        sync_to_html()
        print(f"Task updated: {task_id}")
    else:
        print(f"Task not found: {task_id}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sync_to_html() # Default to just syncing
    elif sys.argv[1] == "add":
        title = sys.argv[2]
        status = sys.argv[3] if len(sys.argv) > 3 else "TO DO"
        progress = sys.argv[4] if len(sys.argv) > 4 else "0%"
        category = sys.argv[5] if len(sys.argv) > 5 else "Task"
        add_task(title, status, progress, category)
    elif sys.argv[1] == "update":
        task_id = sys.argv[2]
        status = sys.argv[3] if len(sys.argv) > 3 else None
        progress = sys.argv[4] if len(sys.argv) > 4 else None
        update_task(task_id, status, progress)
    elif sys.argv[1] == "sync":
        sync_to_html()
