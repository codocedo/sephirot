//
//  TBPattern.cpp
//  Xcode-Zephyr
//
//  Created by Kyori on 23/10/14.
//  Copyright (c) 2014 INRIA. All rights reserved.
//

#ifdef _OPENMP
#include<omp.h>
#endif
#include <chrono>
#include "TBIntent.h"




inline ostream& operator<< (ostream& outs, const TBIntent::TParti * obj ) {
    if (obj->size() == 0)
        outs<< "<>";
    else {
        outs << "<" ;
        for (auto it=obj->begin();it!=obj->end();++it) {
            for (auto it2=it->begin();it2!=it->end();++it2)
                outs << *it2 << ",";
            outs << "||";
        }
        outs << ">";
    }
    return outs;
}

TBIntent::~TBIntent() {
    delete pattern;
    pattern = NULL;
}

TBIntent::TBIntent(std::vector<Tvalue> & attrs, const Config * cfg, unsigned int obj) {
    min_rows = &cfg->min_rows;
    pattern = new TParti();
    if (obj >= cfg->thetaVector.size()) {
        cout << "ERROR: Thetas vector is empty or it does not contain the element required.\n\t-> Check if the thetas file exists and its length (same length of the set of attributes)" << endl;
        cout << "THETAs CONTENT: " << &cfg->thetaVector << endl;
        cout << "ELEMENT REQUIRED: " << obj << endl;
        exit(0);
    }

    double theta = cfg->thetaVector[obj];
    
    TPattern sorted_domain;
    for (auto it=attrs.begin(); it!=attrs.end(); ++it) {
        if (*it != cfg->empty_value)
            sorted_domain.insert(*it);
    }
    
    // Building domain of value
    std::vector<double> W;
    for(auto it = sorted_domain.begin();it != sorted_domain.end();++it)
        W.push_back(*it);
    //cout << &W << endl;
    std::vector<std::pair<Tvalue,Tvalue> > intervals;
    
    
    //vector<double> classesL;
    //vector<double> classesR;
    
    /// Computing blocks of tolerance over W ///
    double curL,curR;
    unsigned int i, j;
    double k = -999999999;
    
    
    for (i = 0 ; i != W.size(); i++)
    {
        curL= W[i];
        curR= W[i];
        for (j = i; j != W.size(); j++)
        {
            if (W[j] - curL <= theta)
                curR = W[j];
            else break;
        }
        if (! (curR<= k) )
            intervals.push_back(std::make_pair(curL, curR));
        //classesL.push_back(curL);
        //classesR.push_back(curR);
        k = curR;
    }
//   cout << &attrs << endl;
//    cout << &intervals << "theta: " << theta << endl;
    for (auto it=intervals.begin();it!=intervals.end();++it) {
        //cout << "[" << it->first << "," << it->second << "] ;";
        TPattern component;
        for (int j=0;j<attrs.size();j++) {
            if ((attrs[j] != cfg->empty_value) && (it->first <= attrs[j]) && (attrs[j]<= it->second))
                component.insert(j+1);
        }
        if (component.size() >= *min_rows)
            pattern->push_back(component);
        
    }
    std::sort(pattern->begin(),pattern->end(),TBIntent::compareSets);
    clean_patterns();
    //cout << &attrs  <<endl;
    //cout << " - " <<intervals.size() << "  tolerance relations found. minrows: " << *min_rows;
    //cout << pattern << endl;
    cout << "\t\t --> " << pattern->size() << " components found";
    cout.flush();
}

/****************************************
 * OPERATORS
 *********************************************/
bool TBIntent::operator== (const IIntent * other) const {
    TParti * opattern = static_cast<TParti *>(other->desc());
    
    // IF BOTH TB's HAVE DIFFERENT COMPONENTS, THEN THEY ARE INMMEDIATLY DIFFERENT.
    if (pattern->size() != opattern->size())
        return false;
    for (int i=0;i<pattern->size();i++)
        if (!(pattern->at(i) == opattern->at(i)))
            return false;
    return true;
}

// FINER <= COARSER
bool TBIntent::operator<= (const IIntent * other) const
{
    TParti * opattern = static_cast<TParti *>(other->desc());
    if (pattern->size() == 0)
        return true;
    else if (opattern->size() == 0)
        return false;

    //cout << pattern << endl <<" <=? " << opattern << endl;
    // IF THE COARSER PARTITION HAS MORE COMPONENTS, THEN IMMEDIATLY IT IS NOT COARSER
    if (opattern->size() > pattern->size())
        return false;
    int k=0;
    for (int i=0;i<pattern->size();i++) {
        bool isSubSet = false;
        for (int j=k;j<opattern->size();j++) {
            if (pattern->at(i).size() > opattern->at(j).size())
                k++;
            else
                isSubSet |= std::includes(opattern->at(j).begin(),opattern->at(j).end(),pattern->at(i).begin(),pattern->at(i).end());
        }
        if(!(isSubSet))
            return false;
    }
    return true;
}


