//
//  PartitionPattern.cpp
//  Biclusterer
//
//  Created by Kyori on 01/09/14.
//  Copyright (c) 2014 INRIA. All rights reserved.
//

#include "PartitionPattern.h"
#include <map>

PartitionPattern::~PartitionPattern() {
    delete d;
    d = NULL;
}

/****************************************
 * CONSTRUCTORS
 *********************************************/

PartitionPattern::PartitionPattern(std::vector<Tvalue> & attrs, const Config * cfg, unsigned int obj)
{
    std::vector<Tentity> pidx;
    std::map<Tentity,std::vector<Tentity> > idx;
    //cout << endl <<"PRE: " << &attrs << endl;
    d = new Description(cfg->min_rows,attrs.size());
    d->strip.resize(attrs.size());
    d->strip.set();
    if (attrs.size() > 0) {
        //for (auto it=attrs.begin(); it!=attrs.end(); ++it) {
        //d->pattern = new std::vector<Tentity>(attrs.size(),EMPTY);
        
        for (int i = 0;i<attrs.size();i++) {
            if (idx.find(attrs[i]) == idx.end())
                pidx.push_back(attrs[i]);
            idx[attrs[i]].push_back(i);
        }
        int i = 1;
        for (auto it=pidx.begin();it!=pidx.end();++it) {
            if ((*it != cfg->empty_value) && (idx[*it].size() >= d->min_rows)) {
                for (auto it2 = idx[*it].begin();it2!=idx[*it].end();++it2) {
                    d->pattern[*it2] = i;
                    //d->pattern->operator[](*it2) = i;
                }
                i++;
            }
            else
                for (auto it2 = idx[*it].begin();it2!=idx[*it].end();++it2) {
                    d->strip[*it2] = 0;
                }
        }
        
    }
    else {
        cout << "ERROR: Row "<<  obj << " in the datatable is empty. "<< obj;
        exit(0);
    }
    //    cout << "REP: " << d->pattern << endl;
    //cout << "PARTITION PATTERN: " << to_csv() << endl;
}


/****************************************
 * OPERATORS
 *********************************************/

bool PartitionPattern::Description::operator== (const PartitionPattern::Description * other) const {
    for (int i=0;i<size;i++)
        if ((pattern[i] != other->pattern[i]))
            return false;
    return true;
}
string PartitionPattern::Description::to_csv() const {
    ostringstream s;
    string sep = "";
    for (int i=0;i<size;i++) {
        s << sep << pattern[i];
        sep = ",";
    }
    return s.str();
}

bool PartitionPattern::empty() const {
    if (d->strip.count() == 0)
        return true;
    return  false;
}




PartitionPattern * PartitionPattern::get_less_general_intent() const {
    Description * newd = new Description(d->min_rows,d->size);
//    for (auto it = d->pattern->begin();it!=d->pattern->end();++it)
//        newd->pattern->push_back(0);
    newd->strip.resize(newd->size);
    newd->strip.set();
    return new PartitionPattern(newd);
}

PartitionPattern * PartitionPattern::clone() const {
    Description * newd = new Description(d->min_rows,d->size);
//    for (auto it = d->pattern->begin();it!=d->pattern->end();++it) {
    for (int i =0; i<d->size; i++) {
        newd->pattern[i] = d->pattern[i];
    }
//        newd->pattern->push_back(*it);
//    }
    newd->strip = d->strip;
    return new PartitionPattern(newd);
}




bool PartitionPattern::operator==(const IIntent *other) const {
    //cout << "COMPARING ==" << endl;
    Description * op = static_cast<Description *>(other->desc());
    bool result = (*op == d);
    //delete op;
    //op = NULL;
    //cout << this->to_csv() <<  " =? " << other->to_csv() << " = " ;
    //cout << result << endl;
    //cout << "END COMPARING ==" << endl << endl;
    return result;
}

