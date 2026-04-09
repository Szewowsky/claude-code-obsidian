# Claude Code + Obsidian — Szablon Second Brain

Gotowy szablon `CLAUDE.md` do pracy z Obsidian vaultem przez [Claude Code](https://claude.com/product/claude-code).

Claude Code czyta `CLAUDE.md` z roota vaulta i na tej podstawie wie:
- jak tworzyć i formatować notatki (wikilinki, tagi, struktura)
- gdzie co trafia (concept notes, content ideas, daily notes)
- czego nie robić (nie commituj sam, nie wymyślaj tagów)

## Szybki start — automatyczny (zalecane)

Sklonuj repo, otwórz Claude Code w folderze swojego vaulta i wpisz:

```
/setup
```

Claude przeprowadzi Cię przez instalację krok po kroku — zapyta kim jesteś, jaki język, czy używasz Wispr Flow, i sam skopiuje wszystkie pliki na miejsce.

> Wymaga sklonowania tego repo obok vaulta, żeby Claude miał dostęp do szablonów.

## Szybki start — ręczny

Jeśli wolisz zrobić to sam:

### 1. Skopiuj `CLAUDE.md` do roota swojego vaulta

```bash
cp CLAUDE.md /ścieżka/do/twojego/vaulta/.claude/CLAUDE.md
```

> Jeśli używasz Wispr Flow — weź `CLAUDE-wispr.md` zamiast `CLAUDE.md` (ma dodatkowe sekcje o auto-eksporcie voice notes).

### 2. Uzupełnij sekcje `[DO UZUPEŁNIENIA]`

Otwórz `CLAUDE.md` i wypełnij:
- **Persona** — kim jesteś, czym się zajmujesz
- **Język** — w jakim języku Claude ma odpowiadać
- **Vault Structure** — dostosuj strukturę folderów do swojego vaulta

### 3. Skopiuj `tags.md` do roota vaulta

```bash
cp tags.md /ścieżka/do/twojego/vaulta/tags.md
```

Dodaj własne tagi. Claude nie będzie wymyślał tagów — użyje tylko tych z `tags.md`.

### 4. Gotowe

Otwórz Claude Code w folderze vaulta:

```bash
cd /ścieżka/do/twojego/vaulta
claude
```

Claude automatycznie przeczyta `CLAUDE.md` i będzie wiedział jak pracować z Twoim vaultem.

---

## Wispr Flow Setup (opcjonalnie)

Jeśli używasz [Wispr Flow](https://wisprflow.ai/r?ROBERT4265) do voice notes, możesz ustawić automatyczny eksport notatek głosowych do Obsidian.

### 1. Skopiuj skrypt do vaulta

```bash
mkdir -p /ścieżka/do/vaulta/.claude/scripts
cp wispr-flow/wispr_export.py /ścieżka/do/vaulta/.claude/scripts/
```

### 2. Edytuj ścieżki w skrypcie

Otwórz `wispr_export.py` i zmień:
- `VAULT_DIR` — ścieżka do Twojego vaulta
- `OUTPUT_DIR` — folder inbox (domyślnie `Ideaverse/`)

### 3. Skopiuj wrapper

```bash
mkdir -p ~/.local/bin
cp wispr-flow/wispr-export-run.sh ~/.local/bin/
chmod +x ~/.local/bin/wispr-export-run.sh
```

Edytuj ścieżkę w `wispr-export-run.sh` — musi wskazywać na skrypt w Twoim vaultcie.

### 4. Zainstaluj LaunchAgent

```bash
# Skopiuj i edytuj plist (zamień TWOJ_USER na swoją nazwę użytkownika)
cp wispr-flow/com.user.wispr-export.plist ~/Library/LaunchAgents/

# Załaduj agenta
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.user.wispr-export.plist
```

Od teraz voice notes z Wispr Flow będą automatycznie pojawiać się w Twoim vaultcie co 15 minut (lub natychmiast po zapisaniu nowej notatki).

### Troubleshooting

```bash
# Sprawdź czy agent działa
launchctl print gui/$(id -u)/com.user.wispr-export

# Sprawdź logi
cat ~/Library/Logs/wispr-export.log

# Przeładuj agenta
launchctl bootout gui/$(id -u)/com.user.wispr-export
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.user.wispr-export.plist
```

---

## Co jest w repo

| Plik | Opis |
|------|------|
| `CLAUDE.md` | Szablon bazowy — Obsidian + Claude Code |
| `CLAUDE-wispr.md` | Szablon rozszerzony — z sekcją Wispr Flow |
| `tags.md` | Starter kit tagów |
| `wispr-flow/wispr_export.py` | Skrypt eksportu Wispr Flow → Obsidian |
| `wispr-flow/wispr-export-run.sh` | Wrapper shell (omija problem ze spacjami w ścieżkach iCloud) |
| `wispr-flow/com.user.wispr-export.plist` | Szablon LaunchAgent dla macOS |
| `.claude/commands/setup.md` | Komenda `/setup` — automatyczna instalacja |

## FAQ

**Czy muszę używać Wispr Flow?**
Nie. `CLAUDE.md` (bazowy) działa bez Wispr Flow. Wispr Flow to opcjonalny dodatek.

**Czy to działa na Windows/Linux?**
`CLAUDE.md` i `tags.md` — tak, działają wszędzie. Skrypt Wispr Flow i LaunchAgent — tylko macOS (Wispr Flow jest na macOS).

**Mogę zmienić strukturę folderów?**
Tak — dostosuj sekcję "Vault Structure" w `CLAUDE.md` do swojego vaulta. Claude przeczyta ją i dostosuje się.

**Jak dodać własne komendy?**
Stwórz folder `.claude/commands/` w vaultcie i dodaj pliki `.md` z promptami. Claude Code automatycznie je wykryje jako slash commands.

---

Szablon powstał na bazie mojego Second Brain — więcej na [YouTube](https://www.youtube.com/watch?v=7i85dqtkptU).
