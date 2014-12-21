# prob37
# Soft K-Means Clustering

import sys
import re
import random
import functools
import math
import operator

def scale (factor, vector):
	return tuple([round(factor * i, 3) for i in vector])
def sumvectors(vectors):
	return tuple(map(sum, zip(*vectors)))
	
# Returns the euclidean distance between any two points of any dimensionality
def euclideandistance(v, w):
	return sum([(v[i] - w[i])**2 for i in range(0, len(w))]) ** (0.5)	

def genhiddenmatrix(points, centers, b):
	hidden = {}
	for point in points:
		hidden[point] = {}
		sum1 = sum([math.exp(-b*euclideandistance(point, center)) for center in centers])
		for center in centers:
			hidden[point][center] = math.exp(-b*euclideandistance(point, center)) / sum1
	return hidden
			
def calculatecenters(hiddenmatrix, centers, points):
	newcenters = []
	for center in centers:
		denom = sumvectors([scale(hiddenmatrix[point][center], point) for point in points])
		numer = sum([hiddenmatrix[point][center] for point in points])
		newcenters.append(scale(1/numer, denom))
	#print(newcenters)
	return newcenters
	
def softkmeansclustering(data, k, b):
	centers = sorted(cmsc423.selectrandomcenters(data, k))
	hiddenmatrix = None
	changed = True
	while changed:
		changed = False
		hiddenmatrix = genhiddenmatrix(data, centers, b)
		newcenters = sorted(calculatecenters(hiddenmatrix, centers, data))
		changed = centers != newcenters
		centers = newcenters
	return (centers, hiddenmatrix)