"""
TODO
"""


def read_input(path):
    """
    TODO
    """
    with open(path, "r", encoding="utf-8") as file:
        input_data = list(map(int, file.readline().split()))
    if sum(input_data) > 255:
        raise Exception('The sum can not exceed the maximum value stored in 8 bit.')
    return input_data


def verify_output(result, alice_data_path, bob_data_path):
    """
    TODO
    """
    alice_data = read_input(alice_data_path)
    bob_data = read_input(bob_data_path)
    if (sum(alice_data) + sum(bob_data)) == result:
        print(f'The sum is correct and it is {result}.')
    else:
        print(f'The sum is {result} and it is incorrect.')
