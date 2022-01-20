"""
TODO
"""
import argparse
from yao.garbler import Alice, Bob, LocalTest
from utils import read_input, verify_output, write_to_file, ALICE_DATA_PATH, BOB_DATA_PATH


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
        bits_b = list(f"{sum(self.data_bob):b}".zfill(8))
        bits_b = [int(i) for i in bits_b]
        b_inputs_clear = {
            b_wires[i]: bits_b[i]
            for i in range(len(b_wires))
        }
        print(f"Received {circuit['id']}")
        write_to_file(clear=True)
        write_to_file(f'Bob\'s input set sum is {sum(self.data_bob)}\n')
        write_to_file(f'Bob\'s message for Alice is {"".join(map(str, pbits_out.values()))}\n')
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
        bits_a = list(f"{sum(self.data_alice):b}".zfill(8))
        bits_a = [int(i) for i in bits_a]
        for i, _ in enumerate(a_wires):
            a_inputs[a_wires[i]] = (keys[a_wires[i]][bits_a[i]],
                                    pbits[a_wires[i]] ^ bits_a[i])
        result = self.ot.get_result(a_inputs, b_keys)
        str_result = ''.join([str(result[w]) for w in outputs])
        write_to_file(f'Alice\'s input set sum is {sum(self.data_alice)}\n')
        write_to_file(f'Alice\'s message for Bob is {str_result}\n')
        verify_output(int(str_result, 2))
        print('Communication completed, all the information are in the file.')


def main(party, circuit_path='circuit/add.json'):
    """
    TODO
    """
    if party == 'alice':
        Sender(circuit_path).start()
    elif party == 'bob':
        Receiver().listen()
    elif party == "table":
        LocalTest(circuit_path, print_mode='table').start()


def init():
    """
    TODO
    """
    parser = argparse.ArgumentParser(description="Run Yao protocol.")
    parser.add_argument("party",
                        choices=["alice", "bob", "table"],
                        help="The yao party to run.")
    main(party=parser.parse_args().party)


init()
