a1 = 60
a1_2 = 15
a2 = 30
a3 = 0
a4 = 320
a5 = 300
a6 = 270
a7 = 240
a8 = 210
a8_2 = 195
a9 = 180
a10 = 150
a11 = 130
a12 = 90

directions = [[a3 for _ in range(40)] for _ in range(40)]

# continuous blocks ================================================================================================

# for x in range(7,16):
#     for y in range(1,4):
#         directions[x][y] = a9
for x in range(14, 32):
    for y in range(2, 8):
        directions[x][y] = a9

# for x in range(1,4):
#     for y in range(4,13):
#         directions[x][y] = a6
for x in range(2, 8):
    for y in range(8, 26):
        directions[x][y] = a6

# for x in range(4,14):
#     for y in range(16,19):
#         directions[x][y] = a3
for x in range(8, 28):
    for y in range(32, 38):
        directions[x][y] = a3

# for x in range(9,16):
#     for y in range(13,16):
#         directions[x][y] = a9
for x in range(18, 32):
    for y in range(26, 32):
        directions[x][y] = a9

# for x in range(4,7):
#     for y in range(10,14):
#         directions[x][y] = a12
for x in range(8, 14):
    for y in range(20, 28):
        directions[x][y] = a12

# for x in range(10,16):
#     for y in range(4,8):
#         directions[x][y] = a3
for x in range(20, 32):
    for y in range(8, 16):
        directions[x][y] = a3

# top left zone =====================================================================================================

# directions[6][1] = a9
for x in range(12, 14):
    for y in range(2, 4):
        directions[x][y] = a9
# directions[5][1] = a9
for x in range(10, 12):
    for y in range(2, 4):
        directions[x][y] = a9
# directions[4][1] = a8
for x in range(8, 10):
    for y in range(2, 4):
        directions[x][y] = a8
# directions[3][1] = a7
for x in range(6, 8):
    for y in range(2, 4):
        directions[x][y] = a7
# directions[2][1] = a6
for x in range(4, 6):
    for y in range(2, 4):
        directions[x][y] = a6

# directions[6][2] = a9
for x in range(12, 14):
    for y in range(4, 6):
        directions[x][y] = a9
# directions[5][2] = a9
for x in range(10, 12):
    for y in range(4, 6):
        directions[x][y] = a9
# directions[4][2] = a8
for x in range(8, 10):
    for y in range(4, 6):
        directions[x][y] = a8
# directions[3][2] = a7
for x in range(6, 8):
    for y in range(4, 6):
        directions[x][y] = a7
# directions[2][2] = a7
for x in range(4, 6):
    for y in range(4, 6):
        directions[x][y] = a7
# directions[1][2] = a6
for x in range(2, 4):
    for y in range(4, 6):
        directions[x][y] = a6

# directions[6][3] = a9
for x in range(12, 14):
    for y in range(6, 8):
        directions[x][y] = a9
# directions[5][3] = a9
for x in range(10, 12):
    for y in range(6, 8):
        directions[x][y] = a9
# directions[4][3] = a8
for x in range(8, 10):
    for y in range(6, 8):
        directions[x][y] = a8
# directions[3][3] = a7
for x in range(6, 8):
    for y in range(6, 8):
        directions[x][y] = a7
# directions[2][3] = a6
for x in range(4, 6):
    for y in range(6, 8):
        directions[x][y] = a6
# directions[1][3] = a6
for x in range(2, 4):
    for y in range(6, 8):
        directions[x][y] = a6

# directions[5][4] = a8
for x in range(10, 12):
    for y in range(8, 10):
        directions[x][y] = a8
# directions[4][4] = a8
for x in range(8, 10):
    for y in range(8, 10):
        directions[x][y] = a8
# directions[4][5] = a8
for x in range(8, 10):
    for y in range(10, 12):
        directions[x][y] = a8

# bottom left zone ===================================================================================================

