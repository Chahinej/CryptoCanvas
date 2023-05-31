import re
from random import seed, gauss
from numpy import *


def key_check(__key):
    if (len(__key) != 8) or (not re.findall('^[0-7]+$', __key)):
        print("The key format is wrong!")
        exit(1)
    for i in __key:
        for j in __key[__key.index(i) + 1:]:
            if j == i:
                print("The key format is wrong!")
                exit(1)
    else:
        return


# The interleaving function required for the second and third rounds of encryption, according to the key reorganization matrix
def interleaving(length, password, b, c):
    j = 0
    while j < length:
        i = 0
        for pw in password:
            if i > 7:
                i = 0
            else:
                b[j][i] = c[j][pw]
            i += 1
            pw += 1
        j += 1


# AWGN noise generating function
def noise_generate(img_len):
    seed(1)  #Encryption and decryption random number seed should be consistent
    # The noise sequence should satisfy the Gaussian distribution, that is, the additive white Gaussian noise (AWGN) series
    series_temp = [gauss(0.0, 1.0) for i in range(img_len * 8)]
    series = reshape(series_temp, (img_len, 8))  # Recombined Noise Sequence Format
    mini = min(series_temp)
    z = series - mini
    maxi = z.max()
    key2_list = maxi / 2 ** 6
    audio = fix(z / key2_list)  # audio signal floor
    return audio / audio.max()


# According to the noise of the second stage of key generation, both encryption and decryption can be reused
def stage_2(image_len):
    seed(1)
    signal_AWGN = noise_generate(image_len)
    signal_interleaved = [[0 for i in range(8)] for j in range(image_len)]
    key2 = input("2nd key (AWGN):")
    key_check(key2)
    key2_list = list()
    for v in key2:
        key2_list.append(int(v))
    interleaving(image_len, key2_list, signal_interleaved, signal_AWGN)
    return signal_AWGN


def img_red_to_matrix(im_matrix):
    image_len = len(im_matrix)
    # Get the R value corresponding to each img pixel and store it in the matrix for LSB encryption
    image_pixels = [[0 for i in range(8)] for j in range(image_len)]  # Corresponding to the information matrix, the number of columns is determined by the upper limit of the ascii code 255
    i = 0
    j = 0
    while j < image_len:
        while i < 8:
            image_pixels[j][i] = im_matrix[j, i, 2]
            i += 1
        j += 1
        i = 0
    return image_pixels
