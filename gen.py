# Generates the simplified matrix csv file based on given parameters.

import sys
import os
import table as t

# Vars
sample_file,annot_file,data_file,out_file = 'sampleinfo.csv', 'annotation.csv', 'beta.csv', 'test_folder'
sample_filk,sample_filv,sample_sw,ann_filk,ann_filv,ann_sw = None,None,False,None,None,False
key = 'Sample.ID'
defaults = {sample_filk:True,sample_filv:True,sample_sw:True,ann_filk:True,ann_filv:True,ann_sw:True,sample_file:True,annot_file:True,data_file:True,out_file:True,key:True}

for arg in sys.argv[1:]:
	if arg.startswith('sample='):
		sample_file,defaults[sample_file] = arg.split('=')[1], False
	elif arg.startswith('annot='):
		annot_file,defaults[annot_file] = arg.split('=')[1], False
	elif arg.startswith('data='):
		data_file,defaults[data_file] = arg.split('=')[1], False
	elif arg.startswith('out='):
		out_file,defaults[out_file] = arg.split('=')[1], False
	elif arg.startswith('sfilk='):
		sample_filk,defaults[sample_filk] = arg.split('=')[1], False
	elif arg.startswith('sfilv='):
		sample_filv,defaults[sample_filv] = arg.split('=')[1], False
	elif arg.startswith('afilk='):
		ann_filk,defaults[ann_filk] = arg.split('=')[1], False
	elif arg.startswith('afilv='):
		ann_filv,defaults[ann_filv] = arg.split('=')[1], False
	elif arg.startswith('ssw='):
		sample_sw,defaults[sample_sw] = False if arg.split('=')[1] == 'False' else True, False
	elif arg.startswith('asw='):
		ann_sw,defaults[ann_sw] = False if arg.split('=')[1] == 'False' else True, False
	elif arg.startswith('key='):
		key,defaults[key] = arg.split('=')[1], False
	else:
		print('Unknown argument:', arg)

def printformat(string, value, is_default):
	print('%-*s %-*s %s' % (24, string, 20, '\'' + str(value) + '\'', ('(Default)' if is_default else '')))

print('>> Input arguments <<')
printformat('Sample file:', sample_file, defaults[sample_file]) 
printformat('Annot. file:', annot_file, defaults[annot_file])
printformat('Data file:', data_file, defaults[data_file])
printformat('Output folder:', out_file, defaults[out_file])
printformat('Sample filter key:', sample_filk, defaults[sample_filk]) 
printformat('Sample filter value:', sample_filv, defaults[sample_filv])
printformat('Sample use prefix?', sample_sw, defaults[sample_sw])
printformat('Annot. filter key:', ann_filk, defaults[ann_filk])
printformat('Annot. filter value:', ann_filv, defaults[ann_filv])
printformat('Annot. use prefix?', ann_sw, defaults[ann_sw])
printformat('Sort key:', key, defaults[key])
print()
	
print('Started loading sample.')
sample = t.Table(sample_file, filter_key=sample_filk, filter_value=sample_filv, vstartswith=sample_sw)
#print(sample.entrynames())
print('Finished loading sample.')


print('Started loading annotations.')
annotation = t.Table(annot_file, filter_key=ann_filk, filter_value=ann_filv, vstartswith=ann_sw)
print('Finished loading annotations.')



print('Started loading data.')
beta = t.Table(data_file, filter_entry=annotation.entrynames())
print('Finished loading data.')

if not os.path.exists(out_file):
    os.makedirs(out_file)
print('Started writing data to %s.' % out_file)
with open(out_file + '/format.csv', 'w') as mat:
	entrynames = sample.entrynames()
	entrynames.sort(key=lambda samplename: sample.get(samplename, key))
	print(','.join(['', 'pos'] + entrynames), file=mat)
	for (cpgregion, samplenames) in beta:
		#print(annotation.get(cpgregion, 'pos'))
		print(cpgregion + ',' + annotation.get(cpgregion, 'pos') + ',' + ','.join([samplenames[key] for key in entrynames]), file=mat)
print('Finished writing data to file.')



