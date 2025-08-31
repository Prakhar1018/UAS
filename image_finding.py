import cv2 as cv
import numpy as np
from landOceanSeg import *

def compress(coords, eps=50):
    coords = [tuple(map(float, c)) for c in coords]  #converting to Python floats
    clusters = []  # list of lists

    for point in coords:
        px, py = point
        assigned = False

        for cluster in clusters:
            # compute distance from this point to cluster mean
            cx = sum(x for x, _ in cluster) / len(cluster)
            cy = sum(y for _, y in cluster) / len(cluster)
            dist = ((px - cx)**2 + (py - cy)**2)**0.5

            if dist <= eps:
                cluster.append(point)
                assigned = True
                break

        if not assigned:
            clusters.append([point])

    #mean for each clusters
    cluster_means = [
        (int(sum(x for x, _ in cluster) / len(cluster)),
         int(sum(y for _, y in cluster) / len(cluster)))
         for cluster in clusters]

    return cluster_means

def wmap(path: str, temp_paths: dict[str:list[tuple[int, int]]]) -> dict[str:list[tuple[int, int]]]:
    coordinates = []
    obj = {"circle":[],"star":[],"triangle":[],"square":[]}
    img_rgb = cv.imread(path)
    
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    favs = ["circle","star","triangle","square"]
    for fav in favs:
        template = cv.imread(temp_paths[fav], cv.IMREAD_GRAYSCALE)
        w, h = template.shape[::-1]

        res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)

        if fav=="circle":
            threshold = 0.72
        else:
            threshold = 0.8
        loc = np.where( res >= threshold)
        for pt in zip(*loc[::-1]):
            coordinates.append((int((2*pt[0] + w)//2), int((2*pt[1] + h)//2)))
        coordinates = compress(coordinates)
        for pt in coordinates:
            obj[fav].append(pt)
            #cv.circle(img_rgb, pt, 5, (255, 0, 0), -1)  # blue filled circle
        coordinates=[]
    img_rgb = overlap(img_rgb)
    cv.imwrite(f'res.png',img_rgb)
    return obj
