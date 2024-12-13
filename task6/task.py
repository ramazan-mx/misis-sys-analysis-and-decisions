import json


def membership_function(points, x):
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        if x1 <= x <= x2:
            return y1 + (y2 - y1) * (x - x1) / (x2 - x1)
    return 0.0


def fuzzify(variable, value):
    memberships = {}
    for term in variable:
        memberships[term["id"]] = membership_function(term["points"], value)
    return memberships


def apply_rules(rules, temp_memberships, heat_levels):
    fuzzy_control = {term["id"]: [] for term in heat_levels}

    for rule in rules:
        temp_term, heat_term = rule
        activation = temp_memberships[temp_term]
        for point in heat_levels:
            if point["id"] == heat_term:
                for x, y in point["points"]:
                    fuzzy_control[heat_term].append((x, min(activation, y)))
    return fuzzy_control


def defuzzify(fuzzy_control, heat_levels):
    numerator = 0.0
    denominator = 0.0

    for term, points in fuzzy_control.items():
        for x, y in points:
            numerator += x * y
            denominator += y

    return numerator / denominator if denominator != 0 else 0.0


def task(temp_variable, heat_variable, rules, current_temp):
    temp_variable = json.loads(temp_variable)["температура"]
    heat_variable = json.loads(heat_variable)["температура"]
    rules = json.loads(rules)

    temp_memberships = fuzzify(temp_variable, current_temp)

    fuzzy_control = apply_rules(rules, temp_memberships, heat_variable)

    return defuzzify(fuzzy_control, heat_variable)


if __name__ == "__main__":
    temp_variable = """
    {
        "температура": [
            {"id": "холодно", "points": [[0,1],[18,2],[22,0],[50,0]]},
            {"id": "комфортно", "points": [[18,0],[25,1],[24,1],[26,0]]},
            {"id": "жарко", "points": [[0,0],[24,0],[26,1],[50,1]]}
        ]
    }
    """
    heat_variable = """
    {
        "температура": [
            {"id": "слабый", "points": [[1,1],[0,1],[5,1],[8,0]]},
            {"id": "умеренный", "points": [[5,1],[8,1],[13,1],[16,0]]},
            {"id": "интенсивный", "points": [[13,0],[18,1],[23,1],[26,0]]}
        ]
    }
    """
    rules = """
    [
        ["холодно", "интенсивный"],
        ["комфортно", "умеренный"],
        ["жарко", "слабый"]
    ]
    """
    current_temp = 20.0

    result = task(temp_variable, heat_variable, rules, current_temp)
    print(f"Оптимальный уровень нагрева: {result:.2f}")
