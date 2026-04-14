🕵️‍♂️ BlameStyle

BlameStyle is a background code analysis tool that estimates authorship contribution by combining:

- 📜 Git blame (ground truth history)
- 🧠 Stylometric analysis (how code is written)
- 📊 Weighted scoring (probabilistic attribution)

It answers a harder question than “who committed this?”:

«“How much of this code actually comes from a specific programmer?”»

---

🚀 Core Concept

Traditional tools rely on commit history.

BlameStyle goes further by blending:

Authorship ≈ History (what was committed)
           + Style (how it was written)

This allows detection of:

- ghostwriting
- copied code
- AI-assisted contributions
- identity drift over time

---

📦 Features

- 🔍 Per-file contribution scoring
- 📊 Overall authorship percentage
- 🧠 Style similarity via TF-IDF (character n-grams)
- 📜 Git blame integration
- 🔁 Continuous background analysis
- 📁 JSON report output

---

📂 Project Structure

blamestyle/
│
├── analyzer.py
├── contribution_report.json
└── README.md

---

⚙️ Installation

1. Clone the repository

git clone <your-repo>
cd blamestyle

---

2. Install dependencies

pip install gitpython scikit-learn watchdog

---

🧭 Usage

Run in background mode

python analyzer.py

By default, the system:

- scans the repository
- computes authorship scores
- updates every 2 minutes

---

Configure Target Author

Edit in "analyzer.py":

TARGET_AUTHOR = "Your Name"
REPO_PATH = "./your_repo"

---

📊 Output Format

Results are written to:

contribution_report.json

Example

{
  "target_author": "Will G",
  "overall_contribution_estimate": 63.4,
  "files": [
    {
      "file": "src/main.py",
      "blame_score": 0.7,
      "style_score": 0.65,
      "combined_score": 0.68
    }
  ]
}

---

🧠 Scoring Model

BlameStyle uses a weighted hybrid model:

Final Score = (0.6 × Git Blame) + (0.4 × Style Similarity)

Components

📜 Git Blame

- Measures line-level authorship
- Most reliable signal
- Resistant to style spoofing

🧠 Style Similarity

- Character n-gram TF-IDF
- Captures:
  - naming patterns
  - formatting tendencies
  - structural habits

---

🔍 What It Detects

✅ Strong Signals

- True authorship
- Partial contributions
- Refactored code ownership

⚠️ Weak Signals

- Heavily formatted codebases
- Shared coding standards
- Small files

---

🧪 Use Cases

- 🧑‍💻 Contributor analysis in teams
- 🕵️ Detect ghostwritten or outsourced code
- 🤖 Identify AI-assisted development
- 📊 Codebase ownership tracking
- 🔐 Identity verification systems

---

🔥 Advanced Concepts

🧬 Identity Drift

Detect when a contributor’s style suddenly changes:

- possible outsourcing
- AI usage
- different developer

---

🤖 AI Detection Layer (future)

Estimate probability that code is:

- human-written
- AI-generated

---

⏱ Behavioral Analysis (future)

Track:

- commit timing patterns
- editing bursts
- refactor frequency

---

⚠️ Limitations

- Not a definitive proof of authorship
- Style can be mimicked or normalized
- Git history can be rewritten
- Requires sufficient data for accuracy

---

🛠 Roadmap

- [ ] Git hook integration (pre-commit / pre-push)
- [ ] Real-time dashboard UI
- [ ] Multi-author comparison
- [ ] Drift alert system
- [ ] Plugin for IDEs (VS Code, JetBrains)
- [ ] Graph visualization of authorship

---

🧭 Philosophy

«Code has a fingerprint.
History tells you who touched it.
Style tells you who it feels like.»

BlameStyle lives at the intersection of both.

---

📄 License

MIT (or your preferred license)

---

✍️ Author

Designed for deep code attribution, behavioral analysis, and identity-aware systems.

---
