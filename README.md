# sephirot
FCA algorithms for C++

## Introduction

Sephirot is an open source implementation in C++ of the AddIntent algorithm. It currently supports three different types of pattern structures:

Set patterns (i.e. standard FCA).
Partition patterns
Heterogeneous pattern structures

## Installation

The source code dependes on three C++ libraries that can be obtained from the following sites: * Rapidjson: https://code.google.com/p/rapidjson/ * Boost: http://www.boost.org/ * Simpleini: https://github.com/brofield/simpleini * make

Once you have download and installed these dependencies, please modify the Makefile accordingly changing in the INC flag the paths to the corresponding headers. Then, run: make -j

## Execution

Sephrot's only parameter of execution is the .ini file. Examples of the .ini files are provided in the ini folder. The entries are the following:

context: path to the context file in csv format (examples are provided in the contexts file).
outfilepath: path to the output lattice. Two files will be created, one with a suffix .lat.txt which contains an ad-hoc format to represent the lattice as line per formal concept and a .lat.json file which represents the lattices as a json file.
partition_limit: minimal number of rows per partition (0 per default means no limits).
pretty_json: unimplemented (true or false)
stability: calculate similarity (true or false)
type: Type of pattern structure (0 for set patter, 1 for partition patterns, 2 for heterogeneous patterns).
thetas: Use a file to indicate the thetas to use for partitions
thetas_file: path to the thetas file
transpose: transpose or not the matrix. (true or false)
