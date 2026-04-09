# Setup — Instalacja Claude Code + Obsidian

Zainstaluj szablon Second Brain w bieżącym Obsidian vaultcie.

## Instrukcje

1. Sprawdź czy jesteś w katalogu Obsidian vaulta (powinien istnieć folder `.obsidian/`). Jeśli nie — powiedz użytkownikowi żeby otworzył Claude Code w folderze vaulta.

2. Zapytaj użytkownika:
   - Jak się nazywasz i czym się zajmujesz? (do sekcji Persona)
   - W jakim języku mam z Tobą rozmawiać?
   - Czy używasz Wispr Flow do voice notes?

3. Skopiuj odpowiedni szablon:
   - Jeśli Wispr Flow: skopiuj zawartość `CLAUDE-wispr.md` z tego repo
   - Jeśli nie: skopiuj zawartość `CLAUDE.md` z tego repo
   - Zapisz jako `.claude/CLAUDE.md` w vaultcie (stwórz folder `.claude/` jeśli nie istnieje)

4. Uzupełnij sekcje na podstawie odpowiedzi użytkownika:
   - **Persona** — wstaw imię, rolę, kontekst
   - **Język** — wstaw wybrany język

5. Skopiuj `tags.md` do roota vaulta (jeśli jeszcze nie istnieje).

6. Sprawdź strukturę folderów vaulta i dostosuj sekcję "Vault Structure" w CLAUDE.md do tego co faktycznie istnieje.

7. Jeśli użytkownik wybrał Wispr Flow:
   - Skopiuj `wispr_export.py` do `.claude/scripts/`
   - Zapytaj o ścieżkę do vaulta i uzupełnij `VAULT_DIR` i `OUTPUT_DIR` w skrypcie
   - Skopiuj wrapper do `~/.local/bin/wispr-export-run.sh` i uzupełnij ścieżkę
   - Skopiuj i uzupełnij plist do `~/Library/LaunchAgents/`
   - Załaduj LaunchAgent: `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.user.wispr-export.plist`

8. Na koniec pokaż podsumowanie co zostało zainstalowane i co użytkownik może dalej zrobić.
