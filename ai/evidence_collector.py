from pathlib import Path


def collect_playwright_evidence(project_dir: str) -> dict:
    results_dir = Path(project_dir) / "test-results"

    evidence = {
        "screenshots": [],
        "traces": [],
        "videos": []
    }

    if not results_dir.exists():
        return evidence

    for file in results_dir.rglob("*"):
        if not file.is_file():
            continue

        if file.suffix == ".png":
            evidence["screenshots"].append(str(file))

        elif file.name == "trace.zip":
            evidence["traces"].append(str(file))

        elif file.suffix == ".webm":
            evidence["videos"].append(str(file))

    return evidence