void TBIntent::clean_patterns() const {
    std::vector<unsigned int> toDel;
    for (int i =0; i<pattern->size(); i++)
        for (int j=i+1;j< pattern->size(); j++)
            if (std::includes(pattern->at(j).begin(),pattern->at(j).end(),pattern->at(i).begin(),pattern->at(i).end())) {
                toDel.push_back(i);
                break;
            }

    if (toDel.size() > 0) {
        //cout << "CLEANING: " << pattern << " size: "<<pattern->size() <<endl;
        for (int i =0; i<toDel.size(); i++) {
            //cout << ", i:" << i<< ", toDel:" << toDel[i] << " newpos:" << toDel[i]-i <<endl;
            //cout << pattern->at(toDel[i]-i) ;
            pattern->erase(pattern->begin()+(toDel[i]-i));
        }
    }
    //cout << "CLEAN" << endl;
}

TBIntent * TBIntent::operator& (const IIntent * other) const {
    TParti opattern = *static_cast<TParti *>(other->desc());
    TParti * intersection = new TParti();
   /*
    //cout << pattern << endl <<" &= " << opattern << endl;
   std::chrono::high_resolution_clock::time_point t1 = std::chrono::high_resolution_clock::now();
    for (int i =0; i<pattern->size(); i++) {
        for (int j=0;j<opattern.size(); j++) {
            //cout << (pattern->at(i)) << endl;
            //cout << (opattern->at(j)) << endl;
            std::vector<Tvalue> cinter = std::vector<Tvalue>();
            std::set_intersection(pattern->at(i).begin(), pattern->at(i).end(), opattern[j].begin(), opattern[j].end(), std::back_inserter(cinter));

            if (cinter.size() >= *min_rows)
                intersection->push_back(TPattern(cinter.begin(),cinter.end()));
        }
    }
      std::chrono::high_resolution_clock::time_point t12 = std::chrono::high_resolution_clock::now();
    intersection->clear();   
   std::chrono::high_resolution_clock::time_point t2 = std::chrono::high_resolution_clock::now();*/
    int i,j;
    TParti op1=*pattern;

#pragma omp parallel shared(op1,opattern) private(i,j)
    {
#pragma omp for
    for (i =0; i<op1.size(); i++) {
       TParti auxInter;
        for (j=0;j<opattern.size(); j++) {
            //cout << (pattern->at(i)) << endl;
            //cout << (opattern->at(j)) << endl;
            std::vector<Tvalue> cinter = std::vector<Tvalue>();
            std::set_intersection(op1[i].begin(), op1[i].end(), opattern[j].begin(), opattern[j].end(), std::back_inserter(cinter));
	   if (cinter.size() >= *min_rows)
	     auxInter.push_back(TPattern(cinter.begin(),cinter.end()));
	}
#pragma omp critical
	   intersection->insert(intersection->end(),auxInter.begin(),auxInter.end());
    }
       
    }
    //std::chrono::high_resolution_clock::time_point t3 = std::chrono::high_resolution_clock::now();
    
    //cout << pattern->size() << "x" << opattern.size() <<": " << pattern->size()*opattern.size() <<" P" << (double)((std::chrono::duration_cast<std::chrono::microseconds>(t3-t2)).count())/1000000.0 << " S" << (double)((std::chrono::duration_cast<std::chrono::microseconds>(t12-t1)).count())/1000000.0 << endl;
    
    std::sort(intersection->begin(),intersection->end(),TBIntent::compareSets);
    //cout << intersection << endl;
    TBIntent * out  = new TBIntent(intersection, min_rows);
    out->clean_patterns();
    return out;
    
}




TBIntent * TBIntent::get_less_general_intent() const {
    TParti * n = new TParti();
    n->push_back(TPattern());
    for (int i =0; i<pattern->size(); i++)
        n->at(0).insert(pattern->at(i).begin(),pattern->at(i).end());
    
    return new TBIntent(n,min_rows);

}

void TBIntent::join(const IIntent * other) const {
    if (pattern->size() == 0)
        pattern->push_back(TPattern());
    TParti * opattern = static_cast<TParti *>(other->desc());
    for (int j=0;j< opattern->size(); j++)
        pattern->at(0).insert(opattern->at(j).begin(), opattern->at(j).end());
}

string TBIntent::to_csv() const { ostringstream s; s<<pattern; return s.str();}
size_t TBIntent::hash() const {boost::hash<std::string> string_hash;return string_hash(to_csv());}

TBIntent * TBIntent::clone() const {
    TParti * n = new TParti();
    for (int i =0; i<pattern->size(); i++)
        n->push_back(pattern->at(i));
    return new TBIntent(n,min_rows);
}


bool TBIntent::empty() const {
    return (pattern->size() == 0);
}
void TBIntent::serialize(Jetson & writer, const Config * cfg) const {
    writer.array();
    for (auto it=pattern->begin(); it!=pattern->end(); ++it) {
        writer.array();
        for (auto it2=it->begin(); it2!=it->end(); ++it2)
            writer.write(*it2);
        writer.close_array();
    }
    writer.close_array();
}
void TBIntent::clean(const IIntent * other) const { }
//TParti signature2partition() const {}


