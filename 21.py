import collections
from functools import reduce
import pprint
import sys

import aoc


def main():
    harness = aoc.Harness()
    harness.attempt_part(
        _count_nonallergic_ingredient_occurrences, "./21.txt", [("./21_test.txt", 5)],
    )
    harness.attempt_part(
        _list_canonical_dangerous_ingredients,
        "./21.txt",
        [("./21_test.txt", "mxmxvkd,sqjhc,fvjkl")],
    )


def _list_canonical_dangerous_ingredients(filename):
    ingredients, allergen_recipes = _parse_label(filename)
    allergens = _solve_allergens(ingredients, allergen_recipes)
    return ",".join(allergens[k] for k in sorted(allergens))


def _count_nonallergic_ingredient_occurrences(filename):
    ingredients, allergen_recipes = _parse_label(filename)
    allergens = _solve_allergens(ingredients, allergen_recipes)
    return sum((i not in allergens.values()) for recipe in ingredients for i in recipe)


def _solve_allergens(ingredients, allergen_recipes):
    decoded = dict()
    while len(decoded) < len(allergen_recipes):
        for a in allergen_recipes:
            if a not in decoded:
                candidates = reduce(
                    set.intersection, (ingredients[i] for i in allergen_recipes[a])
                ).difference(decoded.values())
                if len(candidates) == 1:
                    (food,) = candidates
                    decoded[a] = food
    return decoded


def _find_candidate_ingredients(indices, ingredients):
    return


def _parse_label(filename):
    ingredients = []
    allergens = collections.defaultdict(set)
    with open(filename) as f:
        for i, line in enumerate(f.read().splitlines()):
            raw_ingredients, raw_allergens = line.rstrip(")").split(" (contains ")

            ingredients.append(set(raw_ingredients.split()))

            for a in raw_allergens.split(", "):
                allergens[a].add(i)
    return ingredients, allergens


if __name__ == "__main__":
    sys.exit(main())