// a \sqsubseteq b \iff a \sqcap b = a
// 12|3|45 \sqcap 123|45 = 12|3|45 \implies
// 12|3|45 <= 123|45
bool PartitionPattern::operator<=(const IIntent *other) const {
    //cout << "COMPARING <=" << endl;
    //cout << to_csv() << " with " << other->to_csv() << ": ";
    
    Description * op = static_cast<Description *>(other->desc());
    
    if (d->strip.count() == 0){
        //cout << "TRUE1" << endl;
        return true;
    }
    else if(op->strip.count() == 0) {
        //cout << "FALSE2" << endl;
        return false;
    }
    
    if ((op->strip & d->strip) != d->strip) {
        //cout << "FALSE3" << endl;
        return false;
    }
    
    bool result = (*op == d);
    if (result) {
        //cout << "TRUE4" << endl;
        return true;
    }
    
    std::map<Tentity, Tentity> idx;
//    for(int i = 0;i<d->pattern->size();i++) {
    for(int i = 0;i<d->size;i++) {
        //    for (auto it=op->pattern->begin(); it!=op->pattern->end(); ++it) {
        if (d->pattern[i] != 0) {
            if (idx.find(d->pattern[i]) == idx.end())
                idx[d->pattern[i]] = op->pattern[i];
            else if (idx[d->pattern[i]] != op->pattern[i]) {
                //cout << "FALSE5" << endl;
                return false;
            }
        }
    }
    //PartitionPattern * intersection = (*this) & other;
    //bool result = (this->operator==(intersection));
    //cout << intersection->to_csv() << endl;
    //cout << result << "RESULT" << endl;
    //delete op;
    //delete intersection;
    //op = NULL;
    //intersection = NULL;
    //cout << "TRUE6" << endl;
    return true;
}


PartitionPattern * PartitionPattern::operator&(const IIntent *other) const {
    //cout << "INTERSECTING" << endl;
    //cout << to_csv() << " with " << other->to_csv() << endl;
    Description * op = static_cast<Description *>(other->desc());
    Description * newd = new Description(d->min_rows,d->size);
//    newd->pattern = new std::vector<Tentity>(d->pattern->size(),EMPTY);
    newd->strip = d->strip & op->strip;
    //cout << "MIN_ROWS" << d->min_rows << endl;
    if (newd->strip.count() >= d->min_rows) {
        //std::map<std::pair<Tvalue,Tvalue>, Tvalue> hashlb;
        std::map<std::pair<Tentity,Tentity>, std::vector<Tentity> > idx;
        std::vector<std::pair<Tentity,Tentity> > pidx;
        
        
        for (int i = 0;i<d->size;i++) {
            if (newd->strip[i]) {
            //if ((d->pattern->operator[](i)!=EMPTY) && (op->pattern->operator[](i)!=EMPTY)) {
                std::pair<Tentity, Tentity> x = std::make_pair(d->pattern[i], op->pattern[i]);
                if (idx.find(x) == idx.end())
                    pidx.push_back(x);
                idx[x].push_back(i);
                //newd->pattern->push_back(hashlb[x]);
            }
        }
        // STRIP PARTITIONS. I.E. PARTITIONS WITH ONE COMPONENT ARE STRIPPED OUT.
        int i = 1;
        for (auto it=pidx.begin();it!=pidx.end();++it) {
            if (idx[*it].size() >= d->min_rows) {
                for (auto it2 = idx[*it].begin();it2!=idx[*it].end();++it2) {
                    newd->pattern[*it2] = i;
                }
                i++;
            }
            else
                for (auto it2 = idx[*it].begin();it2!=idx[*it].end();++it2) {
                    newd->strip[*it2] = 0;
                }
        }
    }
    else
        newd->strip.reset();
    
    //delete op;
    //op = NULL;
    
    //cout << endl << endl << this->to_csv() <<  " & " << other->to_csv() << " = " ;
    PartitionPattern * out = new PartitionPattern(newd);
    //cout << out->to_csv() << endl;
    //cout << "END INTERSECTING" << endl;
    return out;
}

void PartitionPattern::serialize(Jetson & writer, const Config * cfg) const {
    TParti partition = signature2partition();
    writer.array();
    for (auto it=partition.begin(); it!=partition.end(); ++it) {
        writer.array();
        for (auto it2=it->begin(); it2!=it->end(); ++it2)
            writer.write(*it2);
        writer.close_array();
    }
    writer.close_array();
    //writer.write(to_csv());
}

size_t PartitionPattern::hash() const {
    boost::hash<std::string> string_hash;
    ostringstream s;
    s << d->pattern << d->strip;
    return string_hash(s.str());
}

PartitionPattern::TParti PartitionPattern::signature2partition() const {
    TParti partition;
    std::map<Tentity, std::vector<Tentity> > hashlb;
    for (int i=0;i<d->size;i++)
        if (d->strip[i] == 1)
            hashlb[d->pattern[i]].push_back(i);
    for (auto it=hashlb.begin();it!=hashlb.end();++it) {
        std::vector<Tentity> component;
        for (auto it2=it->second.begin();it2!=it->second.end();++it2)
            component.push_back(*it2);
        partition.push_back(component);
    }
    return partition;
}

