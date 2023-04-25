directions = [[0 for _ in range(20)] for _ in range(20)]

a1 = 60
a2 = 30
a3 = 0
a4 = 330
a5 = 300
a6 = 270
a7 = 240
a8 = 210
a9 = 180
a10 = 150
a11 = 120
a12 = 90

# continuous blocks ================================================================================================

for x in range(7,16):
    for y in range(1,4):
        directions[x][y] = a9

for x in range(1,4):
    for y in range(4,13):
        directions[x][y] = a6

for x in range(4,14):
    for y in range(16,19):
        directions[x][y] = a3

for x in range(9,16):
    for y in range(13,16):
        directions[x][y] = a9

for x in range(4,7):
    for y in range(10,14):
        directions[x][y] = a12

for x in range(10,16):
    for y in range(4,8):
        directions[x][y] = a3

# top left zone =====================================================================================================

directions[6][1] = a9
directions[5][1] = a9
directions[4][1] = a8
directions[3][1] = a7
directions[2][1] = a6

directions[6][2] = a8
directions[5][2] = a7
directions[4][2] = a7
directions[3][2] = a7
directions[2][2] = a7
directions[1][2] = a6

directions[6][3] = a8
directions[5][3] = a8
directions[4][3] = a7
directions[3][3] = a7
directions[2][3] = a6
directions[1][3] = a6

directions[5][4] = a7
directions[4][4] = a7

# bottom left zone ===================================================================================================

directions[1][13] = a6
directions[1][14] = a5
directions[1][15] = a5
directions[1][16] = a4
directions[1][17] = a3

directions[2][13] = a5
directions[2][14] = a5
directions[2][15] = a4
directions[2][16] = a4
directions[2][17] = a4
directions[2][18] = a3

directions[3][13] = a5
directions[3][14] = a4
directions[3][15] = a4
directions[3][16] = a4
directions[3][17] = a3
directions[3][18] = a3

directions[4][15] = a4

# bottom right zone =======================================================================================================

directions[14][16] = a5
directions[14][17] = a3
directions[14][18] = a3

directions[15][16] = a5
directions[15][17] = a3
directions[15][18] = a3

directions[16][13] = a9
directions[16][14] = a9
directions[16][17] = a2
directions[16][18] = a2

directions[17][13] = a9
directions[17][14] = a11
directions[17][15] = a12
directions[17][16] = a1
directions[17][17] = a2
directions[17][18] = a1

directions[18][14] = a10
directions[18][15] = a11
directions[18][16] = a12
directions[18][17] = a12
directions[18][18] = a1

directions[19][16] = a11
directions[19][16] = a11

# middle zone =========================================================================================================

directions[4][7] = a1
directions[4][8] = a1
directions[4][9] = a1

directions[5][5] = a3
directions[5][6] = a2
directions[5][7] = a1
directions[5][8] = a1
directions[5][9] = a1
directions[5][14] = a12

directions[6][4] = a3
directions[6][5] = a3
directions[6][6] = a2
directions[6][7] = a2
directions[6][8] = a1
directions[6][9] = a12
directions[6][14] = a11
directions[6][15] = a11

directions[7][4] = a3
directions[7][5] = a3
directions[7][6] = a3
directions[7][7] = a2
directions[7][8] = a1
directions[7][9] = a12
directions[7][10] = a12
directions[7][11] = a11
directions[7][12] = a11
directions[7][13] = a11
directions[7][14] = a11
directions[7][15] = a10

directions[8][4] = a3
directions[8][5] = a3
directions[8][6] = a3
directions[8][7] = a2
directions[8][12] = a10
directions[8][13] = a10
directions[8][14] = a10
directions[8][15] = a9

directions[9][4] = a3
directions[9][5] = a3
directions[9][6] = a3
directions[9][7] = a2

# top right zone =====================================================================================================

directions[16][1] = a9
directions[16][2] = a10
directions[16][3] = a10
directions[16][4] = a12
directions[16][5] = a2
directions[16][6] = a2
directions[16][7] = a1

directions[17][1] = a9
directions[17][2] = a10
directions[17][3] = a11
directions[17][4] = a12
directions[17][5] = a1
directions[17][6] = a1

directions[18][2] = a10
directions[18][3] = a11
directions[18][4] = a12
directions[18][5] = a1


