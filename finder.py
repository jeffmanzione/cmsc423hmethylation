# Imports and such
from __future__ import print_function
import functools
import sys
import re
import table as t
import fuzzykmeans as f
import lloyds
import postcluster

SoftKMeans,Lloyds = 0,1

rangethresh,stdevthresh,k,b,sample_file = 0,0,2,0.8,'sampleinfo.csv'
algo = SoftKMeans
difffile,datafile,src_file = None,'format.csv',None

for arg in sys.argv[1:]:
	#print(arg)
	if arg in ['-l', '-lloyd']:
		algo = Lloyds
	elif arg in ['-f', '-fuzzy', '-soft']:
		algo = SoftKMeans
	elif arg.startswith('sample='):
		sample_file = arg.split('=')[1]
	elif arg.startswith('out='):
		src_file = arg.split('=')[1]
	elif arg.startswith('rt='):
		rangethresh = float(arg.split('=')[1])
	elif arg.startswith('stdt='):
		stdevthresh = float(arg.split('=')[1])
	elif arg.startswith('k='):
		k = int(arg.split('=')[1])
	elif arg.startswith('stiff='):
		b = float(arg.split('=')[1])
	elif arg.startswith('d='):
		difffile = arg.split('=')[1]
	elif arg.startswith('data='):
		datafile = arg.split('=')[1]
	elif arg.startswith('src='):
		src_file = arg.split('=')[1]
	else:
		print('Unknown argument:', arg)


print('Started loading sample.')
sample = t.Table(sample_file)
#print(sample.entrynames())
print('Finished loading sample.')

	
print('Started loading data.')
data = t.Table(src_file + '/' + datafile)
print('Finished loading data.')

print('Preparing data.')
if difffile:
	print('Started generating differences file %s.' % difffile)
vectors = []
count,interesting = 0,0
if difffile:
	diffs = open(difffile, 'w')
for (id, values) in data:
	if difffile:
		sumx,sumx2,max,min = 0.,0.,-999999999999999,9999999999999999
		for value in [float(values[key]) for key in data.headers()]:
			if value < min:
				min = value
			if value > max:
				max = value
			sumx += value
			sumx2 += value**2
		ex,ex2 = sumx / len(values), sumx2 / len(values)
		stdev = (ex2 - ex**2)**0.5
		print(id + ',' + str(ex)  + ',' + str(stdev) + ',' + str(min) + ',' + str(max), file=diffs)
	if (not difffile) or (not rangethresh or max-min > rangethresh) and (not stdevthresh or stdev > stdevthresh):
		interesting += 1
		vector = (id, [float(values[key]) for key in data.headers() if not key == 'pos'])
		#print(vector)
		vectors.append(vector)
	count += 1
if difffile:
	diffs.close()
	print('Finished reading differences.')
print('Finished perparing data.')

	
print('Clustering %d out of %d datapoints using range thresh %f, stdev thresh %f.' % (interesting, count, rangethresh, stdevthresh))
if algo == SoftKMeans:	
	print('Starting soft clustering with k=%d, b=%f.' % (k, b))
	centers,hiddenmatrix = f.softkmeansclustering(vectors, k, b)
else:
	print('Starting Lloyd\'s clustering with k=%d.' % k)
	centers,clusters = lloyds.cluster(vectors, k)
print('Finished clustering.')


print('Started writing to center file %s.' % (src_file + '/centers.csv'))
with open(src_file + '/centers.csv', 'w') as centerf:
	strsamples = re.sub('[\'\[\]]', '', str([header for header in data.headers() if not header == 'pos']))
	strnames = re.sub('[\'\[\]]', '', str([sample.get(header, 'Sample.ID') for header in data.headers() if not header == 'pos']))
	print('Center,' + ('Count,' if algo == Lloyds else '') + strsamples, file=centerf)
	print((',' if algo == Lloyds else '') + 'Type,' + strnames, file=centerf)
	for i in range(0, len(centers)):
		center = centers[i]
		strcenter = str(center)
		print(str(i) + ',' + (str(len(clusters[center])) + ',' if algo == Lloyds else '') + strcenter[1:len(strcenter)-1], file=centerf)
print('Finished writing centers.')


print('Started writing to clusters file %s.' % (src_file + '/clusters.csv'))
with open(src_file + '/clusters.csv', 'w') as clus:
	if algo == SoftKMeans:
		print('CpG,' + ','.join([str(i) for i in range(0, len(centers))]), file=clus)
		for i in range(0, len(ids)):
			print(ids[i] + ',' + ','.join([str(hiddenmatrix[vectors[i]][center]) for center in centers]), file=clus)
	elif algo == Lloyds:
		entries = []
		print('CpG,Cluster,pos', file=clus)
		for i in range(0,len(centers)):
			center = centers[i]
			for vector in clusters[center]:
				entries.append((vector[0], i, data.get(vector[0], 'pos')))
		entries.sort(key=lambda x: x[2])
		for entry in entries:
			print(re.sub('[\'\(\)]', '', str(entry)), file=clus)
print('Finished writing clusters.')




