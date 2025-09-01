from image_finding import *
import math

def draw_arrow(img, start, end, color=(255,255,255), thickness=2, arrow_magnitude=15):
    """
    Draws a line with a proper arrowhead pointing towards `end`.
    """
    # Draw main line
    cv.line(img, start, end, color, thickness)

    # Compute direction
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    angle = math.atan2(dy, dx)

    # Arrowhead points
    x1 = int(end[0] - arrow_magnitude * math.cos(angle - math.pi/6))
    y1 = int(end[1] - arrow_magnitude * math.sin(angle - math.pi/6))
    x2 = int(end[0] - arrow_magnitude * math.cos(angle + math.pi/6))
    y2 = int(end[1] - arrow_magnitude * math.sin(angle + math.pi/6))

    # Draw arrowhead
    cv.line(img, (x1, y1), end, color, thickness)
    cv.line(img, (x2, y2), end, color, thickness)

'''
Priority order of casualties : Star-3(Highest), Triangle-2, Square-1(Lowest)
Priority order of emergency : Severe-3(Highest), Mild-2, Safe-1(Lowest)
Max capacity of rescue pads : Pink-3 casualties, Blue-4 casualties, Grey-2 casualties
'''
path = f"C:\\Users\\Prakhar Srivastava\\.vscode\\coding\\opencv\\photos\\3.jpg"
temp_paths = {"circle":"C:\\Users\\Prakhar Srivastava\\.vscode\\coding\\UAS\\circle.png","square":"C:\\Users\\Prakhar Srivastava\\.vscode\\coding\\UAS\\square.png","triangle":"C:\\Users\\Prakhar Srivastava\\.vscode\\coding\\UAS\\triangle.png","star":"C:\\Users\\Prakhar Srivastava\\.vscode\\coding\\UAS\\star.png"}


coordinates = wmap(path,temp_paths)
img_rgb = cv.imread("C:\\Users\\Prakhar Srivastava\\.vscode\\coding\\UAS\\res.png")
for fav in coordinates:
        for i in range(len(coordinates[fav])):
            coordinates[fav][i] = (*coordinates[fav][i],img_rgb[coordinates[fav][i][1],coordinates[fav][i][0]].tolist()[::-1])



for fav in coordinates:
        for i in range(len(coordinates[fav])):
            if list(coordinates[fav][i]).pop()==[255,0,0]:
                coordinates[fav][i]=(coordinates[fav][i][0],coordinates[fav][i][1],'Red')
            if list(coordinates[fav][i]).pop()==[0,255,0]:
                coordinates[fav][i]=(coordinates[fav][i][0],coordinates[fav][i][1],'Green')
            if list(coordinates[fav][i]).pop()==[0,0,255]:
                coordinates[fav][i]=(coordinates[fav][i][0],coordinates[fav][i][1],'Blue')
            if list(coordinates[fav][i]).pop()==[255,255,0]:
                coordinates[fav][i]=(coordinates[fav][i][0],coordinates[fav][i][1],'Yellow')
            if list(coordinates[fav][i]).pop()==[128,128,128]:
                coordinates[fav][i]=(coordinates[fav][i][0],coordinates[fav][i][1],'Grey')
            if list(coordinates[fav][i]).pop()==[255,0,255]:
                coordinates[fav][i]=(coordinates[fav][i][0],coordinates[fav][i][1],'Pink')



# Extract list of casualties
casualty_list = []
for shape in ['star', 'triangle', 'square']:
    for x, y, emergency in coordinates.get(shape, []):
        casualty_list.append({'shape': shape, 'x': x, 'y': y, 'emergency': emergency})

#print('\ncasualty_list',casualty_list)

# Extract list of pads
pad_list = []
for x, y, color in coordinates.get('circle', []):
    pad_list.append({'name': color, 'x': x, 'y': y})

#print('\npad_list',pad_list)

# Build distance matrix: distance[i][j] = distance from casualty i to pad j
distance = [[0]*len(pad_list) for _ in range(len(casualty_list))]

for i, c in enumerate(casualty_list):
    for j, p in enumerate(pad_list):
        dx = p['x'] - c['x']
        dy = p['y'] - c['y']
        distance[i][j] = math.hypot(dx, dy)

# Optional: print
#for i, row in enumerate(distance):
    #print(f"\nCasualty {i} distances to pads:", row)

# Priority mapping
shape_score = {'star': 3, 'triangle': 2, 'square': 1}
emergency_score = {'red': 3, 'yellow': 2, 'green': 1}

# Compute priority score for each casualty
for c in casualty_list:
    c['priority'] = shape_score[c['shape'].lower()] * emergency_score[c['emergency'].lower()]

#print('\ncasualty_list',casualty_list)

# Sort casualties by priority desc, then emergency desc
casualty_list.sort(key=lambda c: (-c['priority'], -emergency_score[c['emergency'].lower()]))

print('\ncasualty_list',casualty_list)

# Maximum capacities for each pad
pad_capacity = {'Pink': 3, 'Blue': 4, 'Grey': 2}

# Initialize remaining capacity
pad_remaining = pad_capacity.copy()

# Dictionary to store casualty assignments
assignments = {}

# Iterate through casualties in sorted order (highest priority first)
for i, casualty in enumerate(casualty_list):
    x1, y1 = casualty['x'], casualty['y']

    # Find pads with available capacity
    available_pads = [p for j, p in enumerate(pad_list) if pad_remaining[p['name']] > 0]
    
    if not available_pads:
        assignments[i] = None  # No pad available
        continue
    
    # Pick the nearest pad among available ones
    nearest_pad = min(
        available_pads,
        key=lambda p: math.hypot(p['x'] - casualty['x'], p['y'] - casualty['y'])
    )
    
    # Assign casualty to this pad
    assignments[i] = nearest_pad['name']

    # Decrement pad capacity
    pad_remaining[nearest_pad['name']] -= 1

    # --- ✅ Draw line/arrow from casualty to assigned pad ---
    x2, y2 = nearest_pad['x'], nearest_pad['y']
    #cv.arrowedLine(img_rgb, (x1, y1), (x2, y2), (255,255,255), 2, tipLength=0.05)
    draw_arrow(img_rgb, (x1, y1), (x2, y2), (255,255,255), 3)


for i, casualty in enumerate(casualty_list):
    pad = assignments[i]
    print(f"\nCasualty {i} ({casualty['shape']}, {casualty['emergency']}) -> Pad {pad}")


cv.imshow("Assignments on res.png", img_rgb)
cv.waitKey(0)
cv.destroyAllWindows()

cv.imwrite("C:\\Users\\Prakhar Srivastava\\.vscode\\coding\\UAS\\res_with_arrows.png", img_rgb)


