import math
from apps.physics.engine.parser import parse_task
from apps.physics.engine.matcher import find_all_applicable


class PhysicsEngine:
    def __init__(self):
        self.math_env = {}
        self._safe = {
            "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "asin": math.asin, "acos": math.acos, "atan": math.atan,
            "pi": math.pi, "e": math.e, "log": math.log, "log10": math.log10,
            "exp": math.exp, "radians": math.radians, "degrees": math.degrees,
            "fabs": math.fabs, "abs": abs,
        }

    def solve(self, text):
        parsed = parse_task(text)
        known = {k: v["value"] for k, v in parsed["values"].items()}
        target = parsed["target"]
        result = {
            "parsed": parsed,
            "known": known,
            "target": target,
            "steps": [],
            "answer": None,
            "error": None,
            "candidates": [],
        }
        if not parsed["values"]:
            result["error"] = (
                "Не удалось распознать ни одной величины с числом. "
                "Укажите значения с единицами, например: 'm = 2 кг'."
            )
            return result
        if not target:
            result["error"] = (
                "Не удалось определить, что нужно найти. "
                "Напишите: 'найти кинетическую энергию...'"
            )
            return result

        candidates = find_all_applicable(known, target, text)
        result["candidates"] = [
            (c[0], c[2]["name"], c[2]["expr"], c[3]) for c in candidates[:5]
        ]

        solved = self._solve_chain(known, target, candidates, visited=set(), depth=0)
        if solved is None:
            result["error"] = "Не удалось подобрать формулу. Проверьте единицы и условие."
            return result

        chain, final_target, final_value, final_unit = solved
        result["steps"] = self._build_steps(chain, known, final_target, final_value, final_unit)
        result["answer"] = {
            "target": final_target,
            "value": final_value,
            "unit": final_unit,
        }
        return result

    def _solve_chain(self, known, target, candidates, visited, depth):
        if depth > 4:
            return None
        current = dict(known)

        chosen = None
        for score, n_missing, f, missing in candidates:
            if f["solves"] != target:
                continue
            if f["id"] in visited:
                continue
            chosen = (f, missing)
            if all(n in current for n in f["needs"]):
                break

        if chosen is None:
            return None

        f, missing = chosen
        visited = visited | {f["id"]}
        chain = []

        for need in f["needs"]:
            if need in current:
                continue
            sub = self._solve_chain(current, need, candidates, visited, depth + 1)
            if sub is None:
                return None
            sub_chain, sub_target, sub_value, sub_unit = sub
            chain.extend(sub_chain)
            current[sub_target] = sub_value
            visited = visited | {ch["formula"]["id"] for ch in sub_chain}

        try:
            value = self._evaluate(f["code"], current)
        except ZeroDivisionError:
            return None
        except Exception:
            return None

        chain.append({
            "formula": f,
            "inputs": {n: current.get(n) for n in f["needs"]},
            "output": f["solves"],
            "value": value,
            "unit": f["unit"],
        })
        current[f["solves"]] = value

        if f["solves"] == target:
            return chain, target, value, f["unit"]

        return None

    def _evaluate(self, code, env):
        ns = dict(self._safe)
        ns.update(env)
        return eval(code, {"__builtins__": {}}, ns)

    def _build_steps(self, chain, known, target, value, unit):
        steps = []
        steps.append({
            "type": "given",
            "title": "Дано",
            "lines": [f"  {k} = {v:g}" for k, v in known.items()],
        })
        steps.append({
            "type": "target",
            "title": "Найти",
            "lines": [f"  {target} = ?"],
        })
        for i, ch in enumerate(chain, 1):
            f = ch["formula"]
            steps.append({
                "type": "formula",
                "title": f"Шаг {i}. {f['name']}",
                "lines": [
                    f"  Формула:  {f['expr']}",
                    f"  Решаем относительно: {f['solves']}",
                ],
            })
            sub = " · ".join(
                f"{k} = {v:g}" if isinstance(v, (int, float)) else f"{k} = {v}"
                for k, v in ch["inputs"].items()
            )
            steps.append({
                "type": "subst",
                "title": "Подстановка",
                "lines": [
                    f"  {sub}",
                    f"  → {f['solves']} = {ch['value']:.6g} {ch['unit']}",
                ],
            })
        steps.append({
            "type": "answer",
            "title": "Ответ",
            "lines": [f"  {target} = {value:.6g} {unit}"],
        })
        return steps