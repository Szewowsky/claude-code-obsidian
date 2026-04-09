# CLAUDE.md

Obsidian vault — Twój Second Brain zarządzany przez Claude Code.

<!-- ═══════════════════════════════════════════════════════════════════════
     INSTRUKCJA: Uzupełnij sekcje oznaczone [DO UZUPEŁNIENIA].
     Usuń te komentarze gdy skończysz.
     ═══════════════════════════════════════════════════════════════════════ -->

## Persona

<!-- Opisz siebie — kim jesteś, czym się zajmujesz, jaki kontekst jest ważny.
     Im więcej Claude wie, tym lepiej dopasuje styl i treść odpowiedzi. -->

**Persona:** [DO UZUPEŁNIENIA — np. "Jan Kowalski — programista, pasjonat PKM, pracuje w startup XYZ"]

**Język:** [DO UZUPEŁNIENIA — np. "Polski" lub "English"]

**Data:** Używaj daty z system prompt do nazywania plików (YYYY-MM-DD_...) i kontekstu czasowego.

## Read Before Acting

Przed każdym zadaniem: **CZYTAJ istniejące pliki NAJPIERW**. Przed tworzeniem notatki → sprawdź czy podobna już istnieje. Przed tagowaniem → przeczytaj `tags.md`.

## Vault Structure

<!-- Opisz strukturę folderów w swoim vaultcie.
     Claude musi wiedzieć co gdzie trafia, żeby nie tworzyć bałaganu.
     Poniżej przykład — dostosuj do swojego vaulta. -->

```
Inbox/                 # Nowe notatki, do przetworzenia
Concepts/              # Insighty, frameworki, concept notes
Content/               # Pomysły na content (filmy, posty, newsletter)
Projects/              # Pomysły projektowe, backlog
Daily/                 # Notatki dzienne (YYYY-MM-DD.md)
AI_Zone/               # Strefa Claude — research, analizy, wygenerowane materiały

tags.md                # Jedyne źródło prawdy dla tagów
```

## Formatting Rules

1. **Wikilinki**: Do linkowania notatek ZAWSZE używaj `[[podwójnych nawiasów]]`
2. **Kontekst relacyjny**: Tworzysz notatkę → sprawdź czy pojęcia mają istniejące notatki → linkuj je `[[tak]]`
3. **Tagowanie**: Tylko tagi z `tags.md`. Format: `#tag`. Nie wymyślaj nowych.
4. **Format**: Wyłącznie czysty Markdown (.md)
5. **Analiza wiedzy**: W raportach/analizach ZAWSZE linkuj pojęcia `[[wikilinkami]]` aby wpiąć raport w graf
6. **Concept notes**: Gdy identyfikujesz oryginalną myśl → stwórz notatkę w `Concepts/` z `[[wikilinkami]]` do źródła
7. **Content ideas**: Pomysły na content → `Content/`. Project ideas → `Projects/`

## File Naming

- Notatki dzienne: `Daily/YYYY-MM-DD.md`
- Concept notes: `Concepts/YYYY-MM-DD_nazwa-konceptu.md`
- Research/analizy: `AI_Zone/YYYY-MM-DD_temat.md`
- Content ideas: `Content/YYYY-MM-DD_temat.md`

## Git Workflow

Po większych zmianach w vaultcie zaproponuj commit i push. Dotyczy to:
- dodania nowych notatek lub edycji wielu plików
- zmian w strukturze katalogów
- zmian w konfiguracji `.obsidian/` lub `.claude/`

**Nie wykonuj `git commit` ani `git push` automatycznie** — najpierw zaproponuj wiadomość commita i poczekaj na wyraźną zgodę.

## Self-Update

Gdy użytkownik powie "zaktualizuj CLAUDE.md":
1. Przeczytaj obecny CLAUDE.md
2. Przeanalizuj ostatnie zmiany i konwersacje
3. Zaproponuj konkretne zmiany (dodaj/usuń/zmień)
4. Poczekaj na akceptację przed nadpisaniem
