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

    def __init__(self, data):
        super().__init__()
        self.data = read_input(data)

    def send_evaluation(self, entry):
        """
        TODO
        """
        circuit, pbits_out = entry["circuit"], entry["pbits_out"]
        garbled_tables = entry["garbled_tables"]
        b_wires = circuit.get("bob", [])

        print(f"Received {circuit['id']}")
        print(self.data)
        print(sum(self.data))
        bits_b = list(f"{sum(self.data):b}".zfill(8))
        bits_b = [int(i) for i in bits_b]
        print(bits_b)

        b_inputs_clear = {
            b_wires[i]: bits_b[i]
            for i in range(len(b_wires))
        }

        self.ot.send_result(circuit, garbled_tables, pbits_out,
                            b_inputs_clear)


class Sender(Alice):
    def __init__(self, input_sender, input_receiver, circuits):
        super().__init__(circuits)
        self.input_sender = input_sender
        self.input_receiver = input_receiver



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
