import unittest
import sys
import os
sys.path.append(os.path.abspath('../code'))
import dp_sse_bench as dp_sse_pkg
import numpy as np 

dp_sse_bench = dp_sse_pkg.dp_sse_bench()

class Test_dp_sse_bench(unittest.TestCase):
    
    def test_init_db(self):
        self.assertNotEqual( dp_sse_bench.db, [] )
    
    def test_init_keyword_univ_and_stop_words(self):
        self.assertNotEqual( dp_sse_bench.keyword_univ, [] )
        self.assertNotEqual( dp_sse_bench.stop_words, [] )

    def test_init_bucket_status(self):
        self.assertNotEqual( dp_sse_bench.bucket_status, {} )
    
    def test_hash_choice(self):
        id = 0
        keyword = dp_sse_bench.keyword_univ[10]
        max_bucket = 2000
        b, counter = dp_sse_bench.hash_choice( id, keyword, max_bucket )
        self.assertLessEqual( b, max_bucket )
        self.assertEqual(counter, 1)

    def test_build_index_plain_bench(self):
        return
        pt_index_bench = dp_sse_bench.build_index_plain_bench()
        cmax = dp_sse_bench.dp_sse_pt.cmax
        smax = dp_sse_bench.dp_sse_pt.smax
        new_db_size = dp_sse_bench.dp_sse_pt.new_db_size
        self.assertEqual( len(pt_index_bench), dp_sse_bench.dp_sse_pt.new_db_size )  
        for item in pt_index_bench:
            self.assertEqual( len( item ), 4 )
            id, h1, h2, mp = item 
            self.assertLessEqual( id,  new_db_size)
            self.assertLessEqual( h1, cmax)
            self.assertLessEqual( h2, cmax)
            self.assertLessEqual( len( mp ),  smax)
        
    def test_rearrange_pt_index_bench(self):
        return 
        cmax = dp_sse_bench.dp_sse_pt.cmax
        
        pt_index_bench = dp_sse_bench.build_index_plain_bench()
        pt_index_bench_rearrange = dp_sse_bench.rearrange_pt_index_bench_and_store(pt_index_bench)
        self.assertEqual( len(pt_index_bench_rearrange), cmax )
    
    def test_search_plain_bench(self):
        idx1 = (1, {str(("test", 1, 1)): True, str(("test", 1, 0)): False})
        token_tp = ("test", 1, 1, None, False)
        token_fp = (None, None, None, 1, False)
        token_nm = (None, None, None, None, True)
        token_ = ("test", 1, 0, None, False)
        self.assertEqual( dp_sse_bench.search_plain_bench(idx1, token_tp), (True, 1, True, False) )
        self.assertEqual( dp_sse_bench.search_plain_bench(idx1, token_fp), (True, 1, False, True ) )
        self.assertEqual( dp_sse_bench.search_plain_bench(idx1, token_nm), (False, None, False, False) )
        self.assertEqual( dp_sse_bench.search_plain_bench(idx1, token_), (False, None, False, False) )
    
    def test_gen_tokens_tp_bench(self):
        cmax = dp_sse_bench.dp_sse_pt.cmax
        keyword = 'test'
        tp = 0.0005
        tp_tokens = dp_sse_bench.gen_tokens_tp_bench(keyword, tp)
        for tk in tp_tokens:
            self.assertEqual( len( tk ), 5 )
            self.assertEqual( [tk[3], tk[4] ], [None, False] )
            self.assertEqual( tk[0], keyword )
            self.assertLessEqual( tk[1],  cmax)
            self.assertGreater( tk[1],  0)
            self.assertLessEqual(tk[2], 3)
        self.assertLessEqual(len(tp_tokens), tp * dp_sse_bench.dp_sse_pt.new_db_size * 3)
        
    def tst_gen_tokens_fp_bench(self):
        fp = 0.0005
        fp_tokens = dp_sse_bench.gen_tokens_fp_bench(fp)
        for tk in fp_tokens:
            self.assertEqual( len(tk), 5)
            self.assertEqual( [tk[0], tk[2] ], [None, None] )
            self.assertLessEqual( tk[3], dp_sse_bench.dp_sse_pt.new_db_size)
            self.assertLessEqual( tk[1], dp_sse_bench.dp_sse_pt.cmax)
            self.assertGreater( tk[1],  0)            
            self.assertEqual(tk[4], False)
        self.assertLessEqual(len(fp_tokens), fp * dp_sse_bench.dp_sse_pt.new_db_size * 3)
        
    def test_gen_tokens_non_match_bench(self): 
        fp = 0.0005
        nm_tokens = dp_sse_bench.gen_tokens_non_match_bench(fp)
        for tk in nm_tokens:
            self.assertEqual( len(tk), 5 )
            self.assertEqual( (tk[0], tk[2], tk[3], tk[4]), (None, None, None, True) )
            self.assertLessEqual( tk[1], dp_sse_bench.dp_sse_pt.cmax)
            self.assertGreater( tk[1],  0) 
        self.assertLessEqual(len(nm_tokens), fp * dp_sse_bench.dp_sse_pt.new_db_size * 3)

    def test_gen_tokens_bench(self):
        keyword = "test"
        tp, fp = 0.0005, 0.0005
        all_tokens = dp_sse_bench.gen_tokens_bench(keyword, tp, fp)
        self.assertLessEqual( len(all_tokens), 3 * (3 * fp + tp) * dp_sse_bench.dp_sse_pt.new_db_size )
        self.assertGreater( len(all_tokens),  0) 
        for tk in all_tokens:
            self.assertEqual( len(tk), 5) 
    
    def test_rearrange_all_tokens_bench(self):
        keyword = "test"
        tp, fp = 0.0005, 0.0005
        all_tokens = dp_sse_bench.gen_tokens_bench(keyword, tp, fp)
        rearranged_tokens = dp_sse_bench.rearrange_all_tokens_bench( all_tokens )
        count = 0
        for bucket in [ i +1 for i in range(dp_sse_bench.dp_sse_pt.cmax)]:
            count += len( rearranged_tokens[bucket] )
        self.assertEqual( len(all_tokens), count )

    def test_serialize_rearrange(self):
        keyword = "test"
        tp, fp = 0.0005, 0.0005
        all_tokens = dp_sse_bench.gen_tokens_bench(keyword, tp, fp)
        rearranged_tokens = dp_sse_bench.rearrange_all_tokens_bench( all_tokens )
        serialized_tokens, serialized_tokens_map = dp_sse_bench.serialze_rearrange_bench( rearranged_tokens )
        self.assertEqual( len(serialized_tokens), len(serialized_tokens_map) )
        self.assertEqual( len(serialized_tokens[0]), 5 )
    
    def test_single_core_subtask(self):
        cmax = dp_sse_bench.dp_sse_pt.cmax
        pt_index_bench = dp_sse_bench.build_index_plain_bench()[0:100]
        pt_index_bench_rearrange = dp_sse_bench.rearrange_pt_index_bench(pt_index_bench)
        keyword = "test"
        tp, fp = 0.0005, 0.0005
        all_tokens = dp_sse_bench.gen_tokens_bench(keyword, tp, fp)
        rearranged_tokens = dp_sse_bench.rearrange_all_tokens_bench( all_tokens )
        serialized_index, serialized_map_index = dp_sse_bench.serialze_rearrange_bench( pt_index_bench_rearrange )
        serialized_tokens, serialized_map_tokens = dp_sse_bench.serialze_rearrange_bench( rearranged_tokens )
        dp_sse_bench.benchmarking_kernel( pt_index_bench_rearrange, rearranged_tokens, serialized_index, serialized_tokens, serialized_map_index, serialized_map_tokens, 2 )


        

    
    

        

if __name__ == "__main__":
    unittest.main()
            

