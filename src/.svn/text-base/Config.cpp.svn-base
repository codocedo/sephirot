//
//  Config.cpp
//  Sephirot
//
//  Created by Kyori on 10/07/14.
//  Copyright (c) 2014 Kyori. All rights reserved.
//
#include "Config.h"
#include <algorithm>


inline std::vector<string> getKeys(string section, CSimpleIniA & ini) {
    std::vector<string> ckeys;
    CSimpleIni::TNamesDepend keys;
    ini.GetAllKeys(&section[0], keys);
    
    for (auto it=keys.begin();it!=keys.end();++it)
        ckeys.push_back(it->pItem);
    return ckeys;
}

Config::Config(char * initfilepath) : fca_type(TFCA::BINARY), type_of_partition('x'), outfilepath(""), filepath(""), bins(0),offset(0), obj_mapping_on(false), att_mapping_on(false), stability(false), prettyjson(false),invert_context(false), empty_value(std::numeric_limits<double>::min()), invert_matrix(false), min_rows(0), singleTheta(-1), delimiter(",")
{
    CSimpleIniA ini;
    ini.SetUnicode();
    ini.LoadFile(initfilepath);
    
    
    std::vector<string> ckeys = getKeys("sephirot", ini);
    
    fca_type = ini.GetDoubleValue("sephirot", "type");
    filepath = ini.GetValue("sephirot", "context_path", "");
    outfilepath = ini.GetValue("sephirot", "lattice_path", "");
    switch (fca_type) {
        case TFCA::BINARY:
            invert_context = ini.GetBoolValue("sephirot", "transpose");
            break;
        case TFCA::LATTICE:
            //if (ini.GetBoolValue("sephirot", "thetas"))
            //    theta_intervals = read_thetas(ini.GetValue("sephirot", "thetas_file"));
            invert_context = ini.GetBoolValue("sephirot", "transpose");
            break;
        case TFCA::INTERVAL: {
            invert_matrix = ini.GetBoolValue("sephirot", "transpose");
            
            std::vector<string> ikeys = getKeys("interval",ini);
            if (std::find(ikeys.begin(),ikeys.end(),"theta") != ikeys.end())
                singleTheta = ini.GetDoubleValue("interval", "theta");
            if (std::find(ikeys.begin(),ikeys.end(),"thetas_file") != ikeys.end())
                thetaVector = read_thetas(ini.GetValue("interval", "thetas_file"));
            break;
            }
        case TFCA::PARTITION: {
            invert_matrix = ini.GetBoolValue("sephirot", "transpose");
            std::vector<string> ikeys = getKeys("partition",ini);
            
            if (std::find(ikeys.begin(),ikeys.end(),"mrows") != ikeys.end())
                min_rows = ini.GetDoubleValue("partition", "mrows");
            if (std::find(ikeys.begin(),ikeys.end(),"empty_value") != ikeys.end())
                empty_value = ini.GetDoubleValue("partition", "empty_value");
            break;
        }
        case TFCA::TBLOCKS: {
            invert_matrix = ini.GetBoolValue("sephirot", "transpose");
            std::vector<string> ikeys = getKeys("tblocks",ini);
            
            if (std::find(ikeys.begin(),ikeys.end(),"mrows") != ikeys.end())
                min_rows = (unsigned int)ini.GetDoubleValue("tblocks", "mrows");
            if (std::find(ikeys.begin(),ikeys.end(),"empty_value") != ikeys.end())
                empty_value = ini.GetDoubleValue("tblocks", "empty_value");
            if (std::find(ikeys.begin(),ikeys.end(),"thetas_file") != ikeys.end())
                thetaVector = read_thetas(ini.GetValue("tblocks", "thetas_file"));
            break;
        }
        case TFCA::HETEROGENEOUS: {
            std::vector<std::string> tokens = str_split(ini.GetValue("sephirot", "htypes"),",");
            if (ini.GetBoolValue("sephirot", "thetas"))
            thetaVector = read_thetas(ini.GetValue("sephirot", "thetas_file"));
            for (auto it=tokens.begin();it!=tokens.end();++it) {
                Tvalue x;
                if (to_numeric_format(*it, x)) {
                    htypes.push_back(x);
                }
                else {
                    cout << "ERROR: HTYPES SHOULD BE NUMERIC AND CSV." << endl;
                    exit(0);
                }
            }
            break;
        }
        default:
            cout << "ERROR: The type of FCA provided is either not supported or not valid" << endl;
            exit(0);
            break;
            
    }
    stability = ini.GetBoolValue("sephirot", "stability");
    prettyjson = ini.GetBoolValue("sephirot", "pretty_json");
    
    // EXECUTE READINGS
    _readContext();
    _postProcess();

}

void Config::_postProcess() {
    cout << "Post processing configuration *****" << endl;
    if (invert_context) _invertContext();
    else if (invert_matrix) _invertMatrix();
    if (singleTheta != -1)
        for (int i = 0; i < context[0].size(); i++)
            thetaVector.push_back(singleTheta);
}


