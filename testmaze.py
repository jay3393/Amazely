groupings = []

for x in range(0, 100):
    for y in range(0, 100):
        grouping = (x, y)
        groupings.append([grouping])

print(groupings)

for x in range(len(groupings)):
    if (0,0) in groupings[x]:
        print(x)