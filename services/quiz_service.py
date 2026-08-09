import json
import os
import random
from utils.memory import load_memory, save_memory

QUIZ_DIR = "assets/quiz_data"
BATCH_SIZE = 10


def load_batch_from_file(path, start, batch_size):
    """Load batch safely from a single file"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if start >= len(data):
            return []  # ✅ skip if overflow

        return data[start:start + batch_size]

    except Exception as e:
        print(f"❌ Error reading {path}: {e}")
        return []


def fetch_quiz():
    memory = load_memory()
    counter = memory.get("counter", 0)

    all_questions = []

    files = [f for f in os.listdir(QUIZ_DIR) if f.endswith(".json")]

    if not files:
        raise Exception("No JSON files found")

    # 🔥 STEP 1: Fetch from EACH file
    for file in files:
        path = os.path.join(QUIZ_DIR, file)

        batch = load_batch_from_file(path, counter, BATCH_SIZE)

        if batch:  # ✅ only add if data exists
            all_questions.extend(batch)

    # 🔥 STEP 2: Shuffle combined result
    random.shuffle(all_questions)

    # 🔥 STEP 3: Increase counter
    counter += BATCH_SIZE

    memory["counter"] = counter
    save_memory(memory)

    return all_questions, False