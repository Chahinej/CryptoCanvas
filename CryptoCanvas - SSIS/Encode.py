import cv2
from Functions import *

info = input("Please enter the information to be hidden:")
print("Please note: For all subsequent keys, please enter any arrangement of 0~7, a total of 8 digits")
info_length = len(info)
info_list = list()
for word in range(info_length):
    info_list.append(0)  #Initialization information list
i = 0
for word in info:
    if ord(word) > 255:
        print("There are unsupported characters in the input sequence!")
        exit(1)
    info_list[i] = ord(word)
    i += 1
# print(info_list)
# The ascii value of each character corresponding to the information is stored in the list
binary_info_list = [[0 for i in range(8)] for j in range(info_length)]  # Initialize the binary information matrix, the upper limit of the ascii code is 255, and it is 8 columns
i = 0
j = 7
# Store the binary value corresponding to the information in the matrix
while i < info_length:
    while j > -1:
        binary_info_list[i][j] = info_list[i] % 2
        info_list[i] = (info_list[i] - binary_info_list[i][j]) // 2
        j -= 1
    i += 1
    j = 7
# print(binary_info_list)
i = 0
j = 0
# For the convenience of subsequent operations, to distinguish from the original 0 in the matrix, change all 0 values to 2
while j < info_length:
    while i < 8:
        if binary_info_list[j][i] == 0:
            binary_info_list[j][i] = 2
        i += 1
    j += 1
    i = 0
# print(binary_info_list)

# Image information reading
im_matrix = cv2.imread("test.png")
# Get the R value corresponding to each img pixel and store it in the matrix for LSB encryption
image_length = len(im_matrix)
image_pixels = img_red_to_matrix(im_matrix)

if info_length > image_length // 8:
    print("The image size is not large enough to accommodate the above information!")
    exit(1)
# convert to binary
image_pixels_binary = [[0 for i in range(8)] for j in range(image_length * 8)]  # 8 columns (RGB range 0~255)*8*len lines (maximum information length)
i = 7  # Compare with the number of columns in the original matrix (1 column in the original matrix = 8 columns in binary)
j = 0  # The row count of the original matrix (it is more appropriate to call the height in the new matrix here, and for the convenience of subsequent encryption with the information table, it is declared as a two-dimensional list)
k = 0  # Original matrix column count + new matrix row count
while j < image_length:
    while k < 8:
        while i > -1:
            image_pixels_binary[k + (8 * j)][i] = image_pixels[j][k] % 2  # Map a decimal matrix into a binary matrix
            image_pixels[j][k] = (image_pixels[j][k] - image_pixels_binary[k + (8 * j)][i]) // 2
            i -= 1
        k += 1
        i = 7
    j += 1
    k = 0

# Map a decimal matrix into a binary matrix
key1 = input("1st key (LSB):")
key_check(key1)
LSB_key = list()
# LSB key bitwise initialized into a list
for i in key1:
    LSB_key.append(int(i))
# print(LSB_key)
i = 0
j = 0
while j < info_length:
    for key_bit in LSB_key:
        if i > 7:
            i = 0
        image_pixels_binary[key_bit + (8 * j)][7] = binary_info_list[j][i]  # The last bit of the corresponding position in the pixel matrix is changed to store information
        i += 1
    j += 1
    i = 0
print("The LSB algorithm is executed!")

# The second round, pseudorandom noise encryption
signal_interleaved = stage_2(image_length)
print("A noisy signal has been generated!")

u = 0
v = 0
img_embedded = [[0 for i in range(8)] for j in range(image_length)]
# Multiplicative embedding of two matrices
while u < image_length:
    while v < 8:
        img_embedded[u][v] = image_pixels_binary[u][v] * signal_interleaved[u][v]
        v += 1
    u += 1
    v = 0

# Aliasing noise matrix and image matrix
img_interleaved = [[0 for i in range(8)] for j in range(image_length)]
key3 = input("3rd key (aliasing):")
key_check(key3)
length = len(key3)
key3_list = list()
for v in key3:
    key3_list.append(int(v))

interleaving(image_length, key3_list, img_interleaved, img_embedded)

print("Mixing done!")

# After processing, convert the matrix back to decimal
img_interleaved_decimal = [[0 for i in range(8)] for k in range(image_length)]
k = 0
i = 0
while k < image_length:
    for i in range(8):
        img_interleaved_decimal[k][i] = (img_interleaved[k][i]) * (2 ** 7)
        i += 1
    k += 1
    i = 0

# write back
for i in range(image_length):
    for j in range(8):
        im_matrix[i, j, 2] = img_interleaved_decimal[i][j]

cv2.imwrite("output.png", im_matrix)
print("OK!")
