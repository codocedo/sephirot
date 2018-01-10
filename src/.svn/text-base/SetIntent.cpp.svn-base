//
//  SetIntent.cpp
//  HFCA
//
//  Created by Kyori on 28/03/14.
//  Copyright (c) 2014 Kyori. All rights reserved.
//

#include <algorithm>
#include <boost/functional/hash.hpp>
#include "SetIntent.h"
extern bool debug;

IIntent * SetIntent::clone() const {
    return new SetIntent(*this);
}

SetIntent::~SetIntent() {
    delete attributes;
    attributes = NULL;
}

SetIntent::SetIntent() {
    attributes = new TPattern();
}

SetIntent::SetIntent(const SetIntent& other) {
    attributes = new TPattern(*other.attributes);
}

void SetIntent::join(const IIntent * other) const {
    TPattern * op = static_cast<TPattern*>(other->desc());
    attributes->insert(op->begin(),op->end());
}

SetIntent::SetIntent(vector<Tvalue> inat, const Config * cfg, unsigned int obj) {
    attributes = new TPattern();
    attributes->insert(inat.begin(), inat.end());
}


bool SetIntent::operator== (const IIntent * other) const {
    TPattern * op = static_cast<TPattern*>(other->desc());
//    if (debug) cout<< "BEGIN [SET-COMP-==]" << endl << "\t ->" << to_csv() << " & " << other.to_csv() << endl;
    bool answer  = (*attributes == *op);
//    if (debug) cout << "\t -> RESULT: " << answer << endl << "END [SET-COMP-==]" << endl;
    return (answer);
}

bool SetIntent::operator<= (const IIntent * other) const {
    TPattern * op = static_cast<TPattern*>(other->desc());
    bool answer = std::includes(op->begin(), op->end(), attributes->begin(), attributes->end());
    return (answer);
}

IIntent * SetIntent::operator& (const IIntent * other) const {
    TPattern * op = static_cast<TPattern*>(other->desc());
    //if (debug) cout<< "BEGIN [SET-INTERSECTION]" << endl << "\t ->" << to_csv() << " & " << other->to_csv() << endl;
    SetIntent * intersection = new SetIntent();
    std::set_intersection(attributes->begin(), attributes->end(), op->begin(), op->end(), std::inserter(*intersection->attributes, intersection->attributes->begin() ) );
    //cout << "\t -> RESULT: " << intersection->to_csv() << endl << "END [SET-INTERSECTION]" << endl;
    return intersection;
}

void SetIntent::serialize(Jetson & writer, const Config *cfg) const{
    writer.array();
    for (auto it=attributes->begin(); it!=attributes->end();++it)
        writer.write(*it);
    writer.close_array();
};


size_t SetIntent::hash() const{
    boost::hash<std::string> string_hash;
    return string_hash(to_csv());
}

std::string SetIntent::to_csv() const {
    std::ostringstream s;
    s << attributes;
    return s.str();
}