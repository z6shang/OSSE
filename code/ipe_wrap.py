import sys, os
import json


# Path hack
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(1, os.path.abspath('../fhipe'))
sys.path.insert(2, os.path.abspath('charm'))
sys.path.insert(3, os.path.abspath('../fhipe/charm/charm'))


from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from fhipe import ipe 
import time

class ipe_wrap:
    def __init__(self, v_len):
        self.pp = None
        self.sk = None
        self.group = None
        self.sk_dump_path = '../db/ipe_sk_dump.json'
        self.large_p = None
        self.vec_len = v_len
    
    def init_para(self):
        # if the parameter already generated and stored
        # then return .
        if os.path.isfile(self.sk_dump_path): return 

        # the vector to be encrypted has length 303
        (self.pp, self.sk) = ipe.setup(self.vec_len, simulated = False)
        (detB, B, Bstar, group, g1, g2) = self.sk 
        self.group = group 

        def deparse_B(M):
            new_M = []
            for i in range(len(M)):
                new_M.append([])
                for j in range(len(M[i])):
                    new_M[i].append( self.group_serial( M[i][j]) )
            return new_M

        sk_dump = { 'detB':detB, 'B': deparse_B(B), 'Bstar': deparse_B(Bstar),\
            'group':'MNT159', 'g1': self.group_serial(g1), 'g2': self.group_serial(g2)	}
        
        with open(self.sk_dump_path, 'w') as fd:
            json.dump( sk_dump, fd )
    
    def group_serial(self, a):
	    return self.group.serialize(a).decode('ascii')
    
    def group_deserial(self, a):
	    return self.group.deserialize( a.encode('ascii') )
    
    def load_para(self):
        sk_dump = None
        with open(self.sk_dump_path, 'r') as fd:
            sk_dump = json.load(fd)
        detB = sk_dump['detB']
        self.group = PairingGroup(sk_dump['group'])
        def parse_B(M):
            new_M = []
            for i in range(len(M)):
                new_M.append([])
                for j in range(len(M[i])):
                    new_M[i].append( self.group_deserial(M[i][j] ) )
            return new_M
        B, Bstar = parse_B(sk_dump['B']), parse_B(sk_dump['Bstar'])
        g1, g2 = self.group_deserial(sk_dump['g1']), self.group_deserial(sk_dump['g2'])
        sk = (detB, B, Bstar, self.group, g1, g2)
        pp = ()
        return pp, sk 
        
    
    def para_setup(self):
        self.pp, self.sk = self.load_para()
        self.large_p = (self.sk)[3].order()
        self.group = self.sk[3]
    
    def encrypt_polycoeffs(self, coeffs):
	    return ipe.encrypt(self.sk, coeffs)
	
    def encrypt_token(self, coeffs):
	    return ipe.keygen(self.sk, coeffs)
    
    def search_enc(self, idx, token):
	    prod = ipe.decrypt(self.pp, token, idx, 1)
	    return True if prod == 0 else False

if __name__ == '__main__':
    ipe_ins = ipe_wrap(10)
    ipe_ins.init_para()
    ipe_ins.para_setup( )
    poly = [2 for i in range(ipe_ins.vec_len)]
    token = poly[:]
    token[-1] = -2 * (ipe_ins.vec_len - 1) 
    enc_poly = ipe_ins.encrypt_polycoeffs( poly )
    enc_token = ipe_ins.encrypt_token( token )
    assert( ipe_ins.search_enc(
        enc_poly, enc_token
    ) )


    

    

    

    