# directions[1][13] = a6
for x in range(2, 4):
    for y in range(26, 28):
        directions[x][y] = a6
# directions[1][14] = a5
for x in range(2, 4):
    for y in range(28, 30):
        directions[x][y] = a5
# directions[1][15] = a5
for x in range(2, 4):
    for y in range(30, 32):
        directions[x][y] = a5
# directions[1][16] = a4
for x in range(2, 4):
    for y in range(32, 34):
        directions[x][y] = a4
# directions[1][17] = a3
for x in range(2, 4):
    for y in range(34, 36):
        directions[x][y] = a3

# directions[2][13] = a5
for x in range(4, 6):
    for y in range(26, 28):
        directions[x][y] = a5
# directions[2][14] = a5
for x in range(4, 6):
    for y in range(28, 30):
        directions[x][y] = a5
# directions[2][15] = a4
for x in range(4, 6):
    for y in range(30, 32):
        directions[x][y] = a4
# directions[2][16] = a3
for x in range(4, 6):
    for y in range(32, 34):
        directions[x][y] = a3
# directions[2][17] = a3
for x in range(4, 6):
    for y in range(34, 36):
        directions[x][y] = a3
# directions[2][18] = a1
for x in range(4, 6):
    for y in range(36, 38):
        directions[x][y] = a1

# directions[3][13] = a5
for x in range(6, 8):
    for y in range(26, 28):
        directions[x][y] = a5
# directions[3][14] = a4
for x in range(6, 8):
    for y in range(28, 30):
        directions[x][y] = a4
# directions[3][15] = a4
for x in range(6, 8):
    for y in range(30, 32):
        directions[x][y] = a4
# directions[3][16] = a3
for x in range(6, 8):
    for y in range(32, 34):
        directions[x][y] = a3
# directions[3][17] = a3
for x in range(6, 8):
    for y in range(34, 36):
        directions[x][y] = a3
# directions[3][18] = a1
for x in range(6, 8):
    for y in range(36, 38):
        directions[x][y] = a1

# directions[4][14] = a1
for x in range(8, 10):
    for y in range(28, 30):
        directions[x][y] = a1
# directions[4][15] = a5
for x in range(8, 10):
    for y in range(30, 32):
        directions[x][y] = a5
# directions[5][15] = a12
for x in range(10, 12):
    for y in range(30, 32):
        directions[x][y] = a5

# bottom right zone =======================================================================================================

# directions[14][16] = a3
for x in range(28, 30):
    for y in range(32, 34):
        directions[x][y] = a3
# directions[14][17] = a3
for x in range(28, 30):
    for y in range(34, 36):
        directions[x][y] = a3
# directions[14][18] = a1
for x in range(28, 30):
    for y in range(36, 38):
        directions[x][y] = a1

# directions[15][16] = a5
for x in range(30, 32):
    for y in range(32, 34):
        directions[x][y] = a5
# directions[15][17] = a3
for x in range(30, 32):
    for y in range(34, 36):
        directions[x][y] = a3
# directions[15][18] = a1
for x in range(30, 32):
    for y in range(36, 38):
        directions[x][y] = a1

# directions[16][13] = a9
for x in range(32, 34):
    for y in range(26, 28):
        directions[x][y] = a9
# directions[16][14] = a9
for x in range(32, 34):
    for y in range(28, 30):
        directions[x][y] = a9
# directions[16][17] = a2
for x in range(32, 34):
    for y in range(34, 36):
        directions[x][y] = a2
# directions[16][18] = a2
for x in range(32, 34):
    for y in range(36, 38):
        directions[x][y] = a2

# directions[17][13] = a9
for x in range(34, 36):
    for y in range(26, 28):
        directions[x][y] = a9
# directions[17][14] = a9
for x in range(34, 36):
    for y in range(24, 26):
        directions[x][y] = a9
# directions[17][15] = a12
for x in range(34, 36):
    for y in range(30, 32):
        directions[x][y] = a12
