from apps.physics.engine.engine import PhysicsEngine


class Solver:
    def __init__(self, data):
        self.data = data
        self.engine = PhysicsEngine()

    def evaluate(self, formula, variables):
        import math
        safe = {
            "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "asin": math.asin, "acos": math.acos, "atan": math.atan,
            "pi": math.pi, "e": math.e, "log": math.log, "exp": math.exp,
            "radians": math.radians, "degrees": math.degrees,
            "abs": abs,
            "__import__": __import__,
        }
        env = dict(safe)
        env.update(variables)
        try:
            result = eval(formula, {"__builtins__": {}}, env)
        except ZeroDivisionError:
            return None, "Деление на ноль"
        except Exception as e:
            return None, f"Ошибка вычисления: {e}"
        return result, None

    def find_formula(self, query):
        q = query.lower()
        matches = []
        for section in self.data.SECTIONS:
            for f in section["formulas"]:
                if q in f["name"].lower() or q in f["expr"].lower():
                    matches.append((section["name"], f))
        return matches

    def solve_task(self, text):
        return self.engine.solve(text)