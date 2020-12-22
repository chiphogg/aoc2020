import copy
import sys

import aoc


def main():
    harness = aoc.Harness()
    harness.attempt_part(
        _compute_winners_score, "./22.txt", [("./22_test.txt", 306)],
    )
    harness.attempt_part(
        _compute_winners_score_recursively, "./22.txt", [("./22_test.txt", 291)],
    )


def _compute_winners_score_recursively(filename):
    decks = _read_decks(filename)
    winner = _play_recursive_combat(decks)
    return _score(decks[winner])


def _play_recursive_combat(decks):
    previous_configs = set()

    while all(decks):
        if _already_seen(decks, previous_configs):
            return 0
        cards = [deck.pop(0) for deck in decks]
        winner = (
            _play_recursive_combat(_copy_decks(decks, sizes=cards))
            if _can_recurse(decks, cards)
            else cards.index(max(cards))
        )
        decks[winner].extend((cards[winner], cards[1 - winner]))

    (winner,) = (i for i, deck in enumerate(decks) if deck)
    return winner


def _copy_decks(decks, sizes):
    return [copy.deepcopy(d[:s]) for d, s in zip(decks, sizes)]


def _can_recurse(decks, cards):
    return all(len(d) >= c for d, c in zip(decks, cards))


def _already_seen(decks, previous_configs):
    config = tuple(tuple(deck) for deck in decks)
    if config in previous_configs:
        return True
    previous_configs.add(config)


def _compute_winners_score(filename):
    player, opponent = _read_decks(filename)
    while player and opponent:
        _play_round(player, opponent)
    return sum(_score(deck) for deck in (player, opponent))


def _read_decks(filename):
    with open(filename) as f:
        return [_read_deck(lines) for lines in f.read().rstrip("\n").split("\n\n")]


def _read_deck(lines):
    return [int(x) for x in lines.splitlines() if ":" not in x]


def _play_round(player, opponent):
    (player_card, opponent_card) = (deck.pop(0) for deck in (player, opponent))
    if player_card > opponent_card:
        player.extend((player_card, opponent_card))
    else:
        opponent.extend((opponent_card, player_card))


def _score(deck):
    return sum(a * b for a, b in zip(deck, reversed(range(len(deck) + 1))))


if __name__ == "__main__":
    sys.exit(main())
