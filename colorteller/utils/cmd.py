from pathlib import Path


def prepare_paths(target):
    """
    Prepare the paths for the given target.
    """
    if not isinstance(target, Path):
        target = Path(target)

    if not target.exists():
        target.mkdir(parents=True, exist_ok=True)

    metrics_to = target/"metrics.json"

    return {
        "target": target,
        "metrics_to": metrics_to
    }