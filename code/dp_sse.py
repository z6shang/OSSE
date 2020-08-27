import sys, os
import random 
from collections import defaultdict
import numpy as np 
from multiprocessing import Pool
import json
import time
import hashlib
import config 

class dp_sse: 
    # Init parameters
    def __init__(self):
        # init parameters from config.py
        self.db_size = config.db_size
        self.new_db_size = config.new_db_size # when size_lmt = 300
        self.cmax = config.cmax
        self.smax = config.smax
        self.placeholder_in_index = config.placeholder_in_index
        self.large_p = config.large_p
        self.stopwords_size = config.large_p
        self.countermax = config.countermax
        self.db_path = config.db_path
        self.core_num = config.core_num
        self.max_len = config.max_len
        self.p1_len = config.p1_len 
        self.p2_len = config.p2_len 
        self.p3_len = config.p3_len 

        #init other parameters
        self.counter_map = defaultdict(int)
        # A map string => integer
        # map keyword + hash(keyword) to the current number of such string 
        self.counter_map_2_hash = defaultdict(int)
        self.sk = ""

    # hash a keyword string into an integer (160bits), no modular
    # Input: 
    #   a: string 
    # Output:
    #   160-bit integer 
    ##
    def hash(self, a):
        return int(hashlib.sha1(str(a).encode('utf8')).hexdigest(), 16)
    
    # hash an integer into one of the self.cmax buckets
    # Input: 
    #   id: integer/string 
    # Output:
    #   string of fixed length self.p2_len 
    ##
    def hash_1(self, id):
        random.seed( int(id) )
        pos =  random.randint(1, self.cmax)
        return str(pos).zfill( self.p2_len )
    
    # hash an integer into the better choice of the 2 buckets 
    # where the 2 candidate buckets are chosen uniformly at random 
    # "better" means that less have chosen such bucket.

    # Another function that hash an integer into one of the self.cmax buckets
    # Input: 
    #   id: integer/string 
    # Output:
    #   string of fixed length self.p2_len 
    ##
    def hash_2(self, id):
        return hash_1(id) #make everything run in one-hash setting
        #comment the above line to run in 2 hash setting.
        random.seed( int( id ) )
        random.seed( random.randint( 1, self.cmax ) )
        pos = random.randint(1, self.cmax)
        return str(pos).zfill( self.p2_len )
    
    # Convert keyword string into integer of fixed length p1_len 
    # Input: 
    #   ss: string of arbitrary length 
    # Output:
    #   string of fixed length, p1_len 
    ## 
    def p_keyword(self, ss):
        _ss = str( ss )[ 0 : self.max_len ]
        res = str( hash( _ss ) % ( 10**self.p1_len ) ).zfill( self.p1_len )
        return res
    
    # Given a keyword and global maps, choose the better bucket position and 
    # the corresponding counter in that bucket position 
    # Input:
    #   k : keyword, string 
    #   h1: string, produced by self.hash_1 
    #   h2: string, produced by self.hash_2 
    # Output:
    #   counter, string of fixed length self.p3_len 
    #   bucket number, string of fixed length self.p2_len 
    ##
    def p_counter(self, k, h1, h2):
        res = (0, 0)
		if self.counter_map_2_hash[k+h1] < self.counter_map_2_hash[k+h2]:
			res = (k + h1, h1)
		elif counter_map_2_hash[k+h1] > counter_map_2_hash[k+h2]:
			res = (k + h2, h2)
		else:
			res = (k + h1, h1) if random.random() < 0.5 else (k + h2, h2)
		counter_map_2_hash[res[0]] += 1 #counter start from 1
		return str(counter_map_2_hash[res[0]]).zfill(p3_len), res[1]

    # Gen the term encoding a keyword 
    # Input:
    #   keyword: string
    #   id: integer/string 
    # Output:
    #   integer mod self.large_p 
    ## 
    def gen_term_basic_2_hash_keyword(self, keyword, id):
        h1 = self.hash_1(id)
		h2 = self.hash_2(id)
		p1 = self.p_keyword(keyword)
		p3, p2 = p_counter(p1, h1, h2)
		term = p1 + p2 + p3
		return hash(term) % self.large_p 
    # Gen the term that used to pad a small file into size self.smax 
    # Input: 
    #   N/A 
    # Output:
    #   integer mod self.large_p
    # Note: As long as the encoded message is different from meaningful terms.
    ##
    def gen_term_basic_2_hash_padding(self):
        p1 = '1'.zfill( self.p1_len )
		p2 = '0'.zfill( self.p2_len )
		p3 = '0'.zfill( self.p3_len )
        term = p1 + p2 + p3
        return hash(term) % self.large_p 
    
    # Gen the term that used generate false positives
    # Input: 
    #   id: integer/string  
    # Output:
    #   integer mod self.large_p
    # Note: As long as the encoded message is different from other terms 
    # that encode real keywords/dummy terms for padding.
    ##
    def gen_term_basic_2_hash_id(self, id):
        p1 = str(id).zfill( self.p1_len )
		p2 = '1'.zfill( self.p2_len )
		p3 = '100'.zfill( self.p3_len )
		term = p1 + p2 + p3
		return hash(term) % self.large_p 
    
    # Given a root, extend it into its series of power self.smax + 2 to 0
    # Input:
    #   term: integer/string 
    # Output:
    #   A list of integers, self.smax + 3 in total 
    ##
    def poly_extend(self, term):
        term = hash(str(term)) %self.large_p
        poly = [
                    term**(self.smax+2 - i) % self.large_p 
                    for i in range(self.smax + 2)
                ]
	    poly.append(1)
        return poly
    
    # Gen the search token for one keyword in one specific position(bucket and counter)
    # Input: 
    #   keyword: string 
    #   bucket:  int/string 
    #   counter: int/string 
    # Output:
    #    a list of self.smax + 3 integer mod self.large_p 
    ##
    def gen_token_basic_keyword(self, keyword, bucket, counter):
        p1 = self.p_keyword( keyword )
		p2 = str(bucket).zfill( self.p2_len )
		p3 = str(counter).zfill( self.p3_len )
        term = p1 + p2 + p3 
	    return self.poly_extend( term )
    
    # Gen dummy token that matches none 
    # Input: 
    #   N/A
    # Output:
    #   a list of self.smax + 3 integers mod self.large_p 
    ##
    def gen_token_basic_padding(self):
        p1 = '0'.zfill( self.p1_len )
		p2 = '2'.zfill( self.p2_len )
		p3 = '100'.zfill( self.p3_len )
		term = p1 + p2 + p3
	    return self.poly_extend( term )        
    
    # Gen false positive token
    # Input: 
    #   id: integer/string
    # Output:
    #   a list of self.smax + 1 integers mod self.large_p 
    ##
    def gen_token_basic_id(self, id):
        p1 = str(id).zfill( self.p1_len )
		p2 = str(  ).zfill( self.p2_len )
		p3 = '100'.zfill( self.p3_len )
		term = p1 + p2 + p3
	    return self.poly_extend( term )        
        
   
    # Given a list of keywords in a file, generate the corresponding polynomial roots
    # Input:
    #   keywords: a list of keywords (string)
    #   id: the id of the file (string/integer)
    # Output:
    #   np.array, all roots of the polynomial
    #   self.smax + 1 in total 
    ##
    def gen_polynomial_roots(self, keywords, id):
        term_list = []
        for keyword in keywords:
            term_list.append( self.gen_term_basic_2_hash_keyword(  keyword, id ) )
        for i in range( self.smax -  len(keywords) ):
            term_list.append( self.gen_term_basic_2_hash_padding( ) )
        term_list.append( self.gen_term_basic_2_hash_id(id) )
        term_list = np.array( term_list, dtype=object )
        return term_list

    # Given all root, gen the polynomial represented by its coefficients
    # # Input:
    #   roots: np.array(, dtype = object)
    # Output:
    #   np.array, all coefficients of the polynomial 
    ##
    def gen_polynomial(self, roots):
        poly = np.poly1d(roots, True) # coefficients from high degree to low
	    coeffs = poly.coeffs % large_p
        coeffs = coeffs.tolist()
        return coeffs
    
    # Given a list of keywords in a file, generate the corresponding index of the file
    # Input:
    #   keywords: a list of keywords (string)
    #   id: the id of the file (string/integer)
    # Output:
    #   list of integer mod self.large_p, all coefficients of the polynomial
    #   self.smax +1 in total 
    ##
    def gen_index_per_file(self, keywords, id):
        roots = self.gen_polynomial_roots(keywords, id)
        return self.gen_polynomial( roots )
    

    # Given an index idx and a query token, return match (True) or not (False)
    # Input:
    #   idx: np.array(dtype = object), the polynomial coefficients
    #   token: np.array(dtype = object)
    # Output:
    #   if the token encode a keywords/the index in the file of idx, then return True
    #   otherwise, return False 
    ##
    def search_plain(idx, token):
        if(len(idx) != len(token)) return False 
        return sum(
            [int(idx[i]) * int(token[i]) for i in range(len(idx))]
            ) % large_p == 0

    #should only take in roots and do coeffs
    # otherwise cannot be in parallel
    def wrap_gen_index_plain_parallel(x):
        res = []
        for i in range(len( x )):
            roots, id = x[i]
            p = np.poly1d(roots, True) # coefficients from high degree to low
            coeffs = p.coeffs % large_p
            coeffs = coeffs.tolist()
            res.append( coeffs )
        return res 