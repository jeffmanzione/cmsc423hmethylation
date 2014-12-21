import random
import functools
import math

# Returns the euclidean distance between any two points of any dimensionality
def euclideandistance(v, w):
	return sum([(v[i] - w[i])**2 for i in range(0, len(w))]) ** (0.5)

# Determines the closest center in centers to p.
def closestcenter(p, centers):
	#print(centers)
	return min(centers, key=lambda y: euclideandistance(p[1], y))

# Selects k random centers from points X.
def selectrandomcenters(x, k):
	centers = []
	while len(centers) < k:
		rand = x[random.randrange(0, len(x))]
		if rand not in centers:
			centers.append(tuple(rand[1]))
	return centers


def cluster(x, k):
	centers = selectrandomcenters(x, k)
	clusters,changed = None,True
	while changed:
		changed = False
		clusters = {}
		for center in centers:
			clusters[center] = []
		for point in x:
			closest = closestcenter(point, centers)
			clusters[closest].append(point)
		newcenters = []
		for center in centers:
			#print([point for point in clusters[tuple(center)] if not point[1]])
			newcenter = clusters[center][0][1]
			for point in clusters[center][1:]:
				newcenter = [x + y for x, y in zip(newcenter, point[1])]
			#print(newcenter)
			#newcenter = functools.reduce(lambda x,y: [i + j for i,j in zip(x[1],y[1])], \
			#		clusters[tuple(center)])
			newcenter = tuple([y / len(clusters[center]) for y in newcenter])
			newcenters.append(newcenter)
			if newcenter not in centers:
				changed = True
		centers = newcenters
	return centers, clusters
	