# directions[17][16] = a1
for x in range(34, 36):
    for y in range(32, 34):
        directions[x][y] = a1
# directions[17][17] = a12
for x in range(34, 36):
    for y in range(34, 36):
        directions[x][y] = a12
# directions[17][18] = a12
for x in range(34, 36):
    for y in range(36, 38):
        directions[x][y] = a12

# directions[18][14] = a9
for x in range(36, 38):
    for y in range(28, 30):
        directions[x][y] = a9
# directions[18][15] = a11
for x in range(36, 38):
    for y in range(30, 32):
        directions[x][y] = a11
# directions[18][16] = a11
for x in range(36, 38):
    for y in range(32, 34):
        directions[x][y] = a11
# directions[18][17] = a11
for x in range(36, 38):
    for y in range(34, 36):
        directions[x][y] = a11
# directions[18][18] = a11
for x in range(36, 38):
    for y in range(36, 38):
        directions[x][y] = a11

# directions[19][16] = a11
for x in range(38, 40):
    for y in range(32, 34):
        directions[x][y] = a11

# middle zone =========================================================================================================

# directions[4][7] = a1
for x in range(8, 10):
    for y in range(14, 16):
        directions[x][y] = a1
# directions[4][8] = a1
for x in range(8, 10):
    for y in range(16, 18):
        directions[x][y] = a1
# directions[4][9] = a1
for x in range(8, 10):
    for y in range(18, 20):
        directions[x][y] = a1

# directions[5][5] = a3
for x in range(10, 12):
    for y in range(10, 12):
        directions[x][y] = a3
# directions[5][6] = a2
for x in range(10, 12):
    for y in range(12, 14):
        directions[x][y] = a2
# directions[5][7] = a1
for x in range(10, 12):
    for y in range(14, 16):
        directions[x][y] = a1
# directions[5][8] = a1
for x in range(10, 12):
    for y in range(16, 18):
        directions[x][y] = a1
# directions[5][9] = a1
for x in range(10, 12):
    for y in range(18, 20):
        directions[x][y] = a1
# directions[5][14] = a12
for x in range(10, 12):
    for y in range(28, 30): 
        directions[x][y] = a12

# directions[6][4] = a3
for x in range(12, 14):
    for y in range(8, 10):
        directions[x][y] = a3
# directions[6][5] = a3
for x in range(12, 14):
    for y in range(10, 12):
        directions[x][y] = a3
# directions[6][6] = a2
for x in range(12, 14):
    for y in range(12, 14):
        directions[x][y] = a2
# directions[6][7] = a2
for x in range(12, 14):
    for y in range(14, 16):
        directions[x][y] = a2
# directions[6][8] = a1
for x in range(12, 14):
    for y in range(16, 18):
        directions[x][y] = a1
# directions[6][9] = a12
for x in range(12, 14):
    for y in range(18, 20):
        directions[x][y] = a12
# directions[6][14] = a12
for x in range(12, 14):
    for y in range(28, 30):
        directions[x][y] = a12
# directions[6][15] = a12
for x in range(12, 14):
    for y in range(30, 32):
        directions[x][y] = a12

# directions[7][4] = a3
for x in range(14, 16):
    for y in range(8, 10):
        directions[x][y] = a3
# directions[7][5] = a3
for x in range(14, 16):
    for y in range(10, 12):
        directions[x][y] = a3
# directions[7][6] = a3
for x in range(14, 16):
    for y in range(12, 14):
        directions[x][y] = a3
# directions[7][7] = a2
for x in range(14, 16):
    for y in range(14, 16):
        directions[x][y] = a2
# directions[7][8] = a12
for x in range(14, 16):
    for y in range(16, 18):
        directions[x][y] = a12
# directions[7][9] = a11
for x in range(14, 16):
    for y in range(18, 20):
        directions[x][y] = a11
# directions[7][10] = a10
for x in range(14, 16):
    for y in range(20, 22):
        directions[x][y] = a10
