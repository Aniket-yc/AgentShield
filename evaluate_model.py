from pathlib import Path
import csv
import json

import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "SMSSpamCollection"
OUT = ROOT / "models" / "sms_model.joblib"
REPORT = ROOT / "models" / "evaluation_report.json"

def load_dataset(path):
    labels, messages = [], []
    with path.open(encoding="utf-8", errors="replace") as f:
        for row in csv.reader(f, delimiter="\t"):
            if len(row) >= 2 and row[0] in {"ham", "spam"}:
                labels.append(row[0])
                messages.append("\t".join(row[1:]))
    if len(messages) < 50:
        raise ValueError("Dataset missing, too small, or not in UCI tab-separated format.")
    return messages, labels

def main():
    if not DATA.exists():
        raise SystemExit(
            f"Dataset not found: {DATA}\n"
            "Copy the UCI file SMSSpamCollection into the data folder."
        )

    X, y = load_dataset(DATA)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    # Fit only on the training split, then evaluate on held-out messages.
    model = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2), min_df=2, strip_accents="unicode"
        )),
        ("classifier", LogisticRegression(
            max_iter=1000, class_weight="balanced"
        )),
    ])
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    labels = ["ham", "spam"]
    cm = confusion_matrix(y_test, predictions, labels=labels)
    report = {
        "dataset": "UCI SMS Spam Collection",
        "total_messages": len(X),
        "train_messages": len(X_train),
        "test_messages": len(X_test),
        "test_size": 0.20,
        "random_state": 42,
        "metrics": {
            "accuracy": round(accuracy_score(y_test, predictions), 4),
            "spam_precision": round(precision_score(y_test, predictions, pos_label="spam", zero_division=0), 4),
            "spam_recall": round(recall_score(y_test, predictions, pos_label="spam", zero_division=0), 4),
            "spam_f1": round(f1_score(y_test, predictions, pos_label="spam", zero_division=0), 4),
        },
        "confusion_matrix": {
            "labels_order": labels,
            "rows_actual_columns_predicted": [
                [int(v) for v in row] for row in cm.tolist()
            ],
        },
        "classification_report": classification_report(
            y_test, predictions, labels=labels, output_dict=True, zero_division=0
        ),
        "note": (
            "Metrics are for a held-out random split of this SMS dataset. "
            "They do not establish performance on URLs, other languages, or all scam types."
        ),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, OUT)
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("\n=== AgentShield SMS Model Evaluation ===")
    print(f"Messages: {len(X)} total | {len(X_train)} train | {len(X_test)} test")
    print(f"Accuracy:        {report['metrics']['accuracy']:.1%}")
    print(f"Spam precision:  {report['metrics']['spam_precision']:.1%}")
    print(f"Spam recall:     {report['metrics']['spam_recall']:.1%}")
    print(f"Spam F1-score:   {report['metrics']['spam_f1']:.1%}")
    print("\nConfusion matrix (rows=actual [ham, spam], columns=predicted [ham, spam]):")
    print(cm)
    print(f"\nUpdated model: {OUT}")
    print(f"Saved report:  {REPORT}")
    print("\nNote: These metrics describe this held-out SMS dataset, not all real-world scams.")

if __name__ == "__main__":
    main()
