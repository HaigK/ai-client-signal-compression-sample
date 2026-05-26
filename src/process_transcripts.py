import json
from pathlib import Path
from datetime import datetime, timezone


BASE_DIR = Path(__file__).resolve().parents[1]
SAMPLE_DATA_DIR = BASE_DIR / "sample_data"
OUTPUT_DIR = BASE_DIR / "output_examples"
OUTPUT_FILE = OUTPUT_DIR / "client_signal_summary.json"


SIGNAL_KEYWORDS = {
    "client_pain_points": {
        "manual reporting": ["manual report", "manual reporting", "spreadsheet", "excel"],
        "slow data access": ["slow data", "waiting on data", "data delay", "report delay"],
        "unclear AI governance": ["ai governance", "governance", "policy", "approval"],
        "workflow inefficiency": ["workflow", "handoff", "bottleneck", "process delay"],
        "poor documentation": ["documentation", "tribal knowledge", "unclear instructions"]
    },
    "risk_signals": {
        "budget concern": ["budget", "cost", "too expensive", "funding"],
        "unclear project owner": ["no owner", "unclear owner", "ownership", "who owns"],
        "delayed rollout": ["delay", "delayed", "behind schedule", "rollout risk"],
        "user adoption risk": ["adoption", "users won't use", "training gap", "resistance"]
    },
    "interest_areas": {
        "generative AI": ["generative ai", "genai", "llm", "large language model"],
        "workflow automation": ["automation", "automate", "workflow"],
        "dashboard reporting": ["dashboard", "power bi", "reporting", "metrics"],
        "knowledge management": ["knowledge management", "documentation", "search"],
        "client signal extraction": ["client signal", "signals", "call notes", "transcript"]
    }
}


def read_text_files(folder: Path) -> dict:
    """Read all .txt files in the sample_data folder."""
    texts = {}

    if not folder.exists():
        raise FileNotFoundError(f"Missing folder: {folder}")

    for path in folder.glob("*.txt"):
        texts[path.name] = path.read_text(encoding="utf-8")

    if not texts:
        raise FileNotFoundError("No .txt files found in sample_data/")

    return texts


def find_matches(text: str, keyword_map: dict) -> list:
    """Return signal labels when any related keyword appears in the text."""
    text_lower = text.lower()
    matches = []

    for label, keywords in keyword_map.items():
        for keyword in keywords:
            if keyword in text_lower:
                matches.append(label)
                break

    return sorted(set(matches))


def score_interest(interest_areas: list, pain_points: list) -> int:
    """Simple scoring model for demonstration."""
    score = 40
    score += len(interest_areas) * 10
    score += len(pain_points) * 5
    return min(score, 100)


def score_churn_risk(risk_signals: list) -> str:
    """Simple churn-risk label for demonstration."""
    if len(risk_signals) >= 3:
        return "high"
    if len(risk_signals) >= 1:
        return "medium"
    return "low"


def recommend_next_action(interest_areas: list, risk_signals: list) -> str:
    """Create a simple business recommendation."""
    if "unclear AI governance" in risk_signals or "generative AI" in interest_areas:
        return "Send an AI governance overview and schedule a technical discovery call."

    if "dashboard reporting" in interest_areas:
        return "Send dashboard reporting examples and schedule a metrics review."

    if "workflow automation" in interest_areas:
        return "Schedule a workflow-mapping session to identify automation opportunities."

    return "Schedule a follow-up call to clarify business needs and next steps."


def process_file(filename: str, text: str) -> dict:
    """Convert one unstructured text file into structured client signals."""
    pain_points = find_matches(text, SIGNAL_KEYWORDS["client_pain_points"])
    risk_signals = find_matches(text, SIGNAL_KEYWORDS["risk_signals"])
    interest_areas = find_matches(text, SIGNAL_KEYWORDS["interest_areas"])

    return {
        "source_file": filename,
        "client_pain_points": pain_points,
        "risk_signals": risk_signals,
        "interest_areas": interest_areas,
        "recommended_next_action": recommend_next_action(interest_areas, risk_signals),
        "churn_risk": score_churn_risk(risk_signals),
        "interest_score": score_interest(interest_areas, pain_points)
    }


def main():
    texts = read_text_files(SAMPLE_DATA_DIR)

    summaries = []
    for filename, text in texts.items():
        summaries.append(process_file(filename, text))

    output = {
        "project": "AI Client Signal Compression Sample",
        "created_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "description": "Converts unstructured business text into structured client signals.",
        "records_processed": len(summaries),
        "summaries": summaries
    }

    OUTPUT_DIR.mkdir(exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(output, indent=2), encoding="utf-8")

    print(f"Wrote output to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