# directions[7][11] = a10
for x in range(14, 16):
    for y in range(22, 24):
        directions[x][y] = a10
# directions[7][12] = a11
for x in range(14, 16):
    for y in range(24, 26):
        directions[x][y] = a11
# directions[7][13] = a11
for x in range(14, 16):
    for y in range(26, 28):
        directions[x][y] = a11
# directions[7][14] = a11
for x in range(14, 16):
    for y in range(28, 30):
        directions[x][y] = a11
# directions[7][15] = a10
for x in range(14, 16):
    for y in range(30, 32):
        directions[x][y] = a10

# directions[8][4] = a3
for x in range(16, 18):
    for y in range(8, 10):
        directions[x][y] = a3
# directions[8][5] = a3
for x in range(16, 18):
    for y in range(10, 12):
        directions[x][y] = a3
# directions[8][6] = a3
for x in range(16, 18):
    for y in range(12, 14):
        directions[x][y] = a3
# directions[8][7] = a2
for x in range(16, 18):
    for y in range(14, 16):
        directions[x][y] = a2
# directions[8][12] = a10
for x in range(16, 18):
    for y in range(24, 26):
        directions[x][y] = a10
# directions[8][13] = a10
for x in range(16, 18):
    for y in range(26, 28):
        directions[x][y] = a10
# directions[8][14] = a10
for x in range(16, 18):
    for y in range(28, 30):
        directions[x][y] = a10
# directions[8][15] = a9
for x in range(16, 18):
    for y in range(30, 32):
        directions[x][y] = a9

# directions[9][4] = a3
for x in range(18, 20):
    for y in range(8, 10):
        directions[x][y] = a3
# directions[9][5] = a3
for x in range(18, 20):
    for y in range(10, 12):
        directions[x][y] = a3
# directions[9][6] = a3
for x in range(18, 20):
    for y in range(12, 14):
        directions[x][y] = a3
# directions[9][7] = a2
for x in range(18, 20):
    for y in range(14, 16):
        directions[x][y] = a2

# top right zone =====================================================================================================

# directions[14][7] = a2
for x in range(28, 30):
    for y in range(14, 16):
        directions[x][y] = a2
# directions[15][6] = a12
for x in range(30, 32):
    for y in range(12, 14):
        directions[x][y] = a12
# directions[15][7] = a12
for x in range(30, 32):
    for y in range(14, 16):
        directions[x][y] = a12
# directions[16][6] = a12
for x in range(32, 34):
    for y in range(12, 14):
        directions[x][y] = a12
# directions[16][7] = a1
for x in range(32, 34):
    for y in range(14, 16):
        directions[x][y] = a1
# directions[17][6] = a12
for x in range(34, 36):
    for y in range(12, 14):
        directions[x][y] = a12
# directions[17][7] = a12
for x in range(34, 36):
    for y in range(14, 16):
        directions[x][y] = a12
# directions[18][6] = a12
for x in range(36, 38):
    for y in range(12, 14):
        directions[x][y] = a12
# directions[18][5] = a12
for x in range(36, 38):
    for y in range(10, 12):
        directions[x][y] = a12
# directions[19][5] = a11
for x in range(38, 40):
    for y in range(10, 12):
        directions[x][y] = a11
# directions[19][4] = a11
for x in range(38, 40):
    for y in range(8, 10):
        directions[x][y] = a11
# directions[19][3] = a10
for x in range(38, 40):
    for y in range(6, 8):
        directions[x][y] = a10
# directions[18][2] = a9
for x in range(36, 38):
    for y in range(4, 6):
        directions[x][y] = a9
# directions[18][1] = a9
for x in range(36, 38):
    for y in range(2, 4):
        directions[x][y] = a9

# directions[16][1] = a9
for x in range(32, 34):
    for y in range(2, 4):
        directions[x][y] = a9
# directions[16][2] = a10
for x in range(32, 34):
    for y in range(4, 6):
        directions[x][y] = a10
