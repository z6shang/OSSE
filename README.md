# An Implementation of DPSSE

This is repository contains the prototype implementation of OSSE. The files in this repository refer to the scheme as DP-SSE (Differentially Private SSE) since this was its original name.

This implementation is a research poc built for micro benchmarking purpose, and is not intended to be used in production-level code as it has not been carefully verified for potential performance issues or security flaws.

Authors: Zhiwei Shang, Simon Oya, Andreas Peter, Florian Kerschbaum.

Contact Zhiwei for questions about the code: z6shang@uwaterloo.ca.

## Prerequisites

Make sure you have the following installed.

 * [Python 3.x.x](https://www.python.org/downloads/release/python-350/)
 * [GMP 5.x](http://gmplib.org/)
 * [PBC](http://crypto.stanford.edu/pbc/download.html) 
 * [OpenSSL](http://www.openssl.org/source/)

 ## Installation 

```bash
    git clone --recursive https://github.com/z6shang/dp_sse.git
    cd fhipe/charm
    git checkout master && git pull
    cd ..
    # It should be noted that you might need to modify the original Makefile in the following way if you are using conda environments
    # Modify 
    # $(CHARM): FORCE
    #    cd charm && ./configure.sh  --install=. && make
    # Into
    # $(CHARM): FORCE
    #	 cd charm && ./configure.sh  --python=your/path/to/python --install=. && make
    sudo make install
```

## Running the benchmarking

Make sure that you are in the dir `dp_sse/code`.

```bash
	python3 dp_sse_bench.py
```

## Modules

This library ships with the following modules:

 * **DPSSE:** In dp_sse/code/dp_sse.py, implements differential private SSE.
 * **DPSSE for benchmarking simulation** In dp_sse/code/dp_sse_bench.py, implements/simulates the dpsse in benchmarking.
 * **Datasets:** In dp_sse/db/*.json, there are the preprocessed dataset used to build dpsse and dpsse benchmarking.

### Submodules

We rely on the following two submodules:
1. [FHIPE](https://github.com/kevinlewi/fhipe) for ipe support. (Note that it is not required in benchmarking.)
   1. [FLINT](http://flintlib.org/) for the C backend 
   2. [Charm](http://charm-crypto.com/) for the pairings implementation 
