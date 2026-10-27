from pathlib import Path
import csv
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "SMSSpamCollection"
OUT = ROOT / "models" / "sms_model.joblib"

def main():
    if not DATA.exists():
        raise SystemExit("Dataset not found. Save the UCI SMS Spam Collection file to data/SMSSpamCollection first.")
    labels, messages = [], []
    with DATA.open(encoding="utf-8", errors="replace") as f:
        for row in csv.reader(f, delimiter="\t"):
            if len(row) >= 2 and row[0] in {"ham", "spam"}:
                labels.append(row[0]); messages.append("\t".join(row[1:]))
    if len(messages) < 50:
        raise SystemExit("Dataset looks too small or is not in the expected tab-separated format.")
    model = Pipeline([("tfidf", TfidfVectorizer(ngram_range=(1,2), min_df=2, strip_accents="unicode")),
                      ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced"))])
    model.fit(messages, labels)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, OUT)
    print(f"Trained on {len(messages)} messages. Model saved to {OUT}")
if __name__ == "__main__":
    main()