string PartitionPattern::to_csv() const {
    ostringstream s;
    std::map<Tentity, TSignature > hashlb;
    TParti partition = signature2partition();
    string sep1 = "",sep2="";
    for (auto it=partition.begin();it!=partition.end();++it) {
        s << sep2;
        sep1 = "";
        for (auto it2=it->begin();it2!=it->end();++it2) {
            s << sep1 << *it2;
            sep1 = ",";
        }
        sep2 = "||";
    }
    //s << "(" << d->to_csv() << ")" << " - I: " << d->strip << " || " << d->strip.count();
    return s.str();
}


/*
 THIS METHOD CLEANS THE CURRENT PARTITIONS OF THOSE COMPONENTS THAT ARE ALREADY CONTAINED IN THE CHILDREN PARTITIONS. FOR EXAMPLE, CONSIDER ac|bd and a|c|bd where a|c|bd <= ac|bd. WE WOULD LIKE TO CONSIDER THE COMPONENT bd ONLY IN a|c|bd SINCE ITS EXTENT WILL BE LARGER AND HENCE, IT WILL GENERATE A MAXIMAL BICLUSTER.
 WE RESOLVE THIS BY EXAMINING THE SIGNATURES OF EACH PARTITION. FOR ac|bd is 1212 and for a|c|bd is 1232. BY WALKING THROUGH THE SIGNATURE OF THE PARENT PARTITION WE CREATE A MAPPING CALLED IDX WHICH ASSIGNS THE ID OF THE COMPONENT IN THE CHILDREN PARTITION TO THE ID OF THE COMPONENT IN THE CURRENT PARTITION. IF THE ID IS ALREADY STORED AND IT DOES NOT COINCIDE, THEN IT IS MARKED AS SAFE. FURTHERMORE, IT THE ID HAS NOT BEEN STORED BUT THE CHILDREN HAS THE COMPONENT MARKED AS EMPTY, THEN WE SAY THAT IT IS SAFE.
 ALL COMPONENTS NOT MARKED AS SAFE ARE REMOVED.
    EX. SIGNATURES 1212 AND 1232.
 POSITION 0: IDX[1] DOES NOT EXISTS -> IDX[1] = 1
 POSITION 1: IDX[2] DOES NOT EXISTS -> IDX[2] = 2
 POSITION 2: IDX[1]:1 != 3 -> IDX[1] = SAFE
 POSITION 3: IDX[2]:2 == 2 -> NOTHING DONE.
 FINAL SIGNATURE: 1010
 */
void PartitionPattern::clean(const IIntent * child) const {
    Description * op = static_cast<Description *>(child->desc());
    if ((d->strip.count() == 0) || (op->strip.count() == 0))
        return;
    
    //TPartition x = std::vector<Tvalue>(d->pattern->size(),SAFE);
    
    //cout << "CLEANING " << to_csv() << " with " << child->to_csv() << endl;
    
    std::map<Tentity, Tentity> idx;
    for (int i = 0; i< d->size;i++) {
            if (idx.find(d->pattern[i]) == idx.end()) {
                if (op->pattern[i] == EMPTY)
                    idx[d->pattern[i]] = SAFE;
                else
                    idx[d->pattern[i]] = op->pattern[i];
            }
            else if ((idx[d->pattern[i]] != SAFE) && (idx[d->pattern[i]] != op->pattern[i])) {
                idx[d->pattern[i]] = SAFE;
        }
    }
    //cout << "IDX" << endl;
    //for (auto it=idx.begin();it!=idx.end();++it)
    //    cout << it->first << ": " << it->second << endl;
    for (int i = 0; i< d->size;i++) {
        if ((idx.find(d->pattern[i]) != idx.end()) && (idx[d->pattern[i]] != SAFE))
            d->strip[i] = 0;
            //d->pattern->operator[](i) = EMPTY;
    }
    //cout << "RESULT: " << to_csv() << endl<<endl;;
}

/*
 JOIN THE PROVIDED PARTITION WITH THIS ONE. THIS IS A NAIVE IMPLEMENTATION. IT IS DESIGNED TO JOIN THE BOTTOM WITH ANOTHER PARTITION. THE BOTTOM IS ALWAYS SUPPOSED TO HAVE A SINGLE COMPONENT IN THE PARTITION. IF THIS IS USED AS THE MAIN OPERATION FOR CONSTRUCTING THE LATTICE, THEN THE CLOSURE OF THE COMPONENTS SHOULD BE CHECKED.
 */
void PartitionPattern::join(const IIntent * other) const
{
    for (int i =0;i<d->size;i++)
        d->pattern[i] = 1;
    d->strip.set();
}