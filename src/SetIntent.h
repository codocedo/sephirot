//
//  SetIntent.h
//  HFCA
//
//  Created by Kyori on 28/03/14.
//  Copyright (c) 2014 Kyori. All rights reserved.
//

#ifndef __HFCA__SetIntent__
#define __HFCA__SetIntent__

#include <iostream>
#include <vector>
#include "IIntent.h"


/**
 * Set intent is a set pattern intent implentation that is the same as standard FCA.
 */
class SetIntent : public IIntent {
public:
    // Set of unsigned ints
    TPattern * attributes;
    
    SetIntent();
    ~SetIntent();
    
    void * desc() const { return attributes; }
    SetIntent(const SetIntent& other);
    SetIntent(std::vector<Tvalue> inat, const Config * cfg, unsigned int obj);
    bool operator== (const IIntent * other) const;
    bool operator<= (const IIntent * other) const;
    IIntent * operator& (const IIntent * other) const;
    size_t hash() const;
    std::string to_csv() const;
    void join(const IIntent * other) const;
    void serialize(Jetson & writer,const Config * cfg) const;
    IIntent * clone() const;
    void clean(const IIntent * other) const { };
};


#endif /* defined(__HFCA__SetIntent__) */
