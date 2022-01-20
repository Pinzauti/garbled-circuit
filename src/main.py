"""
It contains the actual logic of the garbled circuit, it is heavily based on the
ojroques/garbled-circuit repo, which is imported as a library in the yao folder.
"""
import argparse
from yao.garbler import Alice, Bob, LocalTest
from utils import read_input, verify_output, write_to_file, ALICE_DATA_PATH, BOB_DATA_PATH


class Receiver(Bob):
    """
    This class inherits the Bob class of the ojroques/garbled-circuit library.
    """

    def __init__(self):
        super().__init__()
        self.data_bob = read_input(BOB_DATA_PATH)

    def send_evaluation(self, entry):
        """
        Evaluate yao circuit for Bob and Alice's inputs and
        send back the results.
        It writes the following to the output file:
        - the sum of Bob's numbers
        - the message of Bob for Alice
        :param entry: A dict representing the circuit to evaluate.
        :return: None.
        """
        circuit, pbits_out = entry["circuit"], entry["pbits_out"]
        garbled_tables = entry["garbled_tables"]
        b_wires = circuit.get("bob", [])  # list of Bob's wires
        # Read the numbers from the input file, it performs a sum and converts the sum result
        # to bits, which are zero-filled to 8 bits. The bits are then converted to a list
        bits_b = list(f"{sum(self.data_bob):b}".zfill(8))
        bits_b = [int(i) for i in bits_b]
        # Create dict mapping each wire of Bob to Bob's input
        b_inputs_clear = {
            b_wires[i]: bits_b[i]
            for i in range(len(b_wires))
        }
        # Print to screen the circuit received info and write all the info to the output file
        print(f"Received {circuit['id']}")
        write_to_file(clear=True)
        write_to_file(f'Bob\'s input set sum is {sum(self.data_bob)}\n'
                      f'Bob\'s message for Alice is {"".join(map(str, pbits_out.values()))}\n')
        # Evaluate and send result to Alice
        self.ot.send_result(circuit, garbled_tables, pbits_out,
                            b_inputs_clear)


class Sender(Alice):
    """
    This class inherits the Alice class of the ojroques/garbled-circuit library.
    """

    def __init__(self, circuits):
        super().__init__(circuits)
        self.data_alice = read_input(ALICE_DATA_PATH)

    def print(self, entry):
        """
        It writes to the output file:
        - the sum of Alice's numbers
        - the message of Alice for Bob
        - the result of the garbled circuit, and if it is correct or not.
        :param entry: A dict representing the circuit to evaluate.
        :return: None.
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
        # Read the numbers from the input file, it performs a sum and converts the sum result
        # to bits, which are zero-filled to 8 bits. The bits are then converted to a list
        bits_a = list(f"{sum(self.data_alice):b}".zfill(8))
        bits_a = [int(i) for i in bits_a]
        # Map Alice's wires to (key, encr_bit)
        for i, _ in enumerate(a_wires):
            a_inputs[a_wires[i]] = (keys[a_wires[i]][bits_a[i]],
                                    pbits[a_wires[i]] ^ bits_a[i])
        # Send Alice's encrypted inputs and keys to Bob
        result = self.ot.get_result(a_inputs, b_keys)
        # Write all the info to the file
        str_result = ''.join([str(result[w]) for w in outputs])
        write_to_file(f'Alice\'s input set sum is {sum(self.data_alice)}\n'
                      f'Alice\'s message for Bob is {str_result}\n')
        verify_output(int(str_result, 2))
        print('Computation completed, all the information are in the file.')


def main(party):
    """
    It decides if execute Alice or Bob machinery, or if output the table's structure
    :param party: the decision is based on this, it can be alice, bob or table.
    :return: None.
    """
    circuit_path = 'circuit/add.json'
    if party == 'alice':
        Sender(circuit_path).start()
    elif party == 'bob':
        Receiver().listen()
    elif party == "table":
        LocalTest(circuit_path, print_mode='table').start()


def init():
    """
    It collects the arguments to pass to the main function, which is then called.
    :return: None.
    """
    parser = argparse.ArgumentParser(description="Run Yao protocol.")
    parser.add_argument("party",
                        choices=["alice", "bob", "table"],
                        help="The yao party to run.")
    main(party=parser.parse_args().party)


init()
