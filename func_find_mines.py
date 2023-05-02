# finding neighbouring mines using try and except methods
def find_mines(buttons, x, y, rows, cols):
    # calculating the number of mines around by increment algorithm, using try and except blocks to make sure we don't call wrong indexes
    c = 0
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if (x + i <= rows - 1) and (y + j <= cols - 1) and (y + j >= 0) and (x + i >= 0):
                if buttons[x + i][y + j].mine:
                    c += 1

    return c 
