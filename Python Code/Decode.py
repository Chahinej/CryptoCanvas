import cv2
from Functions import *

im_matrix = cv2.imread("output.png")
img_length = len(im_matrix)
img_red = img_red_to_matrix(im_matrix);

# Convert the corresponding information bits to binary and get them into the list
info_matrix = [[0 for i in range(8)] for k in range(img_length)]
k = 0
i = 0
while k < img_length:
    for i in range(8):
        # if i == 0:
        # img_red[k][i] = -1 * (256 - img_red[k][i])
        info_matrix[k][i] = (img_red[k][i]) / (2 ** 7)
        i += 1
    k += 1
    i = 0

# to reproduce the same aliasing matrix
img_before_interleaving = [[0 for i in range(8)] for j in range(img_length)]
key3 = input("3rd key (aliasing):")
key_check(key3)
key3_list = list()
for v in key3:
    key3_list.append(int(v))

# Use interleave in reverse
j = 0
while j < img_length:
    i = 0
    for pw in key3_list:
        if i > 7:
            i = 0
        else:
            img_before_interleaving[j][pw] = info_matrix[j][i]
        i += 1
        pw += 1
    j += 1

print("Aliased Encryption Unwrapped")

signal = stage_2(img_length)
print("The noisy signal has been reconstructed!")

# Restoration Matrix Noise Multiplication Embedded Processing
p = 0
o = 0
img_matrix_after_LSB = [[0 for i in range(8)] for j in range(img_length)]
while o < img_length:
    while p < 8:
        if signal[o][p] != 0:
            img_matrix_after_LSB[o][p] = int(img_before_interleaving[o][p] // signal[o][p])
        p += 1
    o += 1
    p = 0
print("Matrix embeddings are unwrapped!")

# restore LSB
key1 = input("1st key (LSB):")
key_check(key1)
key1_list = list()
for i in key1:
    key1_list.append(int(i))
img_before_LSB = [[0 for i in range(8)] for j in range(img_length // 8)]
j = 0
while j < img_length // 8:
    i = 0
    for pw in key1_list:
        if i > 7:
            i = 0
        if j >= 0:
            img_before_LSB[j][i] = img_matrix_after_LSB[pw + (8 * j)][7]
        i += 1
    j += 1
print ("LSB has been restored!")

word_num = 0
while 1:
    if 0 in img_before_LSB[word_num]:
        break
    else:
        word_num += 1  # No more information is stored from the line containing 0

# When encrypting, convert all 0 to -1, and it should be unlocked when decrypting
i = 0
j = 0
while j < word_num:
    while i < 8:
        if img_before_LSB[j][i] == 2:
            img_before_LSB[j][i] = 0
        else:
            img_before_LSB[j][i] = 1
        i += 1
    j += 1
    i = 0

img_demical = [0 for i in range(img_length // 8)]

i = 7
j = 0
# Convert from binary back to decimal
while j < word_num:
    word_asc = 0
    while i > -1:
        word_asc += img_before_LSB[j][i] * (2 ** (7 - i))
        i -= 1
    img_demical[j] = word_asc
    j += 1
    i = 7
i = 0
j = 0

result_list=""
for i in range(word_num):
    if img_demical[i] == 92:
        break
    else:
        result_list += (chr(img_demical[i]))
print("decryption result:"+result_list)