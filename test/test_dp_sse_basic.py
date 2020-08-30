import unittest
import sys
import os
sys.path.append(os.path.abspath('../code'))
import dp_sse as dp_sse_pkg
import numpy as np 

dp_sse = dp_sse_pkg.dp_sse_plaintext()

class Test_dp_sse_basic(unittest.TestCase):

    def test_hash(self):
        s = "test"
        h = dp_sse.hash(s)
        self.assertEqual( type(h), type(int(2**160)) )
        self.assertLess( h, 2**160 )
    
    def test_hash_1(self):
        id = [1, 2, 10]
        ans = [dp_sse.hash_1(_id) for _id in id ]
        for i in range(len( ans )):
            self.assertEqual( len(ans[i]), dp_sse.p2_len )
            self.assertLessEqual( int(ans[i]), dp_sse.cmax )
            self.assertGreaterEqual( int(ans[i]), 1 )
    
    def test_hash_2(self):
        id = [1, 2, 10]
        ans = [dp_sse.hash_2(_id) for _id in id ]
        for i in range(len( ans )):
            self.assertEqual( len(ans[i]), dp_sse.p2_len )
            self.assertLessEqual( int(ans[i]), dp_sse.cmax )
            self.assertGreaterEqual( int(ans[i]), 1 )
    
    def test_p_keyword(self):
        ss = ["1"*100, "" ]
        for i in range(len(ss)):
            s = ss[i]
            ans = dp_sse.p_keyword( s )
            self.assertEqual( len(ans),  dp_sse.p1_len)
            self.assertLess( int( ans ), 10** dp_sse.p1_len )
    
    def test_p_counter(self):
        k = dp_sse.p_keyword("test")
        h1, h2 = dp_sse.hash_1(k), dp_sse.hash_2(k)
        self.assertEqual( len(dp_sse.p_counter( k, h1, h2 )[0]), dp_sse.p3_len )
        self.assertEqual( len(dp_sse.p_counter( k, h1, h2 )[1]), dp_sse.p2_len )
    
    def test_gen_term_basic_2_hash_keyword(self):
        keyword = "test"
        ids = ["10", 10]
        for id in ids:
            ans = dp_sse.gen_term_basic_2_hash_keyword(keyword, id)
            self.assertLess( ans, dp_sse.large_p )
    
    def test_gen_term_basic_2_hash_padding(self):
        ans = dp_sse.gen_term_basic_2_hash_padding()
        self.assertLess( ans,  dp_sse.large_p)
    
    def test_gen_term_basic_2_hash_id(self):
        id = 10
        ans = dp_sse.gen_term_basic_2_hash_id( id )
        self.assertEqual( len(ans), 2)
        for a in ans:
            self.assertLess(a, dp_sse.large_p)

    
    def test_poly_extend(self):
        term = dp_sse.gen_term_basic_2_hash_padding()
        ans = dp_sse.poly_extend( term )
        self.assertEqual( len(ans), dp_sse.smax + 3 )
        for i in ans:
            self.assertLess( i, dp_sse.large_p )
    
    def test_gen_token_basic_keyword(self):
        keyword = "test"
        buckets = ["10", 10]
        counters = ["2", 2]
        for bucket in buckets:
            for counter in counters:
                ans = dp_sse.gen_token_basic_keyword( keyword, bucket, counter )
                self.assertEqual( len(ans), dp_sse.smax + 3 )
    
    def test_gen_token_basic_padding(self):
        ans = dp_sse.gen_token_basic_padding()
        self.assertEqual( len(ans), dp_sse.smax + 3 )
    
    def test_gen_token_basic_id_hash_1(self):
        ids = ["10", 10]
        for id in ids:
            ans = dp_sse.gen_token_basic_id_hash_1(id)
            self.assertEqual( len(ans), dp_sse.smax + 3)
    
    def test_gen_token_basic_id_hash_2(self):
        ids = ["10", 10]
        for id in ids:
            ans = dp_sse.gen_token_basic_id_hash_2(id)
            self.assertEqual( len(ans), dp_sse.smax + 3)

    def test_gen_polynomial_roots(self):
        keywords = ["0"*i for i in range( dp_sse.smax - 10 )]
        ids = ["1",1]
        for id in ids:
            ans = dp_sse.gen_polynomial_roots( keywords, id )
            self.assertEqual( len(ans), dp_sse.smax + 2 )
    
    def test_gen_polynomial_from_roots(self):
        roots = [i for i in range( dp_sse.smax + 2 )] 
        roots = np.array(roots, dtype = object)
        coeffs = dp_sse.gen_polynomial_from_roots(roots)
        self.assertEqual( len(coeffs), dp_sse.smax + 3 )
        self.assertEqual( coeffs[-1], 0 )
    
    def test_gen_polynomial_plain(self):
        keywords = ["1"*i for i in range( dp_sse.smax - 10 ) ]
        ids = [10, '10']
        for id in ids:
            coeffs = dp_sse.gen_polynomial_plain( keywords, id )
            self.assertEqual( len(coeffs), dp_sse.smax + 3 )
            for c in coeffs:
                self.assertLess( c, dp_sse.large_p )

    def test_gen_tokens_fp_hash_1(self):
        fp = 0.001
        fptks = dp_sse.gen_tokens_fp_hash_1( fp )
        while len(fptks) < 0:
            fptks = dp_sse.gen_tokens_fp_hash_1( fp )      
        self.assertLess( len(fptks), 3 * fp * dp_sse.new_db_size )
        self.assertEqual( len(fptks[0]), 2 )
        self.assertEqual( len( fptks[0][0] ), dp_sse.smax + 3 )
        self.assertLess( fptks[0][1] , dp_sse.cmax )
    
    def test_gen_tokens_fp_hash_2(self):
        fp = 0.001
        fptks = dp_sse.gen_tokens_fp_hash_2( fp )
        while len(fptks) < 0:
            fptks = dp_sse.gen_tokens_fp_hash_2( fp )      
        self.assertLess( len(fptks), 3 * fp * dp_sse.new_db_size )
        self.assertEqual( len(fptks[0]), 2 )
        self.assertEqual( len( fptks[0][0] ), dp_sse.smax + 3 )
        self.assertLess( fptks[0][1] , dp_sse.cmax )
    
    def test_gen_tokens_tp(self):
        keyword = "test"
        tp = 0.1
        tptks = dp_sse.gen_tokens_tp( keyword, tp )
        self.assertEqual( len(tptks[0]), 2 )
        self.assertEqual( len( tptks[0][0] ), dp_sse.smax + 3 )
        self.assertLessEqual( tptks[0][1] ,  dp_sse.cmax)
    
    def test_gen_tokens_non_match(self):
        fp = 0.001
        fp = 0.001
        nmtks = dp_sse.gen_tokens_non_match( fp )
        while len(nmtks) < 0:
            nmtks = dp_sse.gen_tokens_non_match( fp )      
        self.assertLess( len(nmtks), 3 * fp * dp_sse.new_db_size )
        self.assertEqual( len(nmtks[0]), 2 )
        self.assertEqual( len( nmtks[0][0] ), dp_sse.smax + 3 )
        self.assertLess( nmtks[0][1] , dp_sse.cmax )
    
    def test_gen_tokens_plain(self):
        keyword = "test"
        tp = 0.01
        fp = 0.001
        tks = dp_sse.gen_tokens_plain( keyword, tp, fp )
        self.assertEqual( len(tks[0]), 2 )
        self.assertEqual( len( tks[0][0] ), dp_sse.smax + 3 )
        self.assertLess( tks[0][1] , dp_sse.cmax )


    
    def test_search_plain(self):
        keywords = ["1"*i for i in range( dp_sse.smax - 10 ) ]
        id = 0 

        index = dp_sse.gen_polynomial( keywords, id )

        k_true, k_false = "1", "2"
        h1, h2 = dp_sse.hash_1(id), dp_sse.hash_2( id )
        
        t1 = dp_sse.gen_token_basic_id_hash_1( id )
        t2 = dp_sse.gen_token_basic_id_hash_2( id )
        t3 = dp_sse.gen_token_basic_keyword( k_true, h1, 1 )
        t4 = dp_sse.gen_token_basic_keyword( k_true, h2, 1 )
        t5 = dp_sse.gen_token_basic_keyword( k_false, h2, 1 )
        t6 = dp_sse.gen_token_basic_keyword( k_false, h1, 1 )

        self.assertEqual( dp_sse.search_plain( index, t1 ), True )
        self.assertEqual( dp_sse.search_plain( index, t2 ), True )
        self.assertEqual( dp_sse.search_plain( index, t5 ), False )
        self.assertEqual( dp_sse.search_plain( index, t6 ), False )
        self.assertSetEqual ( set([dp_sse.search_plain( index, t3 ), 
            dp_sse.search_plain( index, t4 )]), set([True, False]) )
        



if __name__ == "__main__":
    unittest.main()