void Config::_invertMatrix() {
    vector< vector<Tvalue> > result;
    for (int j =0;j<context[0].size();j++) {
        vector<Tvalue> x;
        x.push_back(context[0][j]);
        result.push_back(x);
    }
    
    for (int i = 1;i<context.size();i++)
        for (int j =0;j<context[i].size();j++)
            result[j].push_back(context[i][j]);
    
    context=result;
}

void Config::_invertContext() {
    std::unordered_map<Tvalue, vector<Tvalue> > m;
    vector< vector<Tvalue> > result;
    for (int j =0;j<context[0].size();j++) {
        vector<Tvalue> object;
        for (int i = 0;i<context.size();i++)
            m[context[i][j]].push_back(i);
    }
    for ( unsigned i = 0; i < m.bucket_count(); ++i) {
        result.push_back(m[i]);
    }
    context=result;
}

string Config::printType() const {
    switch (fca_type) {
        case TFCA::BINARY:
            return "Standard FCA";
        case TFCA::LATTICE:
            return "Lattice PS";
        case TFCA::INTERVAL:
            return "Interval PS";
        case TFCA::PARTITION:
            return "Partition PS";
        case TFCA::HETEROGENEOUS:
            return "Heterogeneous PS";
        default:
            return "Not Supported :p";
    }
}

void Config::print() const {
    cout << "___________________________________\n";
    cout << "CONFIGURATION:" << endl;
    cout << "--> FCA TYPE: " << printType() << endl;
    cout << "--> Filepath: " << filepath << endl;
    cout << "--> Outpath: " << outfilepath << "(.lat.txt and/or .lat.json)"<< endl;
    cout << "--> Inverted: " << (invert_context || invert_matrix) << endl;
    cout << "--> Prettyjson: " << prettyjson << endl;
    if (fca_type == TFCA::INTERVAL)
        cout << "--> Thetas: " << &thetaVector << endl;
    if ((fca_type == TFCA::PARTITION) || (fca_type == TFCA::TBLOCKS)) {
        cout << "--> Min rows: " << min_rows << endl;
        cout << "--> Empty value: " << empty_value << endl;
    }
    cout << "--> # objects: " << context.size() << endl;
    if (fca_type == TFCA::BINARY)
        cout << "--> # attrs: " << nAttributes << endl;
    else{
        cout << "--> Dimensionality: " << context[0].size() << endl;
        cout << "--> |W|: " << nAttributes << endl;
    }
    cout << "___________________________________\n\n";
}


// READ CONTEXT IN A CSV FORMAT AS A MATRIX OF VALUES
void Config::_readContext()
{
    if (!(file_exists(filepath))) {
        cout << "ERROR: The context file provided does not exist" << endl;
        cout << "Context File: " << filepath << endl;
        exit(0);
    }
    
    ifstream file(&filepath[0]);
    
    string line_str;
    getline(file, line_str);
    std::set<Tentity> attrs;
    while(line_str!="")
    {
        vector<Tvalue> new_row;
        istringstream line(line_str);
        string str;
        size_t pos = 0;
        while ((pos = line_str.find(delimiter)) != std::string::npos)
        {
            Tvalue value;
            str = line_str.substr(0,pos);
            if( to_numeric_format(str, value) == false )
            {
                cout<<"Error: Data could not be converted in numeric format."<<endl;
	       cout << line_str << " error with (" << str << ")" <<endl;
	       cout << "Context File: " << filepath << endl;
                exit(1);
            }
            attrs.insert(value);
            new_row.push_back(value);
            line_str.erase(0,pos+delimiter.length());
        }
        
        Tvalue value;
        if( to_numeric_format(line_str, value) == false )
        {
            cout<<"Error: Data could not be converted in numeric format."<<endl;
	       cout << line_str << " error with (" << str << ")" <<endl;	   
	       cout << "Context File: " << filepath << endl;	   
            exit(1);
        }
        new_row.push_back(value);
        context.push_back(new_row);
        getline(file, line_str);
    }
    file.close();
    nAttributes = (unsigned int)attrs.size();
    //cout<<"Size of the input matrix: " << m.size() << "x" << m[0].size() <<endl;
}




/**********************************************************************
 * JETSON IS A JSON WRAPPER
***********************************************************************/
Jetson::~Jetson() {
    close();
}

Jetson::Jetson(std::string path) {
    f = fopen(&path[0],"w");
    fin = new rapidjson::FileStream(f);
    writer = new rapidjson::Writer<rapidjson::FileStream>(*fin);
}
void Jetson::object()  {
    (*writer).StartObject();
}
void Jetson::close_object()  {
    (*writer).EndObject();
}
void Jetson::array()  {
    (*writer).StartArray();
}
void Jetson::close_array()  {
    (*writer).EndArray();
}

void Jetson::write(std::string s)  {
    (*writer).String(&s[0], (int)s.length());
}
void Jetson::write (int value)  {
    (*writer).Int(value);
}
void Jetson::write (unsigned int value)  {
    (*writer).Uint(value);
}
void Jetson::write (double value)  {
    (*writer).Double(value);
}
void Jetson::write(size_t value)  {
    (*writer).Int64(value);
}

void Jetson::close() {
    if (f!=NULL) {
        fclose(f);
        f=NULL;
        delete writer;
        delete fin;
        writer=NULL;
        fin = NULL;
    }
}
