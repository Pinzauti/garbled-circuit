"""
TODO
"""

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


def write_to_file(message='', clear=False):
    """
    TODO
    """
    with open('output/result.txt', 'a', encoding='UTF-8') as file:
        if clear:
            file.truncate(0)
        else:
            file.write(message)


def verify_output(result):
    """
    TODO
    """
    sender_data = read_input(ALICE_DATA_PATH)
    receiver_data = read_input(BOB_DATA_PATH)
    if (sum(sender_data) + sum(receiver_data)) == result:
        write_to_file(f'The sum is correct and it is {result}.')
    else:
        write_to_file('The sum is {result} and it is incorrect.')