"""
This files contains some simple functions to be used in the main, there is no garbled circuit
logic here.
"""

ALICE_DATA_PATH = 'input/alice.txt'
BOB_DATA_PATH = 'input/bob.txt'


def read_input(path):
    """
    It reads a file content
    :param path: the path of the file to read.
    :return: It returns the file's data as a list.
    :raises: If the sum of the numbers contained in the file exceed 255.
    """
    with open(path, "r", encoding="utf-8") as file:
        input_data = list(map(int, file.readline().split()))
    if sum(input_data) > 255:
        raise Exception('The sum can not exceed the maximum value stored in 8 bit.')
    return input_data


def write_to_file(message='', clear=False):
    """
    It writes a message to a file, appending it to the previous content.
    :param message: the message to write.
    :param clear: if true it clears the file.
    :return: None.
    """
    with open('output/result.txt', 'a', encoding='UTF-8') as file:
        if clear:
            file.truncate(0)
        else:
            file.write(message)


def verify_output(result):
    """
    It verifies if the result of the sum from the garbled circuit is correct, comparing it to
    a simple sum computed without multiparty computation
    :param result: the sum to verify if is correct or not.
    :return: None.
    """
    sender_data = read_input(ALICE_DATA_PATH)
    receiver_data = read_input(BOB_DATA_PATH)
    if (sum(sender_data) + sum(receiver_data)) == result:
        write_to_file(f'The sum is correct and it is {result}.')
    else:
        write_to_file('The sum is {result} and it is incorrect.')
