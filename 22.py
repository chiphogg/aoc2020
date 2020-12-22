import sys

import aoc


def main():
    harness = aoc.Harness()
    harness.attempt_part(
        _compute_winners_score, "./22.txt", [("./22_test.txt", 306)],
    )


def _compute_winners_score(filename):
    player, opponent = _read_decks(filename)
    while player and opponent:
        _play_round(player, opponent)
    return sum(_score(deck) for deck in (player, opponent))


def _read_decks(filename):
    with open(filename) as f:
        return (_read_deck(lines) for lines in f.read().rstrip("\n").split("\n\n"))


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
