import io
import csv

csv.field_size_limit(1000000000)

class Table:
	def __init__(self, filename, filter_entry=None, filter_key=None, filter_value=None, vstartswith=False):
		table = csv.reader(open(filename, 'r'))
		self.matrix = {}
		iterator = iter(table)
		self.heads = next(iterator)[1::]
		if filter_entry:
			filter_entry = set(filter_entry)
		while True:
			try:
				row = next(iterator)
				row_name = row[0]
				if not filter_entry or row_name in filter_entry:
					entry = {}
					for i in range(1, len(self.heads) + 1):
						entry[self.heads[i-1]] = row[i]
					#print(filter_key, filter_value)
					if (not filter_key or not filter_value) \
							or (entry[filter_key].startswith(filter_value) if vstartswith else entry[filter_key] == filter_value):
						self.matrix[row_name] = entry
			except StopIteration:
				break
	
	def headers(self):
		return self.heads
	
	def get(self, entry_name, key=None):
		if key:
			return self.matrix[entry_name][key]
		else:
			return self.matrix[entry_name]
	
	def select(self, kvs):
		for entry in self.matrix.keys():
			mistake = False
			for kv in kvs:
				if self.matrix[entry][kv[0]] != kv[1]:
					mistake = True
					break
			if not mistake:
				yield entry,self.matrix[entry]
				
	def selectstart(self, kvs):
		for entry in self.matrix.keys():
			mistake = False
			for kv in kvs:
				if not self.matrix[entry][kv[0]].startswith(kv[1]):
					mistake = True
					break
			if not mistake:
				yield self.matrix[entry]
				
	def entrynames(self):
		return [key for key in self.matrix.keys()]
		
	def __iter__(self):
		for entry in sorted(list(self.matrix.keys())):
			yield (entry, self.matrix[entry])
