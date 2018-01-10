//
//  Utils.h
//  HFCA
//
//  Created by Kyori on 28/03/14.
//  Copyright (c) 2014 Kyori. All rights reserved.
//

#ifndef HFCA_Utils_h
#define HFCA_Utils_h
#include <iostream>
#include <vector>
#include <set>
#include <fstream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <limits.h>
#include <algorithm>
#include <cstdlib>
#include <boost/algorithm/string/split.hpp>
#include <boost/algorithm/string/classification.hpp>
#include <rapidjson/prettywriter.h>	// for stringify JSON
#include <rapidjson/filestream.h>	// wrapper of C stream for prettywriter
#include <boost/functional/hash.hpp>
#define SI_SUPPORT_IOSTREAMS
#include <SimpleIni.h>
#include <sys/stat.h>
using namespace boost;
using namespace std;
typedef double Tvalue;
typedef unsigned int Tentity;
typedef std::vector<unsigned int> Extent;
typedef std::set<Tentity> TPattern;
typedef std::unordered_map<unsigned int, string> TMap;

enum TFCA {
    BINARY,
    PARTITION,
    HETEROGENEOUS,
    INTERVAL,
    LATTICE,
    STAR,
    TBLOCKS
};

// STRING UTILS
vector<std::string> str_split(std::string str, string limiter);
int count_attributes(string & str);
bool to_numeric_format(const string& str, Tvalue& d);

// INVERTERS
std::vector< std::vector<Tvalue> > invert_matrix(vector< vector<Tvalue> > table); // THIS FUNCTION INVERT THE VECTORS OF ATTRIBUTES, NOT MATRIX
vector< vector<Tvalue> > invert_context(vector< vector<Tvalue> > table); // THIS FUNCTION INVERTS THE VECTORS OF ATTRIBUTES, NOT MATRIX


// FILE MANAGERS
std::vector<double> read_thetas(const char * PATH);
std::vector< vector<Tvalue> > read_csv_data(const char * PATH);
TMap read_mapping(const char * PATH, bool delimited=false);
bool file_exists (const std::string& name);
std::vector< std::vector<Tvalue> > read_csv_data(const string PATH);
vector<double> read_thetas(const char * PATH);
vector<vector<pair<double,double> > > read_intervals(const char * PATH);

// WRITERS
ostream& operator<< (ostream& outs, const std::vector<std::pair<Tvalue,Tvalue> > * obj );
ostream& operator<< (ostream& outs, const std::vector<Tentity>  obj );
ostream& operator<< (ostream& outs, const std::vector<Tvalue> * obj );
ostream& operator<< (ostream& outs, const TPattern * obj );
ostream& operator<< (ostream& outs, const std::set<Tvalue> obj );
//******************************************************************************
//******************************************************************************
//******************************************************************************


/*****************************************
 METHODS FOR LATTICE INTENT AND PARTITIONS (DEPRECATED)
*****************************************/
// 1 if s1 in s2, -1 if s2 in s1, 0 if equal, 0 if none
inline int inclusion_test(TPattern s1, TPattern s2) {
    //cout << "Inclusion test"<<endl;
    //cout << &s1 << "," << &s2 << endl;
    if (s1 ==s2)
    return 2;
    
    if (std::includes(s1.begin(), s1.end(), s2.begin(), s2.end()))
    return 1;
    else if (std::includes(s2.begin(), s2.end(), s1.begin(), s1.end()))
    return -1;
    else
    return 0;
    //cout << "INTERSECTED" << endl;
    //cout << "--->" <<&s0 << endl;
    //cout << "DONE"<<endl;
}

inline std::vector< pair<Tvalue, Tvalue> > calculate_tolerance_blocs(std::vector<Tvalue> attrs,int bins) {
    std::vector< pair<Tvalue, Tvalue> > tolerance_blocks;
    Tvalue min=attrs[0];
    Tvalue max=attrs[0];
    
    for (int i =0; i< attrs.size();i++) {
        if (attrs[i] < min) min = attrs[i];
        if (attrs[i] > max) max = attrs[i];
        //    cout << attrs[i] << "->" << max << "," << min <<endl;
    }
    
    tolerance_blocks.resize(bins);
    double step = fabs(max - min) / bins;
    //    cout << "STEP " << step << endl ;
    Tvalue x;
    Tvalue y;
    for(int i =0; i< bins;i++) {
        //if (debug)cout << "[" << min+(i*step)<< "," << min+((i+1)*step) << "],";
        if (i+1 != bins) {
            x =min+(i*step);
            y = min+((i+1)*step);
        }
        else {
            x =min+(i*step);
            y = max + 1;
        }
        tolerance_blocks.push_back( pair<Tvalue, Tvalue>(x,y));
    }
    //if(debug) cout << endl;
    return tolerance_blocks;
}

inline const std::vector< pair<Tvalue, Tvalue> > get_predef_blocs() {
    std::vector< pair<Tvalue, Tvalue> > tolerance_blocks;
    tolerance_blocks.push_back(pair<Tvalue, Tvalue>(1,2));
    tolerance_blocks.push_back(pair<Tvalue, Tvalue>(3,3));
    tolerance_blocks.push_back(pair<Tvalue, Tvalue>(4,5));
    //tolerance_blocks.push_back(pair<Tvalue, Tvalue>(4,4));
    //tolerance_blocks.push_back(pair<Tvalue, Tvalue>(5,5));
    return tolerance_blocks;
}






#endif
