
import pprint 

board = [[0 for i in range(19)] for j in range(19)]

b = []
### Horizontal 
for r in range(19):
	for c in range(15):
		b.append([(r,c),(r,c+1),(r,c+2),(r,c+3),(r,c+4)])

### Vertical 
for r in range(15):
	for c in range(19):
		b.append([(r,c),(r+1,c),(r+2,c),(r+3,c),(r+4,c)])

### Up 
for r in range(15):
	for c in range(15):
		b.append([(r,c),(r+1,c+1),(r+2,c+2),(r+3,c+3),(r+4,c+4)])

### Down 
for r in range(15):
	for c in range(4,19):
		b.append([(r,c),(r+1,c-1),(r+2,c-2),(r+3,c-3),(r+4,c-4)])	

# 1020
# print(len(b))
# print(b)

### Dictionary of coordinates 
coord = {}
for i in range(19):
	for j in range(19):
		coord[(i,j)] = 0

# pprint.pprint(coord)


