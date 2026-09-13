from apps.physics.engine.library import FORMULA_LIBRARY


def score_formula(formula, known, target):
    score = 0
    needs = formula["needs"]
    solves = formula["solves"]
    if target is not None:
        if solves == target:
            score += 100
        elif target and target.lower() in formula["name"].lower():
            score += 60
    for n in needs:
        if n in known:
            score += 25
    missing = [n for n in needs if n not in known]
    score -= len(missing) * 5
    return score, missing


def find_best_formula(known, target, text=""):
    candidates = []
    text_low = text.lower()
    for f in FORMULA_LIBRARY:
        score, missing = score_formula(f, known, target)
        for tag in f["tags"]:
            if tag in text_low:
                score += 30
        if f["solves"] in known and f["solves"] != target:
            score -= 40
        candidates.append((score, len(missing), f, missing))
    candidates.sort(key=lambda x: (-x[0], x[1]))
    return candidates


def find_all_applicable(known, target, text=""):
    scored = find_best_formula(known, target, text)
    return scored