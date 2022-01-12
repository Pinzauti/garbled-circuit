"""
Francesco Pinzauti
"""
import argparse
from yao.garbler import Alice, Bob, LocalTest, logging


def main(
        party,
        circuit_path="circuit/add.json",
        print_mode="circuit",
        loglevel=logging.WARNING,
):
    """
    d
    """
    logging.getLogger().setLevel(loglevel)

    if party == "alice":
        alice = Alice(circuit_path, oblivious_transfer=True)
        alice.start()
    elif party == "bob":
        bob = Bob(oblivious_transfer=True)
        bob.listen()
    elif party == "local":
        local = LocalTest(circuit_path, print_mode=print_mode)
        local.start()
    else:
        logging.error(f"Unknown party '{party}'")


def init():
    """
    c
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
