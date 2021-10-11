def read_map(file_path):
    level = []
    with open(file_path, "r") as reader:
        for line in reader:
            data = [item.strip() for item in line.split(",")]
            level.append(data)

    y = 0
    for row in level:
        x = 0
        for tile in row:
            level[y][x] = int(float(level[y][x]))
            x += 1
        y += 1
    return level


def save_map(level, file_name):
    outfile = open(file_name, "w")

    for row in level:
        x = 0
        for tile in row:
            if x == 0:
                outfile.write(str(tile))
            else:
                if tile >= 10:
                    outfile.write(", " + str(tile))
                else:
                    outfile.write(",  " + str(tile))
            x += 1
        outfile.write("\n")

    outfile.close()