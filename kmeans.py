#!usr/bin/env python2
# -*- coding: UTF-8 -*-
from math import pow, sqrt
import random
import sys
try:
    import ConfigParser as configparser
except importError:
    import configparser


class Point(object):
    """
    Represent a point.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "("+str(self.x)+", "+str(self.y)+")"

    def __eq__(self, p2):
        return (self.x == p2.x) & (self.y == p2.y)

    def distance(self, p2):
        return sqrt(pow(float(p2.x) - float(self.x), 2) + pow(float(p2.y) - float(self.y), 2))


class Centroid(Point):
    """
    Represent a centroid.
    """

    def __init__(self, x, y):
        Point.__init__(self, x, y)
        self.related_points = []

    def __str__(self):
        return Point.__str__(self)+" \nRelated points : "+str(self.related_points)


def get_parameter_from_config(name, value_type, cat):
    config = configparser.ConfigParser()
    config.read("config.ini")

    if value_type == "str":
        return config.get(cat, name)
    elif value_type == "int":
        return config.getint(cat, name)
    elif value_type == "float":
        return config.getfloat(cat, name)
    elif value_type == "bool":
        return config.getboolean(cat, name)


def load_point():
    points = get_parameter_from_config("points", "str", "TEST_KM")
    parsed_points = points.split(" ")
    return [Point(one.split(',')[0], one.split(',')[1]) for one in parsed_points]  


def centroid_init():
    nb_centroid = get_parameter_from_config("nb_centroid", "int", "TEST_KM")
    x_min = get_parameter_from_config("x_min", "float", "TEST_KM")
    x_max = get_parameter_from_config("x_max", "float", "TEST_KM")
    y_min = get_parameter_from_config("y_min", "float", "TEST_KM")
    y_max = get_parameter_from_config("y_max", "float", "TEST_KM")
    res = []
    for x in range(0, nb_centroid):
        res.append(Centroid(random.uniform(x_min, x_max), random.uniform(y_min, y_max)))
    return res


def assign_points_to_centroid(points, centroids):
    distances = []
    for one_point in points:
        for one_centroid in centroids:
            distances.append(one_point.distance(one_centroid))
        centroids[distances.index(min(distances))].related_points.append(one_point)
        distances = []


def not_the_same(centroids, centroids_tmp):
    res = True
    for x in range(0, len(centroids)):
        res = res & (centroids[x]==centroids_tmp[x])
    return res


def balance_centroids(centroids):
    for one_centroid in centroids:
        sum_x = sum([one_related.x for one_related in one_centroid.related_points])
        sum_y = sum([one_related.y for one_related in one_centroid.related_points])
        one_centroid.x = sum_x / len(one_centroid.related_points)
        one_centroid.y = sum_y / len(one_centroid.related_points)


if __name__=="__main__":  
    points = load_point()
    centroids = centroid_init()
    assign_points_to_centroid(points, centroids)
    centroids_tmp = centroid_init()
    while not_the_same(centroids, centroids_tmp):
        centroids_tmp = centroids
        centroids = balance_centroids(centroids)
        assign_points_to_centroid(points, centroids)
    for one_centroid in centroids :
        print "Centroid "+str(one_centroid)
        for one_point in one_centroid.related_points:
            print one_point
