# Post-clustering analysis
import sys
import table as t

# Vars
sample_file,annot_file,src_file = 'sampleinfo.csv', 'annotation.csv', None
sample_filk,sample_filv,sample_sw,ann_filk,ann_filv,ann_sw = None,None,False,None,None,False
key = None
	
def main():
	for arg in sys.argv[1:]:
		if arg.startswith('sample='):
			sample_file = arg.split('=')[1]
		elif arg.startswith('annot='):
			annot_file = arg.split('=')[1]
		elif arg.startswith('src='):
			src_file = arg.split('=')[1]
		elif arg.startswith('sfilk='):
			sample_filk = arg.split('=')[1]
		elif arg.startswith('sfilv='):
			sample_filv = arg.split('=')[1]
		elif arg.startswith('afilk='):
			ann_filk = arg.split('=')[1]
		elif arg.startswith('afilv='):
			ann_filv = arg.split('=')[1]
		elif arg.startswith('key='):
			key = arg.split('=')[1]
		else:
			print('Unknown argument:', arg)
		
		# derive stats from these tables
		
	runpostprocess(src_file, sample_filk, sample_filv, ann_filk, ann_filv)


def runpostprocess(src_file, sample_filk, sample_filv, ann_filk, ann_filv):
	print('Started loading sample.')
	sample = t.Table(sample_file, filter_key=sample_filk, filter_value=sample_filv, vstartswith=sample_sw)
	print('Finished loading sample.')

	print('Started loading annotations.')
	annotation = t.Table(annot_file, filter_key=ann_filk, filter_value=ann_filv, vstartswith=ann_sw)
	print('Finished loading annotations.')
	
	print('Started loading clusters.')
	clusters = t.Table(src_file + '/clusters.csv')
	print('Finished loading clusters.')

	print('Started loading centers.')
	centers = t.Table(src_file + '/centers.csv')
	print('Finished loading centers.')
	
	with open(src_file + '/stats.csv', 'w') as out:
		print('Center,avg,stdev,min,max', file=out)
		for center in centers:
			#print(center[0])
			cluster = clusters.select([('Cluster',center[0])])
			sumx,sumx2,max,min = 0.,0.,-999999999999999,9999999999999999
			count = 0
			for CpG in cluster:
				#print('CpG', CpG)
				position = float(annotation.get(CpG[0], 'pos'))
				if position < min:
					min = position
				if position > max:
					max = position
				sumx += position
				sumx2 += position**2
				count += 1
			print(count)
			ex,ex2 = sumx / count, sumx2 / count
			stdev = (ex2 - ex**2)**0.5
			print(center[0] + ',' + str(ex)  + ',' + str(stdev) + ',' + str(min) + ',' + str(max), file=out)
		print(file=out)

			
if __name__ == "__main__":
	main()
