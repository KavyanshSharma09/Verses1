# ⚔️ Verses1 – 1v1 Python Coding Battle Platform

Have you ever solved the same problem with a friend and wondered:
*"Whose solution is actually better?"*
Not just correct — but faster, more optimized, and smarter.

That curiosity led to **Verses1**, a platform that transforms coding into real-time battles of efficiency.

---

## 🚀 What is Verses1?

Verses1 is a **1v1 Python coding battle platform** where developers compete by solving problems, entering a battle code, and benchmarking their solutions against each other.
It extends my earlier project **PyOptimizer** (which analyzed a single file for performance bottlenecks) into a competitive coding arena.

---

## ✨ Features

### 🏆 Battle Mode
- **1v1 Code Battles** – Challenge friends or random opponents with unique battle codes
- **Real-time Winner Declaration** – Based on comprehensive code analysis
- **Battle History** – Track past duels and improvements
- **Advanced Scoring System** – Multi-factor comparison including complexity, performance, quality, and security

### 📚 Problem Bank
- **Curated Problem Statements** – Problems with difficulty levels (Easy, Medium, Hard)
- **Category System** – Filter problems by tags/categories
- **Test Cases** – Visible sample tests and hidden validation tests
- **Constraints & Examples** – Complete problem descriptions with input/output formats

### 🎯 Practice Mode
- **Solo Problem Solving** – Practice without the pressure of battles
- **Instant Feedback** – Run tests and see results immediately
- **Submission History** – Track your progress on each problem
- **Difficulty Progression** – Work your way from easy to hard problems

### 📊 Advanced Code Analysis
- **Complexity Metrics** – Cyclomatic & cognitive complexity, maintainability index
- **Performance Analysis** – Execution time, memory usage, CPU utilization
- **Code Quality Scores** – Pylint, Flake8, documentation coverage
- **Security Scanning** – Vulnerability detection and security score
- **Halstead Metrics** – Volume, difficulty, and effort measurements
- **Time Complexity Estimation** – Automatic Big-O notation detection

### 👤 User Features
- **User Profiles** – View stats, battle history, and solved problems
- **User Stats & Ratings** – ELO-style rating system (starting at 1200)
- **Login Activity Tracking** – Monitor account security

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Python 3.x, Django 5.2 |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Database** | SQLite (dev) / PostgreSQL (production) |
| **Authentication** | Django Auth |
| **Analysis Engine** | Custom PyOptimizer (extended for Verses1) |
| **Hosting** | Render |
| **Static Files** | WhiteNoise |

---

## 📁 Project Structure

```
verses1/
├── battles/              # Main app - battles, problems, submissions
│   ├── models.py         # Battle, Problem, Submission, UserStats models
│   ├── views.py          # Battle, practice, profile views
│   ├── analysis_engine.py # Code analysis & scoring
│   ├── code_runner.py    # Safe code execution
│   ├── templates/        # Battle & problem templates
│   └── management/       # Custom Django commands
├── upload/               # File upload handling
├── verses1/              # Project settings
└── media/                # User uploaded files
```

---

## ⚡ Roadmap

- [x] ~~Question Bank for structured practice~~ ✅ Implemented
- [x] ~~Practice Mode~~ ✅ Implemented
- [x] ~~User Statistics & Ratings~~ ✅ Implemented
- [x] ~~Category/Tag System~~ ✅ Implemented
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
