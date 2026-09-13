import re
from apps.physics.engine.units import UNITS, to_si


NUMBER_RE = re.compile(
    r"(?P<value>-?\d+(?:[.,]\d+)?(?:[eE][-+]?\d+)?)\s*(?P<unit>[а-яА-Яa-zA-Z°²³/·]+)?"
)


KNOWN_QUANTITIES = {
    "масса": "m", "массой": "m", "весом": "m", "m": "m",
    "скорость": "v", "скоростью": "v", "v": "v",
    "ускорение": "a", "ускорением": "a", "a": "a",
    "время": "t", "t": "t",
    "путь": "S", "расстояние": "S", "s": "S",
    "сила": "F", "силой": "F", "f": "F",
    "работа": "A", "работу": "A", "a": "A",
    "мощность": "N", "мощностью": "N",
    "энергия": "E", "энергию": "E", "E": "E",
    "высота": "h", "высоту": "h", "h": "h",
    "жёсткость": "k", "жесткость": "k", "k": "k",
    "удлинение": "x", "x": "x",
    "объём": "V", "объем": "V", "V": "V",
    "давление": "p", "p": "p",
    "температура": "T", "T": "T",
    "сопротивление": "R", "R": "R",
    "напряжение": "U", "U": "U",
    "ток": "I", "I": "I", "сила тока": "I",
    "заряд": "q", "q": "q",
    "ёмкость": "C", "емкость": "C", "C": "C",
    "индуктивность": "L", "L": "L",
    "частота": "ν", "период": "T",
    "индукция": "B", "B": "B",
    "радиус": "R", "R": "R",
    "длина": "L", "L": "L",
    "плотность": "ρ",
    "кпд": "КПД",
    "угол": "α", "α": "α",
}


TARGET_PATTERNS = [
    r"найти\s+(?P<target>.+?)(?:\s+тела|\s+массой|\s+движущегося|$|,|\.)",
    r"определить\s+(?P<target>.+?)(?:\s+тела|\s+массой|$|,|\.)",
    r"вычислить\s+(?P<target>.+?)(?:\s+тела|\s+массой|$|,|\.)",
    r"какова\s+(?P<target>.+?)(?:\s+тела|\s+массой|$|,|\.)",
    r"каков[ао]?\s+(?P<target>.+?)(?:\s+тела|\s+массой|$|,|\.)",
    r"найти\s+(?P<target>[\wа-яА-ЯёЁ]+)",
    r"какая\s+(?P<target>[\wа-яА-ЯёЁ ]+?)(?:\?|$)",
    r"какой\s+(?P<target>[\wа-яА-ЯёЁ ]+?)(?:\?|$)",
    r"чему\s+равн[аоы]?\s+(?P<target>[\wа-яА-ЯёЁ ]+?)(?:\?|$)",
]


def extract_numbers(text):
    found = []
    for m in NUMBER_RE.finditer(text):
        raw = m.group("value").replace(",", ".")
        try:
            value = float(raw)
        except ValueError:
            continue
        unit = m.group("unit")
        if unit and unit not in UNITS:
            if unit.lower() in UNITS:
                unit = unit.lower()
            else:
                unit = None
        si_value, si_unit = to_si(value, unit)
        found.append({
            "raw": value,
            "raw_unit": unit,
            "value": si_value,
            "unit": si_unit,
            "pos": m.start(),
        })
    return found


def extract_quantity_name(context):
    ctx = context.lower()
    for key in sorted(KNOWN_QUANTITIES, key=len, reverse=True):
        if key in ctx:
            return KNOWN_QUANTITIES[key]
    return None


def extract_target(text):
    low = text.lower()
    for pat in TARGET_PATTERNS:
        m = re.search(pat, low)
        if m:
            return m.group("target").strip()
    return None


def map_values_to_quantities(text, numbers):
    result = {}
    for num in numbers:
        start = max(0, num["pos"] - 30)
        end = min(len(text), num["pos"] + 40)
        context = text[start:end]
        before = text[max(0, num["pos"] - 25):num["pos"]]
        name = extract_quantity_name(before) or extract_quantity_name(context)
        if name and name not in result:
            result[name] = {
                "value": num["value"],
                "unit": num["unit"],
                "raw": num["raw"],
                "raw_unit": num["raw_unit"],
            }
    return result


def parse_task(text):
    numbers = extract_numbers(text)
    values = map_values_to_quantities(text, numbers)
    target_text = extract_target(text)
    target = None
    if target_text:
        for key in sorted(KNOWN_QUANTITIES, key=len, reverse=True):
            if key in target_text.lower():
                target = KNOWN_QUANTITIES[key]
                break
    return {
        "text": text,
        "numbers": numbers,
        "values": values,
        "target_text": target_text,
        "target": target,
    }