#!/usr/bin/env python3
"""
Wispr Flow Notes → Obsidian exporter.

Eksportuje notatki z bazy SQLite Wispr Flow jako pliki .md z YAML front matter
do folderu Inbox w Obsidian vault.
Uruchamiany automatycznie przez launchd (WatchPaths) lub ręcznie.

Zero zewnętrznych zależności — tylko Python stdlib.

Setup:
1. Ustaw VAULT_DIR i OUTPUT_DIR poniżej
2. Skopiuj do .claude/scripts/wispr_export.py w swoim vaultcie
3. Zainstaluj LaunchAgent (patrz wispr-flow/com.user.wispr-export.plist)
"""

import fcntl
import json
import logging
import os
import re
import sqlite3
import sys
import time
import unicodedata
from datetime import datetime
from pathlib import Path

# ── Config ── ZMIEŃ NA SWOJE ŚCIEŻKI ────────────────────────────────────────

# Baza danych Wispr Flow (domyślna lokalizacja na macOS)
DB_PATH = Path.home() / "Library" / "Application Support" / "Wispr Flow" / "flow.sqlite"

# Ścieżka do Twojego Obsidian vaulta
# Przykład dla iCloud: Path.home() / "Library" / "Mobile Documents" / "iCloud~md~obsidian" / "Documents" / "MojVault"
# Przykład lokalny: Path.home() / "Documents" / "MojVault"
VAULT_DIR = Path.home() / "ZMIEN" / "SCIEZKE" / "DO" / "VAULTA"  # ← ZMIEŃ!

# Folder docelowy na notatki z Wispr Flow (inbox)
OUTPUT_DIR = VAULT_DIR / "Ideaverse"  # ← ZMIEŃ jeśli Twój inbox ma inną nazwę

# Folder na skrypty, state i logi (nie ruszaj jeśli nie musisz)
SCRIPTS_DIR = VAULT_DIR / ".claude" / "scripts"
STATE_FILE = SCRIPTS_DIR / ".wispr-state.json"
LOCK_FILE = SCRIPTS_DIR / ".wispr-export.lock"
LOG_FILE = SCRIPTS_DIR / ".wispr-export.log"

# ── Logging ─────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
    ],
)
log = logging.getLogger("wispr-export-obsidian")

# ── Helpers ─────────────────────────────────────────────────────────────────


def slugify(text: str, max_words: int = 5) -> str:
    """Zamienia tekst na slug z pierwszych N słów (ASCII, lowercase, kebab-case)."""
    # Usuń markdown linki [text](url) → text
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    # Usuń URLe
    text = re.sub(r"https?://\S+", "", text)
    # NFD → usuń combining marks → ASCII
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    # Zostaw tylko litery, cyfry, spacje
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    words = text.lower().split()[:max_words]
    slug = "-".join(words)
    return slug or "untitled"


def load_state() -> dict:
    """Wczytuje state file (note_id → {filename, modifiedAt})."""
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            log.warning("Uszkodzony state file — zaczynam od zera")
    return {}


def save_state(state: dict) -> None:
    """Zapisuje state file atomicznie."""
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(STATE_FILE)


def note_to_markdown(note: dict) -> str:
    """Konwertuje notatkę na Markdown z YAML front matter (tags: [idea])."""
    created = note["createdAt"].split(".")[0].replace(" ", "T")  # ISO-ish
    modified = note["modifiedAt"].split(".")[0].replace(" ", "T")

    front_matter = (
        "---\n"
        f"id: {note['id']}\n"
        f"created: {created}\n"
        f"modified: {modified}\n"
        f"source: wispr-flow\n"
        f"tags:\n"
        f"  - idea\n"
        "---\n\n"
    )

    title = note["title"].strip() if note["title"] else ""
    content = note["content"].strip() if note["content"] else ""

    body = ""
    if title:
        body += f"# {title}\n\n"
    body += content + "\n"

    return front_matter + body


def filename_for_note(note: dict) -> str:
    """Generuje nazwę pliku: YYYY-MM-DD_slug.md."""
    date_str = note["createdAt"][:10]
    content_for_slug = note["title"] or note["content"] or "untitled"
    slug = slugify(content_for_slug)
    return f"{date_str}_{slug}.md"


# ── Main ────────────────────────────────────────────────────────────────────


def export_notes() -> None:
    """Główna logika eksportu."""
    if not DB_PATH.exists():
        log.error(f"Baza nie istnieje: {DB_PATH}")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

    # File lock — tylko jedna instancja na raz
    lock_fd = open(LOCK_FILE, "w")
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        log.info("Inna instancja już działa — skip")
        return

    try:
        state = load_state()

        # Podłączenie do SQLite (query_only zamiast mode=ro — mode=ro nie czyta WAL)
        notes = None
        for attempt in range(1, 4):
            try:
                conn = sqlite3.connect(f"file:{DB_PATH}?immutable=0", uri=True)
                conn.execute("PRAGMA query_only = ON")
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(
                    "SELECT id, title, contentPreview, content, createdAt, modifiedAt, isDeleted "
                    "FROM Notes"
                )
                notes = [dict(row) for row in cursor.fetchall()]
                conn.close()
                break
            except sqlite3.OperationalError as e:
                if attempt < 3:
                    log.warning(f"Baza niedostępna (próba {attempt}/3) — retry za 2s: {e}")
                    time.sleep(2)
                else:
                    log.error(f"Baza niedostępna po 3 próbach: {e}")
                    sys.exit(1)

        active_ids = set()
        changes = 0

        for note in notes:
            note_id = note["id"]

            # Usunięte notatki w Wispr Flow → NIE kasuj pliku
            # Plik zostaje — Ty decydujesz co z nim zrobić
            if note["isDeleted"]:
                if note_id in state:
                    log.info(f"Usunięto w Wispr Flow, plik zostaje: {state[note_id]['filename']}")
                continue

            active_ids.add(note_id)
            filename = filename_for_note(note)
            modified = note["modifiedAt"]

            # Sprawdź czy potrzebna aktualizacja
            if note_id in state:
                if state[note_id]["modifiedAt"] == modified:
                    if (OUTPUT_DIR / state[note_id]["filename"]).exists():
                        continue  # Bez zmian
                    # Plik usunięty ręcznie — respektuj decyzję, nie re-eksportuj
                    log.info(f"Plik usunięty ręcznie — pomijam: {state[note_id]['filename']}")
                    continue
                # Zmieniona notatka — usuń stary plik jeśli nazwa się zmieniła
                old_filename = state[note_id]["filename"]
                if old_filename != filename:
                    old_file = OUTPUT_DIR / old_filename
                    if old_file.exists():
                        old_file.unlink()

            # Zapisz plik
            md_content = note_to_markdown(note)
            (OUTPUT_DIR / filename).write_text(md_content, encoding="utf-8")
            state[note_id] = {"filename": filename, "modifiedAt": modified}
            changes += 1
            log.info(f"Eksport: {filename}")

        # Notatki które zniknęły z bazy → NIE kasuj plików
        orphaned = set(state.keys()) - active_ids
        for orphan_id in orphaned:
            log.info(f"Notatka zniknęła z Wispr Flow, plik zostaje: {state[orphan_id]['filename']}")

        save_state(state)

        if changes:
            log.info(f"Gotowe — {changes} zmian(y)")
        else:
            log.info("Brak zmian")

    finally:
        fcntl.flock(lock_fd, fcntl.LOCK_UN)
        lock_fd.close()


if __name__ == "__main__":
    export_notes()
