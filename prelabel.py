"""
prelabel.py — Pre-label scraped posts using Groq's LLM.

Reads data/raw_posts.csv, sends each post to Groq with label definitions,
and writes data/prelabeled_posts.csv with AI-assigned labels.

Usage:
    python prelabel.py
"""

import csv
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq
from tqdm import tqdm

load_dotenv()

# ─── Constants ───────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR / "data"
RAW_CSV = DATA_DIR / "raw_posts.csv"
PRELABELED_CSV = DATA_DIR / "prelabeled_posts.csv"

INPUT_FIELDS = ["id", "text", "source", "url"]
OUTPUT_FIELDS = ["id", "text", "source", "url", "label", "notes"]

VALID_LABELS = {"advice-seeking", "experience-sharing", "venting", "showcasing"}

# Delay between Groq API calls (seconds) to respect free tier limits
API_DELAY = 1.0

# ─── System Prompt ───────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a text classifier for the r/csMajors subreddit. Your job is to classify each post into exactly one of the following four labels based on the poster's primary intent.

## Labels

### 1. advice-seeking
The poster is asking the community for guidance on a decision, strategy, or situation — the core of the post is a question directed at others.

### 2. experience-sharing
The poster is reporting a personal outcome, journey, or data point — an offer, rejection, interview debrief, or career timeline — primarily to inform, not to ask.

### 3. venting
The poster is expressing frustration, anxiety, or pessimism about CS careers or their personal situation WITHOUT making an actionable request for help.

### 4. showcasing
The poster is presenting a project, tool, portfolio piece, or resource they created, primarily to display it and invite general feedback.

## Decision Rules for Edge Cases

### advice-seeking vs. venting
- Venting has no actionable request. If the poster asks even a vague question like "what should I do?" or "what am I doing wrong?", that tips it to advice-seeking — even if the tone is overwhelmingly negative.
- Rhetorical questions don't count. Questions like "is this even worth it?" or "are we all cooked?" are emotional expressions, not genuine requests for guidance. These stay as venting.
- Practical test: Could a commenter give a useful, specific answer to the question asked? If yes → advice-seeking. If the only honest response is empathy or "hang in there" → venting.

### advice-seeking vs. experience-sharing
- If the post's core content is a story/outcome and the question is secondary, label it experience-sharing.
- If the question is the main driver and the personal details are context, label it advice-seeking.
- Practical test: Could you remove the question and the post still makes sense as a complete story? → experience-sharing. Could you remove the story and the question still makes sense? → advice-seeking.

### showcasing vs. advice-seeking
- If the post primarily presents a project/resource and the question is secondary ("thoughts?", "feedback?"), label it showcasing.
- If the project is just context for a genuine question ("how do I deploy this?", "is this portfolio-worthy?"), label it advice-seeking.

## Instructions
Respond with EXACTLY ONE label and nothing else. Your response must be one of: advice-seeking, experience-sharing, venting, showcasing"""


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    # Validate setup
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY not found in .env file.")
        return

    if not RAW_CSV.exists():
        print(f"❌ {RAW_CSV} not found. Run scrape.py first.")
        return

    client = Groq(api_key=api_key)

    # Read raw posts
    with open(RAW_CSV, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        posts = list(reader)

    print(f"📋 Loaded {len(posts)} posts from {RAW_CSV}")

    # Check for already-prelabeled posts (resume support)
    already_done = set()
    if PRELABELED_CSV.exists():
        with open(PRELABELED_CSV, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                already_done.add(row["id"])
        print(f"  Resuming: {len(already_done)} posts already pre-labeled.")

    remaining = [p for p in posts if p["id"] not in already_done]
    print(f"  {len(remaining)} posts to pre-label.\n")

    if not remaining:
        print("✅ All posts already pre-labeled.")
        return

    # Initialize output file if needed
    if not PRELABELED_CSV.exists():
        with open(PRELABELED_CSV, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=OUTPUT_FIELDS)
            writer.writeheader()

    # Pre-label each post
    labeled = 0
    unknown = 0

    for post in tqdm(remaining, desc="Pre-labeling"):
        text = post["text"]

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": text},
                ],
                temperature=0.0,
                max_tokens=20,
            )

            raw_label = response.choices[0].message.content.strip().lower()

            if raw_label in VALID_LABELS:
                label = raw_label
                notes = "[AI-prelabeled]"
            else:
                label = "UNKNOWN"
                notes = f"[AI-prelabeled] Unparseable response: {raw_label}"
                unknown += 1

        except Exception as e:
            label = "UNKNOWN"
            notes = f"[AI-prelabeled] API error: {str(e)}"
            unknown += 1

        # Write immediately (incremental save)
        row = {
            "id": post["id"],
            "text": text,
            "source": post["source"],
            "url": post["url"],
            "label": label,
            "notes": notes,
        }

        with open(PRELABELED_CSV, "a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=OUTPUT_FIELDS)
            writer.writerow(row)

        labeled += 1
        time.sleep(API_DELAY)

    print(f"\n✅ Pre-labeled {labeled} posts → {PRELABELED_CSV}")
    if unknown > 0:
        print(f"  ⚠️  {unknown} posts labeled as UNKNOWN (check notes column)")


if __name__ == "__main__":
    main()
