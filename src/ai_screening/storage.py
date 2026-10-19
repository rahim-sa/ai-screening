"""Saves an assessment to a JSON file and reads it back."""
import json
import re
from datetime import datetime
from pathlib import Path

from ai_screening.library import prescription

ASSESSMENTS_DIR = Path(__file__).resolve().parents[2] / "assessments"


def build_assessment(company, industry, target, owner, results):
    """Turn the screening results into one dict that can be saved."""
    use_cases = []
    for row, verdict, reason in results:
        item = {
            "name": row["Specific use case"],
            "department": row["Department"],
            "verdict": verdict,
            "reason": reason,
        }
        if verdict == "DO":
            item["prescription"] = dict(prescription(row))
        use_cases.append(item)
    return {
        "company": company,
        "industry": industry,
        "target": target,
        "owner": owner,
        "created": datetime.now().isoformat(timespec="seconds"),
        "use_cases": use_cases,
    }


def save_assessment(assessment, folder=ASSESSMENTS_DIR):
    """Write the assessment to a new file. Never overwrites. Returns the path."""
    folder = Path(folder)
    folder.mkdir(exist_ok=True)
    slug = re.sub(r"[^a-z0-9]+", "-", assessment["company"].lower()).strip("-") or "company"
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    path = folder / f"{stamp}_{slug}.json"
    path.write_text(json.dumps(assessment, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def load_assessment(path):
    """Read a saved assessment."""
    return json.loads(Path(path).read_text(encoding="utf-8"))