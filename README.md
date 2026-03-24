# ⚔️ Verses1 – 1v1 Python Coding Battle Platform

Have you ever solved the same problem with a friend and wondered:
*"Whose solution is actually better?"*
Not just correct — but faster, more optimized, and smarter.

That curiosity led to **Verses1**, a platform that transforms coding into real-time battles of efficiency.

🌐 **Live Demo:** [verses1.onrender.com](https://verses1.onrender.com)

---

## 🚀 What is Verses1?

Verses1 is a **1v1 Python coding battle platform** where developers compete by solving problems, entering a battle code, and benchmarking their solutions against each other.
It extends my earlier project **PyOptimizer** (which analyzed a single file for performance bottlenecks) into a competitive coding arena.

---

## ✨ Features

### 🏆 Battle Mode
- **1v1 Code Battles** – Challenge friends or random opponents with unique 8-character battle codes
- **Precise Outcome Engine** – Real-time Winner, Defeat, and Draw dynamic attribution logic for both operators
- **Real-time Winner Declaration** – Based on comprehensive code analysis
- **Battle History** – Track past duels and improvements
- **Advanced Scoring System** – Multi-factor comparison including complexity, performance, quality, and security

### 📚 Problem Bank
- **Curated Problem Statements** – Problems with difficulty levels (Easy, Medium, Hard)
- **Live Search Filtering** – Instantly find modules with real-time dynamic search bars
- **Category System** – Filter problems by tags/categories with custom icons and colors
- **Test Cases** – Visible sample tests and rigorously curated hidden validation tests
- **Constraints & Examples** – Complete problem descriptions with input/output formats
- **Function Signatures** – Predefined signatures with starter code templates

### 🎯 Practice Mode
- **Solo Problem Solving** – Practice without the pressure of battles
- **Live Practice Search** – Locate practice modules elegantly using interactive UI queries
- **Instant Feedback** – Run tests and see results immediately
- **Submission History** – Track your progress on each problem
- **Difficulty Progression** – Work your way from easy to hard problems

### 🎨 Immersive UI & UX
- **Glassmorphism Design** – Next-generation frosted glass styling across cards, data metrics, and terminals
- **Ambient Decorations** – Animated, beautifully glowing thematic background objects that bring the arena to life
- **Solid High-Contrast Terminals** – Legible coding environment built to showcase execution algorithms seamlessly
- **Client-Side Module Searching** – Microsecond-fast JavaScript-based module queries without refreshing the page

### 📊 Advanced Code Analysis Engine
- **Complexity Metrics** – Cyclomatic & cognitive complexity, maintainability index
- **Time & Space Complexity** – Automatic Big-O notation detection (O(1) to O(n!))
- **Halstead Metrics** – Volume, difficulty, effort, and estimated bugs
- **Code Quality Scores** – Style analysis, documentation coverage
- **Security Scanning** – Vulnerability detection (eval, exec, shell injection, etc.)
- **AST-Based Analysis** – Deep code structure analysis using Python's Abstract Syntax Tree

### 👤 User Features
- **User Profiles** – View stats, battle history, and solved problems
- **User Stats & Ratings** – ELO-style rating system (starting at 1200)
- **Login Activity Tracking** – Monitor account security
- **OAuth Support** – Social login via django-allauth

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Python 3.x, Django 5.2.6 |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Database** | SQLite (dev) / PostgreSQL (production) |
| **Authentication** | Django Auth + django-allauth |
| **Analysis Engine** | Custom AST-based Python Analyzer |
| **Hosting** | Render |
| **Static Files** | WhiteNoise 6.6.0 |
| **WSGI Server** | Gunicorn 21.2.0 |

---

## 📁 Project Structure

```
verses1/
├── battles/                  # Main app - battles, problems, submissions
│   ├── models.py             # Battle, Problem, Submission, UserStats, Category models
│   ├── views.py              # Battle, practice, profile, problem views
│   ├── analysis_engine.py    # AST-based code analysis & scoring engine
│   ├── code_runner.py        # Safe code execution sandbox
│   ├── auth_views.py         # Authentication views
│   ├── forms.py              # Django forms for battles & submissions
│   ├── signals.py            # Django signals
│   ├── templates/            # Battle, problem & profile templates
│   ├── templatetags/         # Custom template tags (category_tags)
│   └── management/commands/  # Custom Django commands
│       ├── seed_problems.py  # Seed problem statements
│       ├── seed_categories.py # Seed categories
│       ├── add_hidden_tests.py # Add hidden test cases
│       └── setup_oauth.py    # OAuth configuration
├── upload/                   # File upload handling
├── verses1/                  # Project settings (settings.py, urls.py)
├── media/                    # User uploaded code files
└── requirements.txt          # Python dependencies
```

---

## ⚡ Roadmap

- [x] ~~Question Bank for structured practice~~ ✅ Implemented
- [x] ~~Practice Mode~~ ✅ Implemented
- [x] ~~User Statistics & Ratings~~ ✅ Implemented
- [x] ~~Category/Tag System~~ ✅ Implemented
- [x] ~~OAuth/Social Login~~ ✅ Implemented
- [x] ~~Hidden Test Cases~~ ✅ Implemented
- [ ] Online Python Compiler with sandbox execution (Docker + FastAPI)
- [ ] Global Leaderboards
- [ ] AI-powered challenge generation
- [ ] Real-time multiplayer battles with WebSockets
- [ ] Code editor with syntax highlighting (Monaco/CodeMirror)

---

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd verses1
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Seed problems & categories**
   ```bash
   python manage.py seed_categories
   python manage.py seed_problems
   ```

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```

---

## 🤝 Collaboration

This project isn't about chasing trends or copying what's already out there.
It's about curiosity, experimentation, and reimagining coding as both competitive and collaborative.

👉 While this repository is currently private, I'm happy to collaborate with other developers, designers, and educators who'd like to improve and expand this platform further.

---

## 📫 Contact / Collaboration

If you would like to collaborate or get in touch, feel free to contact me at:

- **Email:** kavyanshsharma2004@gmail.com
- **Name:** Kavyansh Sharma

---

## 📝 License

This project is currently private. Contact the author for licensing inquiries.
