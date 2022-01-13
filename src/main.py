"""
Francesco Pinzauti
"""
import argparse
from yao.garbler import Alice, Bob, LocalTest

ALICE_DATA_PATH = 'input/alice.txt'
BOB_DATA_PATH = 'input/bob.txt'


def read_input(path):
    """
    TODO
    """
    with open(path, "r", encoding="utf-8") as file:
        input_data = list(map(int, file.readline().split()))
    if sum(input_data) > 255:
        raise Exception('The sum can not exceed the maximum value stored in 8 bit.')
    return input_data


def verify_output(result):
    """
    TODO
    """
    sender_data = read_input(ALICE_DATA_PATH)
    receiver_data = read_input(BOB_DATA_PATH)
    if (sum(sender_data) + sum(receiver_data)) == result:
        print(f'The sum is correct and it is {result}.')
    else:
        print(f'The sum is {result} and it is incorrect.')


class Receiver(Bob):
    """
    TODO
    """

    def __init__(self):
        super().__init__()
        self.data_bob = read_input(BOB_DATA_PATH)

    def send_evaluation(self, entry):
        """
        TODO
        """
        circuit, pbits_out = entry["circuit"], entry["pbits_out"]
        garbled_tables = entry["garbled_tables"]
        b_wires = circuit.get("bob", [])

        print(f"Received {circuit['id']}")
        print(f'The sum of Bob is {sum(self.data_bob)}')
        bits_b = list(f"{sum(self.data_bob):b}".zfill(8))
        bits_b = [int(i) for i in bits_b]

        b_inputs_clear = {
            b_wires[i]: bits_b[i]
            for i in range(len(b_wires))
        }

        self.ot.send_result(circuit, garbled_tables, pbits_out,
                            b_inputs_clear)


class Sender(Alice):
    """
    TODO
    """

    def __init__(self, circuits):
        super().__init__(circuits)
        self.data_alice = read_input(ALICE_DATA_PATH)

    def print(self, entry):
        """
        TODO
        """
        circuit, pbits, keys = entry["circuit"], entry["pbits"], entry["keys"]
        outputs = circuit["out"]
        a_wires = circuit.get("alice", [])  # Alice's wires
        a_inputs = {}  # map from Alice's wires to (key, encr_bit) inputs
        b_wires = circuit.get("bob", [])  # Bob's wires
        b_keys = {  # map from Bob's wires to a pair (key, encr_bit)
            w: self._get_encr_bits(pbits[w], key0, key1)
            for w, (key0, key1) in keys.items() if w in b_wires
        }
        print(f"======== {circuit['id']} ========")
        bits_a = list(f"{sum(self.data_alice):b}".zfill(8))
        bits_a = [int(i) for i in bits_a]
        for i, _ in enumerate(a_wires):
            a_inputs[a_wires[i]] = (keys[a_wires[i]][bits_a[i]],
                                    pbits[a_wires[i]] ^ bits_a[i])
        result = self.ot.get_result(a_inputs, b_keys)
        str_result = ''.join([str(result[w]) for w in outputs])
        print(f'The sum of Alice is {sum(self.data_alice)}')
        verify_output(int(str_result, 2))


def main(party, circuit_path='circuit/add.json', print_mode='circuit'):
    """
    TODO
    """
    if party == 'alice':
        Sender(circuit_path).start()
    elif party == 'bob':
        Receiver().listen()
    elif party == "local":
        LocalTest(circuit_path, print_mode=print_mode).start()


def init():
    """
    TODO
    """
    parser = argparse.ArgumentParser(description="Run Yao protocol.")
    parser.add_argument("party",
                        choices=["alice", "bob", "local"],
                        help="The yao party to run")
    parser.add_argument(
        "-m",
        metavar="mode",
        choices=["circuit", "table"],
        default="circuit",
        help="The print mode for local tests (default 'circuit').")
    main(
        party=parser.parse_args().party,
        print_mode=parser.parse_args().m,
    )


init()
