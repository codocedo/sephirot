//
//  TBPattern.h
//  Xcode-Zephyr
//
//  Created by Kyori on 23/10/14.
//  Copyright (c) 2014 INRIA. All rights reserved.
//

#ifndef __Xcode_Zephyr__TBPattern__
#define __Xcode_Zephyr__TBPattern__

#include <stdio.h>
#include "IIntent.h"
#include "Config.h"

class TBIntent : public IIntent
{
public:
    
    typedef Tvalue * TSignature;
    typedef std::set<Tvalue> TPattern;
    typedef std::vector<TPattern> TParti;

    const Tentity * min_rows;
    
    mutable TParti * pattern;
    //std::unordered_map<Tvalue, size_t> values;
    mutable size_t h;
    
    void clean_patterns() const;
    void clean_closures();
    bool component_satisfies_e(int index);
    bool infimum_of_these_components_satisfies_e(int index1, int index2);
    
    /* COSNTRUCTORS */
    TBIntent() { pattern = new TParti(); Tentity x = 1; min_rows = &x;};
    TBIntent(TParti * pattern, const Tentity * min_rows) : pattern(pattern), min_rows(min_rows) { };
    TBIntent(std::vector<Tvalue> & attrs, const Config * cfg, unsigned int obj);
    TBIntent(const TBIntent& other);
    ~TBIntent();
    
    
    static bool compareSets(TPattern t1, TPattern t2) {    if (t1.size() != t2.size())
        return (t1.size() < t2.size());
        else {
            return (t1 < t2);
        }};
    /* INHERITED METHODS */
    void * desc() const { return pattern; }
    TBIntent * get_less_general_intent() const;
    bool operator== (const IIntent * other) const;
    bool operator<= (const IIntent * other) const;
    TBIntent * operator& (const IIntent * other) const;
    void join(const IIntent * other) const;
    string to_csv() const;
    size_t hash() const;
    TBIntent * clone() const;
    bool empty() const;
    void serialize(Jetson & writer, const Config * cfg) const;
    void clean(const IIntent * other) const;
    TParti signature2partition() const;
};



#endif /* defined(__Xcode_Zephyr__TBPattern__) */
