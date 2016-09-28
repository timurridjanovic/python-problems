from scipy import ndimage
import matplotlib.pyplot as plt
from random import sample
from random import random
from math import sqrt
from twisted.internet import task
from twisted.internet import reactor
import time
import os

def import_image(path):
    return ndimage.imread(path)

def get_points(img):
    points = []
    for y, col in enumerate(img):
        for x, row in enumerate(col):
            points.append((x, y, row))
    return points

def euclidian_distance(center, point):
    return sqrt(sum([(float(center[i]) - float(point[i])) ** 2 for i in range(len(point))]))


def get_shorter_distance(point, centers):
    return min([{
        "point": point, 
        "center": i, 
        "dist": euclidian_distance(center, point[2])
    } for i, center in enumerate(centers)], key = lambda x: x["dist"])


def calculate_centers(clusters):
    centers = []
    for cluster in clusters:
        new_center = [0, 0, 0]
        for point in cluster:
            new_center[0] += point['point'][2][0]
            new_center[1] += point['point'][2][1]
            new_center[2] += point['point'][2][2]
        num_points = 1 if len(cluster) == 0 else len(cluster)
        new_center = [int(e)/num_points for e in new_center]
        centers.append(new_center)
    return centers

def no_diff(centers, new_centers, min_diff):
    diffs = [euclidian_distance(centers[i], new_centers[i]) for i in range(len(centers))]
    if sum(diffs) <= len(centers) * min_diff:
        return True
    return False

def kmeans(img, k, min_diff):
    points = get_points(img)
    centers = [e[2] for e in sample(points, k)]
   
    while True:
        clusters = [[] for center in centers]
        
        for point in points:
            dist = get_shorter_distance(point, centers)
            clusters[dist['center']].append(dist)

        new_centers = calculate_centers(clusters)
        if no_diff(centers, new_centers, min_diff):
            break
        else:
            centers = new_centers
    return centers, clusters

def get_target_cluster(centers, clusters):
    """
    getting the cluster wich has a center with an RGB color that is the darkest amongst other 
    colors that have a certain saturation
    """
    def get_saturation(c):
        m = 1 if max(c) == 0 else max(c)
        return max(c) - min(c) / m

    def get_luminance(c):
        return int(0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2])
   
    target = [{ 
        'saturation': get_saturation(center), 
        'luminance': get_luminance(center), 
        'index': i 
    } for i, center in enumerate(centers)]

    filtered_target = filter(lambda x: True if x['saturation'] >= 120 else False, target)

    if len(filtered_target) == 0:
        index = max(target, key=lambda x: x['saturation'])['index']
        return clusters[index]
    
    index = min(filtered_target, key=lambda x: x['luminance'])['index']
    return clusters[index]


def get_target(cluster):
    target = cluster.pop(int(random() * len(cluster)))
    return target


def start_reactor(cluster, img):
    def update_current(current, target, speed):
        def update_coord(value, coord):
            result = 0
            if value < coord:
                result = value + speed
                if result >= coord:
                    result = coord
                return result
            result = value - speed
            if result <= coord:
                result = coord
            return result

        return [update_coord(current[0], target[0]), update_coord(current[1], target[1])]

    def move_mouse():
        if move_mouse.times >= move_mouse.max_times:
            reactor.stop()
            plt.show()
            return
        
        color = 'r'

        if move_mouse.current == move_mouse.target:
            target = get_target(cluster)['point']
            move_mouse.target = [target[0], target[1]]
            color = 'g'

        x = move_mouse.current[0]
        y = move_mouse.current[1]
        print (x, y, time.time())
        plt.scatter([x], [y], c=color, s=40)
        move_mouse.current = update_current(move_mouse.current, move_mouse.target, move_mouse.speed)
        move_mouse.times += 1
        
    move_mouse.timeout = 0.1
    move_mouse.max_times = 150
    move_mouse.times = 0
    move_mouse.speed = 6
    
    target = get_target(cluster)['point']
    move_mouse.target = [target[0], target[1]]
    move_mouse.current = move_mouse.target

    l = task.LoopingCall(move_mouse)
    l.start(move_mouse.timeout)
    plt.imshow(img)
    reactor.run()

def get_path_of_file(file_path):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    if current_dir.split('/')[-1] != 'src':
        #this is to handle bugs related to certain environments or editors
        current_dir = os.path.join(current_dir, 'src')
    return os.path.abspath(os.path.join(current_dir, file_path))


def main():
    imgpath = get_path_of_file('../images/moat_ad.png')
    img = import_image(imgpath)
    print "Processing image..."
    print "Finding the 3 most dominant colors in the image using the kmeans clustering algorithm (this may take 30 seconds or more depending on the size of the image)..."
    centers, clusters = kmeans(img, 3, 1)
    print "Getting the cluster with the most prominent color (in this case the darkest color with a certain amount of saturation)..."
    cluster = get_target_cluster(centers, clusters)
    print "Starting simulation..."
    start_reactor(cluster, img)
    



if __name__ == '__main__':
    main()
