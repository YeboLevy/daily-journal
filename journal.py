# journal.py - Daily Journal Script
# Combines: variables, functions, loops, file I/O, lists, dictionaries, error handling

import json
import os
from datetime import datetime

# ─────────────────────────────────────────────
# SKILL: Variables
# Constants used throughout the program
# ─────────────────────────────────────────────
JOURNAL_FILE = "journal.json"
VALID_MOODS = ["happy", "neutral", "sad"]
MOOD_EMOJI = {
    "happy":   ":)",
    "neutral": ":|",
    "sad":     ":(",
}


# ─────────────────────────────────────────────
# SKILL: Functions + File Reading + Error Handling
# ─────────────────────────────────────────────
def load_entries():
    """Load journal entries from the JSON file. Returns a list of dicts."""
    try:
        if not os.path.exists(JOURNAL_FILE):
            return []  # No file yet — first run
        with open(JOURNAL_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Warning: Journal file is corrupted. Starting fresh.")
        return []
    except OSError as e:
        print(f"Error reading journal: {e}")
        return []


# ─────────────────────────────────────────────
# SKILL: Functions + File Writing + Error Handling
# ─────────────────────────────────────────────
def save_entries(entries):
    """Save the list of entry dicts back to the JSON file."""
    try:
        with open(JOURNAL_FILE, "w") as f:
            json.dump(entries, f, indent=2)
        return True
    except OSError as e:
        print(f"Error saving journal: {e}")
        return False


# ─────────────────────────────────────────────
# SKILL: Functions + Dictionaries + Lists + Loops (input validation)
# ─────────────────────────────────────────────
def add_entry(entries):
    """Prompt the user for a new entry and append it to the list."""
    print("\n--- New Entry ---")

    # Auto-capture today's date and time as a variable
    date = datetime.now().strftime("%Y-%m-%d %H:%M")

    # SKILL: Loop — keep asking until we get a valid mood
    while True:
        mood = input(f"Mood ({'/'.join(VALID_MOODS)}): ").strip().lower()
        if mood in VALID_MOODS:
            break
        print(f"  Please enter one of: {', '.join(VALID_MOODS)}")

    text = input("Write your entry:\n> ").strip()
    if not text:
        print("Entry is empty — nothing saved.")
        return entries

    # SKILL: Dictionary — each entry stores related data under named keys
    entry = {
        "date": date,
        "mood": mood,
        "text": text,
    }

    # SKILL: List — append the new dict to the entries list
    entries.append(entry)

    if save_entries(entries):
        print(f"Saved! [{date}]  Mood: {mood} {MOOD_EMOJI[mood]}")

    return entries


# ─────────────────────────────────────────────
# SKILL: Functions — reusable single-entry display
# ─────────────────────────────────────────────
def display_entry(entry, index):
    """Print one entry in a readable format."""
    emoji = MOOD_EMOJI.get(entry["mood"], "?")
    print(f"\n  [{index}] {entry['date']}   Mood: {entry['mood']} {emoji}")
    print(f"      {entry['text']}")
    print("      " + "─" * 44)


# ─────────────────────────────────────────────
# SKILL: Loops — iterate over the full entries list
# ─────────────────────────────────────────────
def view_all_entries(entries):
    """Display every journal entry."""
    if not entries:
        print("\nNo entries yet. Start writing!")
        return

    print(f"\n=== All Entries ({len(entries)} total) ===")

    # SKILL: enumerate() gives a counter alongside each list item
    for i, entry in enumerate(entries, start=1):
        display_entry(entry, i)


# ─────────────────────────────────────────────
# SKILL: Lists — filter a list using a list comprehension
# ─────────────────────────────────────────────
def view_by_mood(entries):
    """Display only entries that match a chosen mood."""
    if not entries:
        print("\nNo entries yet.")
        return

    # SKILL: Loop — validate mood input
    while True:
        mood = input(f"\nFilter by mood ({'/'.join(VALID_MOODS)}): ").strip().lower()
        if mood in VALID_MOODS:
            break
        print(f"  Please enter one of: {', '.join(VALID_MOODS)}")

    # SKILL: List comprehension — create a new list from matching items
    filtered = [e for e in entries if e["mood"] == mood]

    if not filtered:
        print(f"No '{mood}' entries found.")
        return

    print(f"\n=== {mood.capitalize()} {MOOD_EMOJI[mood]} Entries ({len(filtered)} found) ===")
    for i, entry in enumerate(filtered, start=1):
        display_entry(entry, i)


# ─────────────────────────────────────────────
# SKILL: Loops + Strings — search entry text for a keyword
# ─────────────────────────────────────────────
def search_entries(entries):
    """Find all entries whose text contains a keyword (case-insensitive)."""
    if not entries:
        print("\nNo entries yet.")
        return

    keyword = input("\nSearch keyword: ").strip()
    if not keyword:
        print("No keyword entered.")
        return

    # SKILL: String method .lower() for case-insensitive matching
    keyword_lower = keyword.lower()

    # SKILL: List comprehension — filter entries where keyword appears in text
    matches = [e for e in entries if keyword_lower in e["text"].lower()]

    if not matches:
        print(f"No entries found containing '{keyword}'.")
        return

    print(f"\n=== Search: '{keyword}' ({len(matches)} found) ===")
    for i, entry in enumerate(matches, start=1):
        display_entry(entry, i)


# ─────────────────────────────────────────────
# SKILL: Dictionaries + Loops — tally and report mood counts
# ─────────────────────────────────────────────
def mood_summary(entries):
    """Show how many times each mood was recorded, with a bar chart."""
    if not entries:
        print("\nNo entries yet.")
        return

    # SKILL: Dictionary with a default value — count each mood
    counts = {mood: 0 for mood in VALID_MOODS}

    # SKILL: Loop — tally mood counts by updating dictionary values
    for entry in entries:
        mood = entry["mood"]
        if mood in counts:
            counts[mood] += 1

    total = len(entries)

    print(f"\n=== Mood Summary ({total} entries) ===")

    # SKILL: Loop over dictionary .items() to get key-value pairs
    for mood, count in counts.items():
        emoji = MOOD_EMOJI[mood]
        percent = (count / total * 100) if total > 0 else 0
        # Build a simple bar using string multiplication
        bar = "#" * count
        print(f"  {mood:<8} {emoji}  {bar:<25} {count:>3} ({percent:.0f}%)")

    # SKILL: max() with a key function on a dictionary
    top_mood = max(counts, key=lambda m: counts[m])
    print(f"\n  Most frequent mood: {top_mood} {MOOD_EMOJI[top_mood]}")


# ─────────────────────────────────────────────
# SKILL: Functions — keep display logic in one place
# ─────────────────────────────────────────────
def print_menu():
    """Print the main menu."""
    print("\n================================")
    print("         DAILY JOURNAL")
    print("================================")
    print("  1. Add new entry")
    print("  2. View all entries")
    print("  3. View entries by mood")
    print("  4. Mood summary")
    print("  5. Search by keyword")
    print("  6. Quit")
    print("================================")


# ─────────────────────────────────────────────
# SKILL: Functions + Loops + Error Handling
# main() ties everything together
# ─────────────────────────────────────────────
def main():
    """Main program loop — load entries, show menu, dispatch to features."""
    print("Welcome to your Daily Journal!")

    # SKILL: Variables — hold program state across loop iterations
    entries = load_entries()
    print(f"({len(entries)} existing {'entry' if len(entries) == 1 else 'entries'} loaded)")

    # SKILL: Loop — keep the app running until the user quits
    while True:
        print_menu()

        # SKILL: Error handling — catch Ctrl+C or piped EOF gracefully
        try:
            choice = input("Choose an option (1-6): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if choice == "1":
            entries = add_entry(entries)
        elif choice == "2":
            view_all_entries(entries)
        elif choice == "3":
            view_by_mood(entries)
        elif choice == "4":
            mood_summary(entries)
        elif choice == "5":
            search_entries(entries)
        elif choice == "6":
            print("Goodbye! Keep journaling.")
            break
        else:
            print("Invalid choice — enter a number from 1 to 6.")


# ─────────────────────────────────────────────
# SKILL: Standard Python entry point guard
# Only runs main() when executed directly, not when imported
# ─────────────────────────────────────────────
if __name__ == "__main__":
    main()
