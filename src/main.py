"""
Francesco Pinzauti
"""
import argparse
from yao.garbler import Alice, Bob, LocalTest, logging


def read_input(path):
    """
    TODO
    """
    with open(path, "r", encoding="utf-8") as file:
        input_data = list(map(int, file.readline().split()))
    return input_data


class Receiver(Bob):
    """
    TODO
    """

    def __init__(self, data_receiver):
        super().__init__()
        self.data_receiver = read_input(data_receiver)

    def send_evaluation(self, entry):
        """
        TODO
        """
        circuit, pbits_out = entry["circuit"], entry["pbits_out"]
        garbled_tables = entry["garbled_tables"]
        b_wires = circuit.get("bob", [])

        print(f"Received {circuit['id']}")
        print(self.data_receiver)
        print(sum(self.data_receiver))
        bits_b = list(f"{sum(self.data_receiver):b}".zfill(8))
        bits_b = [int(i) for i in bits_b]
        print(bits_b)

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

    def __init__(self, data_sender, data_receiver, circuits):
        super().__init__(circuits)
        self.data_sender = read_input(data_sender)
        self.data_receiver = read_input(data_receiver)

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

        bits_a = list(f"{sum(self.data_sender):b}".zfill(8))
        bits_a = [int(i) for i in bits_a]

        bits = format(sum(self.data_sender), 'b').zfill(len(a_wires))

        # Map Alice's wires to (key, encr_bit)
        for i in range(len(a_wires)):
            a_inputs[a_wires[i]] = (keys[a_wires[i]][bits_a[i]],
                                    pbits[a_wires[i]] ^ bits_a[i])

        # Send Alice's encrypted inputs and keys to Bob
        result = self.ot.get_result(a_inputs, b_keys)

        # Format output
        str_bits_a = ' '.join(bits[:len(a_wires)])
        str_bits_b = ' '.join(bits[len(a_wires):])
        str_result = ' '.join([str(result[w]) for w in outputs])

        print(f"  Alice{a_wires} = {str_bits_a} "
              f"Bob{b_wires} = {str_bits_b}  "
              f"Outputs{outputs} = {str_result}")
        print()



def main(
        party,
        circuit_path='circuit/add.json',
        print_mode='circuit',
        loglevel=logging.WARNING,
):
    """
    TODO
    """
    logging.getLogger().setLevel(loglevel)
    if party == 'alice':
        alice = Sender("input/alice.txt", "input/bob.txt", circuit_path)
        alice.start()
    elif party == 'bob':
        bob = Receiver('input/bob.txt')
        bob.listen()
    elif party == "local":
        local = LocalTest(circuit_path, print_mode=print_mode)
        local.start()
    else:
        logging.error(f"Unknown party '{party}'")


def init():
    """
    TODO
    """
    loglevels = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL
    }

    parser = argparse.ArgumentParser(description="Run Yao protocol.")
    parser.add_argument("party",
                        choices=["alice", "bob", "local."],
                        help="The yao party to run")
    parser.add_argument(
        "-m",
        metavar="mode",
        choices=["circuit", "table"],
        default="circuit",
        help="The print mode for local tests (default 'circuit').")
    parser.add_argument("-l",
                        "--loglevel",
                        metavar="level",
                        choices=loglevels.keys(),
                        default="warning",
                        help="The log level (default 'warning').")

    main(
        party=parser.parse_args().party,
        print_mode=parser.parse_args().m,
        loglevel=loglevels[parser.parse_args().loglevel],
    )


init()
