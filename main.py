import os
import time
import json
from collections import Counter
from git import Repo
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

REPO_PATH = "./your_repo"
TARGET_AUTHOR = "Your Name"
OUTPUT_FILE = "contribution_report.json"

repo = Repo(REPO_PATH)

# ---------------------------
# 1. Extract code by author
# ---------------------------
def get_author_code(author_name):
    code_snippets = []

    for commit in repo.iter_commits():
        if author_name.lower() in commit.author.name.lower():
            for item in commit.stats.files:
                try:
                    file_path = os.path.join(REPO_PATH, item)
                    if os.path.exists(file_path):
                        with open(file_path, "r", errors="ignore") as f:
                            code_snippets.append(f.read())
                except:
                    pass

    return code_snippets


# ---------------------------
# 2. Extract all repo files
# ---------------------------
def get_all_files():
    files = []
    for root, _, filenames in os.walk(REPO_PATH):
        for f in filenames:
            if f.endswith((".py", ".js", ".cpp", ".c", ".h")):
                files.append(os.path.join(root, f))
    return files


# ---------------------------
# 3. Stylometric similarity
# ---------------------------
def compute_similarity(author_corpus, file_text):
    documents = author_corpus + [file_text]

    vectorizer = TfidfVectorizer(
        analyzer="char",
        ngram_range=(3, 5)
    )

    tfidf = vectorizer.fit_transform(documents)
    sim = cosine_similarity(tfidf[-1], tfidf[:-1])

    return sim.mean()


# ---------------------------
# 4. Git blame weighting
# ---------------------------
def blame_score(file_path, target_author):
    rel_path = os.path.relpath(file_path, REPO_PATH)
    try:
        blame = repo.blame("HEAD", rel_path)
        total_lines = 0
        target_lines = 0

        for commit, lines in blame:
            total_lines += len(lines)
            if target_author.lower() in commit.author.name.lower():
                target_lines += len(lines)

        if total_lines == 0:
            return 0

        return target_lines / total_lines

    except:
        return 0


# ---------------------------
# 5. Analyze repo
# ---------------------------
def analyze():
    author_corpus = get_author_code(TARGET_AUTHOR)
    files = get_all_files()

    results = []

    for file_path in files:
        try:
            with open(file_path, "r", errors="ignore") as f:
                content = f.read()

            style_score = compute_similarity(author_corpus, content)
            blame = blame_score(file_path, TARGET_AUTHOR)

            combined = (0.6 * blame) + (0.4 * style_score)

            results.append({
                "file": file_path,
                "blame_score": round(blame, 3),
                "style_score": round(style_score, 3),
                "combined_score": round(combined, 3)
            })

        except:
            continue

    # overall percentage
    overall = sum(r["combined_score"] for r in results) / max(len(results), 1)

    output = {
        "target_author": TARGET_AUTHOR,
        "overall_contribution_estimate": round(overall * 100, 2),
        "files": results
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"[Updated] Contribution: {output['overall_contribution_estimate']}%")


# ---------------------------
# 6. Background loop
# ---------------------------
def run_background(interval=60):
    while True:
        analyze()
        time.sleep(interval)


if __name__ == "__main__":
    run_background(120)  # every 2 minutes