# directions[16][3] = a10
for x in range(32, 34):
    for y in range(6, 8):
        directions[x][y] = a10
# directions[16][4] = a12
for x in range(32, 34):
    for y in range(8, 10):
        directions[x][y] = a12
# directions[16][5] = a12
for x in range(32, 34):
    for y in range(10, 12):
        directions[x][y] = a12
# directions[16][6] = a12
for x in range(32, 34):
    for y in range(12, 14):
        directions[x][y] = a12
# directions[16][7] = a1
for x in range(32, 34):
    for y in range(14, 16):
        directions[x][y] = a1

# directions[17][1] = a9
for x in range(34, 36):
    for y in range(2, 4):
        directions[x][y] = a9
# directions[17][2] = a10
for x in range(34, 36):
    for y in range(4, 6):
        directions[x][y] = a10
# directions[17][3] = a11
for x in range(34, 36):
    for y in range(6, 8):
        directions[x][y] = a11
# directions[17][4] = a12
for x in range(34, 36):
    for y in range(8, 10):
        directions[x][y] = a12
# directions[17][5] = a12
for x in range(34, 36):
    for y in range(10, 12):
        directions[x][y] = a12
# directions[17][6] = a12
for x in range(34, 36):
    for y in range(12, 14):
        directions[x][y] = a12

# directions[18][2] = a9
for x in range(36, 38):
    for y in range(4, 6):
        directions[x][y] = a9
# directions[18][3] = a9
for x in range(36, 38):
    for y in range(6, 8):
        directions[x][y] = a9
# directions[18][4] = a11
for x in range(36, 38):
    for y in range(8, 10):
        directions[x][y] = a11
# directions[18][5] = a12
for x in range(36, 38):
    for y in range(10, 12):
        directions[x][y] = a12

# outside zone =====================================================================================================

# for x in range(0, 1):
#     for y in range(0, 19):
#         directions[x][y] = a4
for x in range(0, 2):
    for y in range(0, 38):
        directions[x][y] = a4

# for x in range(0, 20):
#     for y in range(19, 20):
#         directions[x][y] = a12
for x in range(0, 40):
    for y in range(38, 40):
        directions[x][y] = a12

# for x in range(19, 20):
#     for y in range(0, 20):
#         directions[x][y] = a9
for x in range(38, 40):
    for y in range(0, 40):
        directions[x][y] = a9

# for x in range(8, 20):
#     for y in range(10, 13):
#         directions[x][y] = a6
for x in range(16, 40):
    for y in range(20, 26):
        directions[x][y] = a6

# for x in range(8, 20):
#     for y in range(7, 10):
#         directions[x][y] = a12
for x in range(16, 40):
    for y in range(14, 20):
        directions[x][y] = a12

# for x in range(0, 20):
#     for y in range(0, 1):
#         directions[x][y] = a6
for x in range(0, 40):
    for y in range(0, 2):
        directions[x][y] = a6


# directions[18][13] = a9
for x in range(36, 38):
    for y in range(26, 28):
        directions[x][y] = a9


# arrow shape =============================================================================================================

# top right
# for x in range(5, 20):
#     directions[x][1] = a7
#     directions[x][3] = a11
for x in range(10, 40):
    for y in range(2, 4):
        directions[x][y] = a7
    for y in range(6, 8):
        directions[x][y] = a11

# left
# for y in range(2, 14):
#     directions[1][y] = a5
#     directions[3][y] = a7
for y in range(4, 28):
    for x in range(2, 4):
        directions[x][y] = a5
    for x in range(6, 8):
        directions[x][y] = a7

# bottom
# directions[15][16] = a4
for y in range(30, 32):
    for x in range(32, 34):
        directions[x][y] = a4
# directions[15][17] = a2
for y in range(30, 32):
    for x in range(34, 36):
        directions[x][y] = a2
