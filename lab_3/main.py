from textwrap import wrap
import operator
from functools import reduce

KEY = '0E329232EA6D0D73'

# начальная перестановка IP
INITIAL_PERMUTATION_IP = [
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7,
    56, 48, 40, 32, 24, 16, 8, 0,
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6]

# конечная перестановка IP^-1
FINAL_PERMUTATION = [
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25,
    32, 0, 40, 8, 48, 16, 56, 24]

# S- блоки
S_BLOCKS = [
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
        0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
        4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
        15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],

    [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
        3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
        0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
        13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],

    [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
        13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
        13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
        1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],

    [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
        13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
        10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
        3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],

    [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
        14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
        4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
        11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],

    [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
        10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
        9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
        4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],

    [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
        13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
        1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
        6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],

    [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
        1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
        7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
        2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
]

# расширяющая перестановка Е
EXPANSION = [
    31, 0, 1, 2, 3, 4,
    3, 4, 5, 6, 7, 8,
    7, 8, 9, 10, 11, 12,
    11, 12, 13, 14, 15, 16,
    15, 16, 17, 18, 19, 20,
    19, 20, 21, 22, 23, 24,
    23, 24, 25, 26, 27, 28,
    27, 28, 29, 30, 31, 0]

# завершающая перестановка в функции шифрования Р
FINAL_P = [
    15, 6, 19, 20, 28, 11, 27, 16,
    0, 14, 22, 25, 4, 17, 30, 9,
    1, 7, 23, 13, 31, 26, 2, 8,
    18, 12, 29, 5, 21, 10, 3, 24]

# начальная перестановка В
INITIAL_PERMUTATION_B = [
    56, 48, 40, 32, 24, 16, 8,
    0, 57, 49, 41, 33, 25, 17,
    9, 1, 58, 50, 42, 34, 26,
    18, 10, 2, 59, 51, 43, 35,
    62, 54, 46, 38, 30, 22, 14,
    6, 61, 53, 45, 37, 29, 21,
    13, 5, 60, 52, 44, 36, 28,
    20, 12, 4, 27, 19, 11, 3]

# сжимающая перестановка
COMPRESSION = [
    13, 16, 10, 23, 0, 4,
    2, 27, 14, 5, 20, 9,
    22, 18, 11, 3, 25, 7,
    15, 6, 26, 19, 12, 1,
    40, 51, 30, 36, 46, 54,
    29, 39, 50, 44, 32, 47,
    43, 48, 38, 55, 33, 52,
    45, 41, 49, 35, 28, 31]

# сдвиг Si
ROTATES = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

# конвертация из ASCII в 16СС-строку
def slice_mess(string):
    return [i.zfill(16) for i in wrap(''.join([hex(ord(j))[2:].zfill(2) for j in string]), 16)]

# конвертация из 16СС в 2СС
def to_bin(s):
    return ''.join([bin(int(i, 16))[2:].zfill(4) for i in s])

def permute(source, table):
    return ''.join([source[i] for i in table])

def XOR(arg_1, arg_2):
    return ''.join([str(int(i) ^ int(j)) for i, j in zip(arg_1, arg_2)])

def rotate_left(block, i):
    return bin(int(block, 2) << i & 0x0fffffff | int(block, 2) >> 28 - i)[2:].zfill(28)

def concatenate(args):
    return reduce(operator.iadd, args, [])

def round_key_gen(C_0, D_0):
    new_key = []

    for i in ROTATES:
        C_0 = rotate_left(C_0, i)
        D_0 = rotate_left(D_0, i)
        new_key.append(permute(C_0 + D_0, COMPRESSION))

    return new_key

def f(data, key):
    final = []

    for j, block in enumerate(wrap(XOR(permute(data, EXPANSION), key), 6)):
        temp_box = [
            S_BLOCKS[j][0:16],
            S_BLOCKS[j][16:32],
            S_BLOCKS[j][32:48],
            S_BLOCKS[j][48:64]]

        m = int(block[0] + block[-1], 2)
        l = int(block[1:-1], 2)

        final.append(bin(temp_box[m][l])[2:].zfill(4))

    return permute(''.join(final), FINAL_P)

def des(block, key_array):
    left, right = block[0: len(block) // 2], block[len(block) // 2:]

    for k_i in key_array:
        right, left = XOR(f(right, k_i), left), right

    return wrap(permute(right + left, FINAL_PERMUTATION), 8)

import sys


def read_bytes(path_to: str) -> bytearray:
    with open(path_to, 'rb') as f:
        return f.read()




def encrypt_bytes(data: bytearray) -> bytearray:
    result = []
    message = ' '.join([str(b) for b in data])

    for i in slice_mess(message):
        # перевод содержимого в биты
        bin_mess, bin_key = to_bin(i), to_bin(KEY)

        # перестановка
        permuted_key, permuted_block = permute(
            bin_key, INITIAL_PERMUTATION_B), permute(bin_mess, INITIAL_PERMUTATION_IP)

        # генерация раундовых ключей
        key_list = round_key_gen(
            permuted_key[: len(permuted_key) // 2], permuted_key[len(permuted_key) // 2:])

        result.append(''.join([hex(int(i, 2))[2:].zfill(2) for i in des(permuted_block, key_list)]))

    return (''.join(result)).encode()


def decrypt_bytes(data: bytearray) -> bytearray:
    result = []
    message = data.decode()

    for i in wrap(message, 16):
        bin_mess, bin_key = to_bin(i), to_bin(KEY)

        permuted_key, permuted_block = permute(
            bin_key, INITIAL_PERMUTATION_B), permute(bin_mess, INITIAL_PERMUTATION_IP)

        key_list = round_key_gen(
            permuted_key[: len(permuted_key) // 2], permuted_key[len(permuted_key) // 2:])

        result.append(''.join([hex(int(i, 2))[2:].zfill(2).upper()
                                for i in des(permuted_block, reversed(key_list))]))

    s = (''.join(concatenate(
           [[chr(int(j, 16)) for j in wrap(i, 2) if int(j, 16) != 0] for i in result]))).split(' ')

    return bytearray([int(c) for c in s])


def main_file():
    data = read_bytes(sys.argv[1])
    if sys.argv[2] == '0':
        data = encrypt_bytes(data)
    else:
        data = decrypt_bytes(data)

    with open('new_%s' % sys.argv[1], 'wb') as f:
        f.write(data)


if __name__ == '__main__':
    if len(sys.argv) > 2:
        main_file()
        exit()
    else:
        print("Error!")

