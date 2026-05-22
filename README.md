# Code Language Converter AI

An AI-powered web application that converts code from one programming language to another — instantly and intelligently.

Built with **Claude AI** (Anthropic), **FastAPI**, and **Next.js**.

---

## What It Does

Most developers, at some point, need to take code written in one language and rewrite it in another. This project automates that — not just a find-and-replace, but a full semantic translation that understands logic, idioms, and language-specific conventions.

---

## Features

### Feature 1 — Basic Conversion
Paste any code snippet, select a source and target language, and get a clean translation powered by Claude AI.

- Supports 17+ languages: Python, Java, JavaScript, TypeScript, Go, Rust, C#, C++, Ruby, Swift, Kotlin, PHP, Scala, R, Dart, Lua, C
- Uses Monaco Editor (the same editor as VS Code) for a professional coding experience
- Output is idiomatic — it writes code the way a native developer would, not a literal line-by-line swap

### Feature 2 — Smart Error Fixing
Code conversion isn't always clean. Some patterns don't translate directly — a Python `dict` becomes a Java `HashMap`, a Python decorator has no direct Java equivalent, `None` becomes `null`. This feature handles those cases automatically.

How it works:
1. Convert the code using Claude AI
2. Run a second pass to detect errors and incompatibilities in the converted output
3. Apply fixes from a **Fix Pool** — a curated set of known conversion patterns for common language pairs
4. Show the user exactly which errors were found and which fixes were applied

This is the difference between code that looks converted and code that actually works.

### Feature 3 — Project Repository *(Premium)*
Real-world code is never a single file. This feature lets you work at the project level.

- Upload an entire codebase — file by file
- Each file is tracked individually with its own conversion status
- A **visual graph** (built with React Flow) shows all your files as nodes, color-coded by status:
  - ⬛ Gray — Pending (not yet converted)
  - 🟡 Yellow — Converting (in progress)
  - 🟢 Green — Converted successfully
  - 🔴 Red — Error (needs attention)
  - 🔵 Blue — Fixed (error was detected and resolved)
- Click any node to view the source code, converted code, and full conversion history side by side
- **Convert All** — process every file in the project with one click
- Every conversion is saved with version history — you can see what changed across attempts

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 16, React 19, TypeScript, Tailwind CSS v4 |
| Code Editor | Monaco Editor (@monaco-editor/react) |
| Graph Visualization | React Flow (@xyflow/react) |
| Backend | FastAPI (Python 3.13) |
| Database | SQLite via SQLAlchemy (async) |
| Authentication | JWT (JSON Web Tokens) |
| AI | Claude claude-sonnet-4-6 via Anthropic SDK |

---

## Project Status

This project is being built incrementally — one phase at a time.

| Phase | Description | Status |
|---|---|---|
| Phase 1 | Project setup, README, architecture planning | ✅ Done |
| Phase 2 | Backend API — auth, projects, file management | 🔜 Coming |
| Phase 3 | Frontend — landing page, auth pages, dashboard | 🔜 Coming |
| Phase 4 | Quick Convert editor with Monaco | 🔜 Coming |
| Phase 5 | Smart Fix system and Fix Pool | 🔜 Coming |
| Phase 6 | Project Repository with visual graph | 🔜 Coming |
| Phase 7 | Deployment | 🔜 Coming |

---

## How to Run Locally *(coming in a future commit)*

Setup instructions will be added here once the code is committed.

---

## Why I Built This

Converting code between languages is something every developer faces — moving a Python script to a Java backend, migrating a JavaScript project to TypeScript, porting a Go service to Rust. Existing tools do a surface-level job. This project uses Claude AI to do it properly, with semantic understanding and automatic error correction.

---

*Built by [Rajkumar Satya](https://github.com/rajkumar-prog)*