# directions[16][16] = a3
for y in range(32, 34):
    for x in range(32, 34):
        directions[x][y] = a3
# directions[16][17] = a2
for y in range(32, 34):
    for x in range(34, 36):
        directions[x][y] = a2

# for x in range(4, 14):
#     directions[x][16] = a3
#     directions[x][18] = a1
for x in range(8, 28):
    for y in range(32, 34):
        directions[x][y] = a3
    for y in range(36, 38):
        directions[x][y] = a1


# center
# for x in range(8, 17):
#     directions[x][13] = a8
#     directions[x][15] = a11
for x in range(16, 34):
    for y in range(26, 28):
        directions[x][y] = a8
    for y in range(30, 32):
        directions[x][y] = a11

# for y in range(7, 14):
#     directions[4][y] = a2
for y in range(14, 28):
    for x in range(8, 10):
        directions[x][y] = a2

# for x in range(6, 16):
#     directions[x][4] = a5
#     directions[x][6] = a3
for x in range(12, 32):
    for y in range(8, 10):
        directions[x][y] = a5
    for y in range(12, 14):
        directions[x][y] = a3

# for x in range(4,6):
#     for y in range(6,8):
#         directions[x][y] = a3
for x in range(8, 12):
    for y in range(12, 16):
        directions[x][y] = a3

# directions[1][2] = a5
for x in range(2, 4):
    for y in range(4, 6):
        directions[x][y] = a5

# for x in range(6,8):
#     directions[x][15] = a11
for x in range(12, 16):
    for y in range(30, 32):
        directions[x][y] = a11

# Left side (converge to middle)
# for y in range(4, 15):
#     directions[1][y] = a5
# for y in range(8, 30):
#     for x in range(2, 4):
#         directions[x][y] = a5 

# directions[1][1] = a6
for x in range(2, 4):
    for y in range(2, 4):
        directions[x][y] = a6
# directions[13][16] = a4
for x in range(26, 28):
    for y in range(32, 34):
        directions[x][y] = a4
# directions[14][16] = a4
for x in range(28, 30):
    for y in range(32, 34):
        directions[x][y] = a4
# directions[15][4] = a3
for x in range(30, 32):
    for y in range(28, 30):
        directions[x][y] = a3
# directions[15][5] = a12
for x in range(30, 32):
    for y in range(30, 32):
        directions[x][y] = a12
# directions[15][6] = a12
for x in range(30, 32):
    for y in range(12, 14):
        directions[x][y] = a12
# directions[16][17] = a12
for x in range(32, 34):
    for y in range(34, 36):
        directions[x][y] = a12
# directions[16][18] = a12
for x in range(32, 34):
    for y in range(36, 38):
        directions[x][y] = a12

for x in range(34, 36):
    for y in range(8, 10):
        directions[x][y] = a11

for x in range(36, 38):
    for y in range(10, 12):
        directions[x][y] = a11

for x in range(18, 36):
    for y in range(28, 30):
        directions[x][y] = a9

for x in range(34, 36):
    for y in range(30, 34):
        directions[x][y] = a12

for x in range(10, 11):
    for y in range(11, 30):
        directions[x][y] = a4

for x in range(4, 32):
    for y in range(36, 38):
        directions[x][y] = a1

for x in range(34, 36):
    for y in range(30, 36):
        directions[x][y] = a11

for y in range(2, 4):
    for x in range(6, 36):
        directions[x][y] = a8_2

for x in range(32, 34):
    for y in range(8, 10):
        directions[x][y] = a11

for x in range(32, 38):
    for y in range(4, 6):
        directions[x][y] = a9

for x in range(4, 6):
    for y in range(4, 6):
        directions[x][y] = a6

for x in range(6, 8):
    for y in range(2, 4):
        directions[x][y] = a7

for x in range(26, 30):
    for y in range(32, 34):
        directions[x][y] = a3

for x in range(10, 11):
    for y in range(11, 29):
        directions[x][y] =  a1