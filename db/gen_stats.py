import json 
import sys
import os
import random
sys.path.append(os.path.abspath('../code'))
import config
import ast 

def read_json(fn):
    with open(fn, 'r') as fd:
        return json.load(fd)

def stats_enron_db():
    fn = "./enron_db_no_stopwords_size_limit.json"
    #{"11": [k1, k2, k3], "12":[k0], ... }
    db = read_json( fn )
    l = len(db)
    print("len: {}".format( l ))
    for key in db.keys():
        value = db[key]
        assert( len(value) <= config.smax )

def stats_enron_inverted():
    fn = "./enron_inverted_index_ordered.json"
    db = read_json( fn )
    fre_keywords = []
    for f in db:
        if len(f[1]) > 2000:
            fre_keywords.append( f[0] )
    print( fre_keywords )
    print( len(fre_keywords) )

def hash_choice(id, num, max_bucket, bucket):
	random.seed(id)
	if num == 1:
		return random.randint(1, max_bucket)
	b1 = random.randint(1, max_bucket)
	random.seed(id)
	s = random.randint(1, sys.maxint)
	random.seed(s)
	b2 = random.randint(1, max_bucket)
	if bucket[b1] < bucket[b2]:
		return b1
	elif bucket[b2] < bucket[b1]:
		return b2
	else:
		if random.random() <= 0.5:
			return b1
		else:
			return b2

def hash_to_bucket(path, choice, max_freq):
	data = read_json(path)
	ans = [0 for j in range(20)]
	for i in range( len(data)):
		bucket = [0 for j in range(max_freq+ 1)]
		if len(data[i][1]) >= max_freq:
			continue
		for doc_id in data[i][1]:
			b = hash_choice(doc_id, choice, max_freq, bucket)
			bucket[b] += 1
		for j in range(max_freq):
			ans[bucket[j]] += 1
	return ans 

def gen_stop_word_list(path, max_freq):
	stop_word = []
	data = read_json(path)
	ans = [0 for j in range(20)]
	for i in range( len(data)):
		bucket = [0 for j in range(max_freq+ 1)]
		if len(data[i][1]) >= max_freq:
			continue
		for doc_id in data[i][1]:
			b = hash_choice(doc_id, choice, max_freq, bucket)
			bucket[b] += 1
		for j in range(max_freq):
			ans[bucket[j]] += 1

def gen_status_pt_index_bench_rearrange(path):
	db = []
	with open(path, 'r') as fd:
		db = json.load(fd)
	counter = 0
	counter_list = [ 0 for i in range(10)]
	for bucket in [str(i) for i in range(1, 2000)]:
		for file in db[bucket]:
			id, terms = file
			for term in terms.keys():
				if terms[term]:
					keyword, _, c = ast.literal_eval( term )
					counter_list[c] += 1
	return counter_list

if __name__ == '__main__':
	stats_enron_db()
	path = "./enron_inverted_index_ordered.json"
	path_pt_index_bench_rearrange = "./plaintext_index_bench_rearrange.json"
	choice = 2
	max_freq = config.cmax
	print ( hash_to_bucket(path, choice, max_freq) )
	stats_enron_inverted()
	print( gen_status_pt_index_bench_rearrange( path_pt_index_bench_rearrange) )