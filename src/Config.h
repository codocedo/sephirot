//
//  Config.h
//  Sephirot
//
//  Created by Kyori on 10/07/14.
//  Copyright (c) 2014 Kyori. All rights reserved.
//

#ifndef __Sephirot__Config__
#define __Sephirot__Config__

#include "Utils.h"
#include <iostream>

typedef rapidjson::Writer<rapidjson::FileStream> TWriter;
typedef std::vector< std::vector<Tvalue> > TContext;

class Config {
    // NON const methods
private:
    void _readContext();
    void _postProcess();
    void _invertContext();
    void _invertMatrix();
    
public:
    // STANDARD FCA
    bool stability;
    bool prettyjson; // TODO: fix the use of  pretty json flag.
    bool invert_context; // It is not the same to invert a context than a matrix
    unsigned int fca_type;
    string filepath;
    string outfilepath;
    string delimiter;
    unsigned int nAttributes;
    
    // THETAS INFORMATION - INTERVALS
    vector<vector<pair<double,double> > > thetaIntervals;
    vector<double> thetaVector;
    Tvalue singleTheta;
    
    // STAR INTENT PARAMS
    std::vector<unsigned int> htypes;
    
    unsigned int bins;
    unsigned int offset;
    
    // MAPPINGS
    bool obj_mapping_on;
    bool att_mapping_on;
    TMap obj_map;
    TMap att_map;
    
    // CONTEXT
    TContext context;
    
    // SHARED: PARTITIONS, INTERVALS
    bool invert_matrix;
    unsigned int numberOfAtts;
    
    // PARTITIONS
    Tentity min_rows;
    Tvalue empty_value;
    char type_of_partition;
    
    // DEFAULT CONSTRUCTOR
    Config() : fca_type(TFCA::BINARY), type_of_partition('x'), outfilepath(""), filepath(""), bins(0),offset(0), obj_mapping_on(false), att_mapping_on(false), stability(false), prettyjson(false),invert_context(false), empty_value(std::numeric_limits<double>::min()), invert_matrix(false), min_rows(0), singleTheta(-1), delimiter(",") { } ;
    
    // CONSTRUCTOR WITH INI FILE
    Config(char * initfilepath);
    
    void print() const;
    string json_output() const { return outfilepath + ".lat.json";}
    string txt_output() const { return outfilepath + ".lat.txt";}
    string printType() const;
    

};


class Jetson {
private:
    FILE * f;
    rapidjson::FileStream * fin;
    TWriter * writer;
public:
//    Jetson() : f(NULL), writer(NULL) {};
    Jetson(std::string path);
    ~Jetson();
    void object() ;
    void close_object() ;
    void array() ;
    void close_array() ;
    void write (string s) ;
    void write (int value) ;
    void write (unsigned int value) ;
    void write (double value) ;
    void write (size_t value) ;
    void close();
};

#endif /* defined(__Sephirot__Config__) */
