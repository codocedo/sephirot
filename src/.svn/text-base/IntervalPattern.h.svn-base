//
//  Interval.h
//  Sephirot
//
//  Created by Kyori on 27/06/14.
//  Copyright (c) 2014 Kyori. All rights reserved.
//

#ifndef __Sephirot__Interval__
#define __Sephirot__Interval__

#include <iostream>


#include <iostream>
#include <time.h>
#include <string>
#include <sstream>
#include <fstream>
#include <math.h>
#include <cfloat>
#include <set>
#include <forward_list>
#include <boost/functional/hash.hpp>
#include <boost/dynamic_bitset.hpp>

#include "IIntent.h"
#include "Config.h"
using namespace boost;

using std::pair;
using std::string;
using std::istringstream;
using std::ostringstream;
using std::cout;
using std::endl;

extern int bins;
extern bool debug;


//typedef bm::bvector<> TPattern;
extern Tvalue e;
extern Tvalue e1;
extern bool debug;



class IntervalPattern : public IIntent
{
public:
    typedef std::pair<Tvalue,Tvalue> TInterval;
    typedef std::vector< TInterval > TIntervalVector;
    const std::vector<Tvalue> * thetas;
    struct Description{
        mutable TIntervalVector * pattern;
        dynamic_bitset<> wtt;
        Description() {
            pattern = new TIntervalVector();
        };
        ~Description() {
            delete pattern;
            pattern = NULL;
        }
    };
    mutable Description * d;
    
    IntervalPattern() {d = new Description(); };
    IntervalPattern(Description * d, const std::vector<Tvalue> * thetas) : d(d), thetas(thetas) { } ;
    ~IntervalPattern() { };
	bool component_satisfies_e(int index);
    
	bool infimum_of_these_components_satisfies_e(int index1, int index2);
    
	IntervalPattern(std::vector<Tvalue> attrs, const Config * cfg, unsigned int obj);
    
    IntervalPattern(const IntervalPattern& other);
	//PatternIntent(std::vector<Tvalue> attrs, char partition_type);
    
    /* INHERITED METHODS */
    void * desc() const { return d; }
    IntervalPattern * get_less_general_intent() const;
    bool operator== (const IIntent * other) const;
    bool operator<= (const IIntent * other) const;
    IntervalPattern * operator& (const IIntent * other) const;
    void join(const IIntent * other) const;
    string to_csv() const;
    size_t hash() const;
    IntervalPattern * clone() const;
    void serialize(Jetson & writer, const Config * cfg) const;
    void clean(const IIntent * other) const { };
};

#endif /* defined(__Sephirot__Interval__) */
