//
//  Utils.cpp
//  Xcode-Zephyr
//
//  Created by Kyori on 22/09/14.
//  Copyright (c) 2014 INRIA. All rights reserved.
//

#include <stdio.h>
#include "Utils.h"


std::vector<std::string> str_split(std::string str, string limiter) {
    std::vector<std::string> tokens;
    boost::algorithm::split(tokens,str,boost::algorithm::is_any_of(limiter));
    return tokens;
}

ostream& operator<< (ostream& outs, const std::vector<std::pair<Tvalue,Tvalue> > * obj ) {
    if (obj->size() == 0)
        outs<< "<[]>";
    else {
        outs << "<[" << obj->at(0).first << "," << obj->at(0).second << "]";
        if (obj->size() > 1)
            for (int i = 1;i<obj->size();i++)
                outs << ",[" << obj->at(i).first << "," << obj->at(i).second << "]";
        outs << ">";
    }
    return outs;
}

ostream& operator<< (ostream& outs, const std::vector<Tentity> obj ) {
    if (obj.size() == 0)
        outs<< "<>";
    else {
        outs << "<" << obj[0];
        if (obj.size() > 1)
            for (int i = 1;i<obj.size();i++)
                outs << "," << obj[i];
        outs << ">";
    }
    return outs;
}

ostream& operator<< (ostream& outs, const std::set<Tvalue> obj ) {
    if (obj.size() == 0)
    outs<< "<>";
    else {
        outs << "<";
        for (auto it =obj.begin();it != obj.end();++it)
            outs << *it << ",";
        outs << ">";
    }
    return outs;
}

ostream& operator<< (ostream& outs, const std::vector<Tvalue> * obj ) {
    if (obj->size() == 0)
        outs<< "<>";
    else {
        outs << "<" << obj->at(0);
        if (obj->size() > 1)
            for (int i = 1;i<obj->size();i++)
                outs << "," << obj->at(i);
        outs << ">";
    }
    return outs;
}

ostream& operator<< (ostream& outs, const TPattern * obj ) {
    outs << "{";
    for (auto it=obj->begin(); it!=obj->end(); ++it)
        outs << *it << ",";
    outs << "}";
    return outs;
}

int count_attributes(string & str)
{
    int n = 0;
    for (string::iterator it = str.begin(); it != str.end(); it++)
    {
        if (',' == *it)
        {
            n++;
        }
    }
    return n+1;
}

bool to_numeric_format(const string& str, Tvalue& d)
{
    istringstream i(str);
    if (i >> d && i.eof())
    {
        return true;
    }
    return false;
}

// THIS FUNCTION INVERT THE VECTORS OF ATTRIBUTES, NOT MATRIX
std::vector< std::vector<Tvalue> > invert_matrix(vector< vector<Tvalue> > table) {
    vector< vector<Tvalue> > result;
    for (int j =0;j<table[0].size();j++) {
        vector<Tvalue> x;
        x.push_back(table[0][j]);
        result.push_back(x);
    }
    
    for (int i = 1;i<table.size();i++) {
        for (int j =0;j<table[i].size();j++) {
            result[j].push_back(table[i][j]);
        }
    }
    
    return result;
}


// THIS FUNCTION INVERTS THE VECTORS OF ATTRIBUTES, NOT MATRIX
vector< vector<Tvalue> > invert_context(vector< vector<Tvalue> > table) {
    std::unordered_map<Tvalue, vector<Tvalue> > m;
    vector< vector<Tvalue> > result;
    for (int j =0;j<table[0].size();j++) {
        vector<Tvalue> object;
        for (int i = 0;i<table.size();i++)
            m[table[i][j]].push_back(i);
    }
    for ( unsigned i = 0; i < m.bucket_count(); ++i) {
        result.push_back(m[i]);
    }
    return result;
}

TMap read_mapping(const char * PATH, bool delimited) {
    TMap result = TMap();
    ifstream file(PATH);
    string line_str;
    getline(file, line_str);
    unsigned int i = 0;
    while (line_str != "") {
        if (!(delimited)) {
            result[i++] = line_str;
        }
        else {
            vector<string> tokens;
            boost::algorithm::split(tokens,line_str,boost::algorithm::is_any_of("\t"));
            char * c = &tokens[0][0];
            result[atof(c)] = tokens[1];
        }
        getline(file, line_str);
    }
    file.close();
    return result;
}

bool file_exists (const std::string& name) {
    struct stat buffer;
    return (stat (name.c_str(), &buffer) == 0);
}

std::vector< std::vector<Tvalue> > read_csv_data(const string PATH)
{
    if (!(file_exists(PATH))) {
        cout << "ERROR: The context file provided does not exist" << endl;
        cout << "Context File: " << PATH << endl;
        exit(0);
    }
    
    vector< vector<Tvalue> > m;
    std::vector<Tvalue *> M;
    ifstream file(&PATH[0]);
    
    string line_str;
    getline(file, line_str);
    std::string delimiter = ",";
    while(line_str!="")
    {
        vector<Tvalue> new_row;
        //Tvalue * object = new Tvalue[P_size]
        istringstream line(line_str);
        string str;
        size_t pos = 0;
        while ((pos = line_str.find(delimiter)) != std::string::npos)
            //for (int i = 0; i < P_size; i++)
        {
            Tvalue value;
            str = line_str.substr(0,pos);
            if( to_numeric_format(str, value) == false )
            {
                cout<<"Error: Data could not be converted in numeric format."<<endl;
                cout << "Context File: " << PATH << endl;
                cout << line_str << endl;
                exit(1);
            }
            new_row.push_back(value);
            line_str.erase(0,pos+delimiter.length());
            //object[i] = value;
        }
        Tvalue value;
        if( to_numeric_format(line_str, value) == false )
        {
            cout<<"Error: Data could not be converted in numeric format."<<endl;
            cout << "Context File: " << PATH << endl;
            cout << line_str << endl;
            exit(1);
        }
        new_row.push_back(value);
        m.push_back(new_row);
        getline(file, line_str);
    }
    file.close();
    
    //cout<<"Size of the input matrix: " << m.size() << "x" << m[0].size() <<endl;
    return m;
}

std::vector<double> read_thetas(const char * PATH) {
    if (!(file_exists(PATH))) {
        cout << "ERROR: The path to the thetas file provided does not exist" << endl;
        cout << "Thetas File: " << PATH << endl;
        exit(0);
    }
    
    vector<double> results;
    ifstream file(PATH);
    string line_str;
    getline(file, line_str);
    vector<string> tokens;
    boost::algorithm::split(tokens,line_str,boost::algorithm::is_any_of(","));
    for (int i = 0;i<tokens.size();i++) {
        results.push_back(atof(&tokens[i][0]));
    }
    file.close();
    return results;
}

vector<vector<pair<double,double> > > read_intervals(const char * PATH) {
    vector<vector<pair<double,double> > > results;
    ifstream file(PATH);
    string line_str;
    getline(file, line_str);
    while (line_str != "") {
        vector<string> tokens;
        vector<pair<double,double> > aux;
        boost::algorithm::split(tokens,line_str,boost::algorithm::is_any_of(";"));
        for (int i=0;i<tokens.size();i++) {
            vector<string> margins;
            boost::algorithm::split(margins,tokens[i],boost::algorithm::is_any_of(","));
            aux.push_back(std::make_pair(atof(&margins[0][0]),atof(&margins[1][0])));
            cout << margins[0] << "," << margins[1] <<";";
        }
        cout << endl;
        results.push_back(aux);
        getline(file, line_str);
    }
    file.close();
    return results;
}