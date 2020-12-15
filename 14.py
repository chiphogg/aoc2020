import sys

import aoc


def main():
    harness = aoc.Harness()
    harness.attempt_part(
        _add_values_in_memory, "./14.txt", [("./14_test.txt", 165)],
    )
    harness.attempt_part(
        _add_values_in_memory_v2, "./14.txt", [("./14_test_b.txt", 208)],
    )


def _add_values_in_memory(filename):
    decoder = Decoder()
    with open(filename) as f:
        for line in f.read().splitlines():
            decoder.apply(line)
    return decoder.add_values()


def _add_values_in_memory_v2(filename):
    decoder = Decoder2()
    with open(filename) as f:
        for line in f.read().splitlines():
            decoder.apply(line)
    return decoder.add_values()


class Decoder:
    def __init__(self):
        self.memory = dict()
        self.mask = ""

    def apply(self, line):
        command, value = line.split(" = ")
        if command == "mask":
            self.mask = value
        else:
            self.apply_memory(command, value)

    def apply_memory(self, command, value):
        self.memory[self.get_address(command)] = self.apply_mask(int(value))

    def get_address(self, memory_command):
        return int(memory_command[4:-1])

    def apply_mask(self, value):
        for i in range(len(self.mask)):
            if self.masked_bit(i) == "0":
                value = _clear_bit(value, i)
            elif self.masked_bit(i) == "1":
                value = _set_bit(value, i)
        return value

    def masked_bit(self, i):
        return self.mask[-1 - i]

    def add_values(self):
        return sum(self.memory.values())


class Decoder2(Decoder):
    def apply_memory(self, command, value):
        base_address = self.apply_mask(self.get_address(command))
        for address in self.float_bits(base_address):
            self.memory[address] = int(value)

    def float_bits(self, address):
        floating_bits = tuple(
            i for i in range(len(self.mask)) if self.masked_bit(i) == "X"
        )
        return _float_bits(value=address, indices=floating_bits)

    def apply_mask(self, value):
        for i in range(len(self.mask)):
            if self.masked_bit(i) == "1":
                value = value | (1 << i)
        return value


def _set_bit(value, i_bit):
    return value | (1 << i_bit)


def _clear_bit(value, i_bit):
    return value & ~(1 << i_bit)


def _float_bits(value, indices):
    if indices:
        bit, *rest = indices
        for x in _float_bits(value, rest):
            yield _set_bit(x, bit)
            yield _clear_bit(x, bit)
    else:
        yield value


if __name__ == "__main__":
    sys.exit(main())
