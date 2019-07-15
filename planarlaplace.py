# Geo-indistigushability for Conservation
# H Imanda, June 2019

# to-do: Insert arXiv link here

# input: (latitude, longitude), epsilon
# output: csv file with 512 noisy (latitude, longitude) results of the planar laplace mechanism

import math
import random
import csv
from mpmath import * #contains the Lambert W function

earth_radius = 6378137

# Convert Cartesian (x,y) to degrees (latitude, longitude)
def cart_to_deg(x, y):
    long_in_rad = x/earth_radius
    lat_in_rad = 2*math.atan(math.exp(y/earth_radius))-(math.pi/2)
    latitude = math.degrees(lat_in_rad)
    longitude = math.degrees(long_in_rad)
    return latitude, longitude

# Convert degrees (latitude, longitude) to Cartesian
def deg_to_cart(latitude, longitude):
    x = earth_radius*math.radians(longitude)
    y = earth_radius*math.log(math.tan(math.pi/4+math.radians(latitude)/2))
    return x, y             

#This is the inverse cumulative polar laplacian distribution function
def chooseRadius(epsilon, z):
    x = (z-1)/math.e
    return -(lambertw(x, k = -1)+1)/epsilon

# http://movable-type.co.uk/scripts/latlong.html
# Returns destination point given distance and bearing from start point
def addVectorToPos(latitude, longitude, distance, angle):
    ang_distance = distance/earth_radius
    #lat1, lon1 = deg_to_cart(latitude, longitude)
    lat1 = math.radians(latitude)
    lon1 = math.radians(longitude)
    lat2 = math.asin(math.sin(lat1)*math.cos(ang_distance)+math.cos(lat1)*math.sin(ang_distance)*math.cos(angle))
    lon2 = lon1 + math.atan2(
        math.sin(angle)*math.sin(ang_distance)*math.cos(lat1),
        math.cos(ang_distance)-math.sin(lat1)*math.sin(lat2))
    lon2 = (lon2 + 3*math.pi)%(2*math.pi) - math.pi #normalise to -180,...,180
    return math.degrees(lat2), math.degrees(lon2), distance, angle


def addNoise(epsilon, latitude, longitude):
    theta = random.random()*math.pi*2
    z = random.random()
    r = chooseRadius(epsilon, z)
    return addVectorToPos(latitude, longitude, r, theta)


def main():
    latitude = float(input("Enter latitude: "))
    longitude = float(input ("Enter longitude: "))
    epsilon = float(input ("Enter epsilon: ")) #Approximately l/r, where r is in metres
    filename = input("Enter filename: ")  #Please include .csv in the filename
    
    header = ['Latitude', 'Longitude', 'Epsilon', 'Distance (m)', 'Angle', 'Shifted Latitude', 'Shifted Longitude']
    latcolumn = []
    loncolumn = []
    epsiloncolumn = []
    noisylatcolumn = []
    noisylongcolumn = []
    distancecolumn = []
    anglecolumn = []

    i = 0
    while i < 512:
        noisylatentry, noisylongentry, distanceentry, angleentry = addNoise(epsilon, latitude, longitude)
        latcolumn.append(latitude)
        loncolumn.append(longitude)
        epsiloncolumn.append(epsilon)
        noisylatcolumn.append(noisylatentry)
        noisylongcolumn.append(noisylongentry)
        distancecolumn.append(distanceentry)
        anglecolumn.append(angleentry)
        i = i + 1

    res = []

    writer = csv.writer(open(filename, 'w'), delimiter=',')
    writer.writerow(i for i in header)
    writer.writerows(zip(latcolumn,loncolumn,epsiloncolumn,distancecolumn, anglecolumn, noisylatcolumn,noisylongcolumn))



if __name__ == '__main__':
    main()
