# finding neighbouring mines using try and except methods
def find_mines(buttons, x, y):
    # calculating the number of mines around by increment algorithm, using try and except blocks to make sure we don't call wrong indexes
    c = 0
    try:
        if buttons[x + 1][y].mine:
            c += 1
    except:
        pass
    if x - 1 != -1 and buttons[x - 1][y].mine:
        c += 1
    try:
        if buttons[x][y + 1].mine:
            c += 1
    except:
        pass
    if y - 1 != -1 and buttons[x][y - 1].mine:
        c += 1
    try:
        if buttons[x + 1][y + 1].mine:
            c += 1
    except:
        pass
    try:
        if y - 1 != -1 and buttons[x + 1][y - 1].mine:
            c += 1
    except:
        pass
    if x - 1 != -1 and y - 1 != -1 and buttons[x - 1][y - 1].mine:
        c += 1
    try:
        if x - 1 != -1 and buttons[x - 1][y + 1].mine:
            c += 1
    except:
        pass

    return c