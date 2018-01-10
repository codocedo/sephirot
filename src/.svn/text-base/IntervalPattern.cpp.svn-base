//
//  Interval.cpp
//  Sephirot
//
//  Created by Kyori on 27/06/14.
//  Copyright (c) 2014 Kyori. All rights reserved.
//

#include "IntervalPattern.h"
#include <math.h>

IntervalPattern::IntervalPattern(std::vector<Tvalue> attrs, const Config * cfg, unsigned int obj)
{
    d = new Description();
    if (attrs.size() > 0) {
        for (auto it=attrs.begin(); it!=attrs.end(); ++it)
            d->pattern->push_back(std::make_pair(*it, *it));
        d->wtt = dynamic_bitset<>(d->pattern->size());
        d->wtt.set();
    }
    else {
        d->pattern->push_back(std::make_pair(-1, -1));
        d->wtt = dynamic_bitset<>(d->pattern->size());
    }
    thetas = &(cfg->thetaVector);
    if (d->pattern->size() != thetas->size()) {
        cout << "ERROR: The number of theta values proposed ("<<thetas->size()<<") is not the same as the number of intervals for object "<< obj << "("<<d->pattern->size()<<")"<< endl;
        exit(0);
    }
}


void IntervalPattern::join(const IIntent * other) const
{
    Description * op = static_cast<Description *>(other->desc());
    d = new Description();
    TInterval pair = std::make_pair(std::numeric_limits<double>::max(),std::numeric_limits<double>::min());
    for (unsigned int i=0;i<=op->pattern->size();i++)
        d->pattern->push_back(pair);
    d->wtt = dynamic_bitset<>(d->pattern->size());
}

bool IntervalPattern::component_satisfies_e(int index)
{
    return (d->pattern->at(index).second - d->pattern->at(index).first <= thetas->at(index));
}

bool IntervalPattern::operator== (const IIntent * other) const
{
    Description * op = static_cast<Description *>(other->desc());
    return (*d->pattern == *op->pattern);
}

// WHEN THE INTERVALS OF OTHER ARE SMALLER ([0,2] <= [1,1]) == true
bool IntervalPattern::operator<= (const IIntent * other) const
{
   Description * op = static_cast<Description *>(other->desc());
    if (d->wtt.count() == 0)
        return true;
    else if (op->wtt.count() == 0)
        return false;
    for (int i = 0; i<d->pattern->size(); i++) {
        if (op->wtt[i] && d->wtt[i]) {
            if ((op->pattern->at(i).first < d->pattern->at(i).first) || (op->pattern->at(i).second > d->pattern->at(i).second))
                return false;
        }
        else if ((!(op->wtt[i])) && (d->wtt[i]))
            return false;
    }
    return true;
}

IntervalPattern * IntervalPattern::operator& (const IIntent * other) const
{
    Description * op = static_cast<Description *>(other->desc());

    Description * intersection = new Description();
    //cout << "INTERSECTING: " << d->pattern << op->pattern << endl;
    //cout << thetas << endl;
    intersection->wtt = d->wtt & op->wtt;
    for (int i = 0; i<d->pattern->size(); i++) {
        if (intersection->wtt[i]) {
            TInterval ni = std::make_pair(std::min(d->pattern->at(i).first, op->pattern->at(i).first), std::max(d->pattern->at(i).second, op->pattern->at(i).second));
            if ((ni.second - ni.first) > thetas->at(i)) {
                intersection->wtt[i] = 0;
                intersection->pattern->push_back(std::make_pair(-1,-1));
            }
            else
                intersection->pattern->push_back(ni);
        }
        else
            intersection->pattern->push_back(std::make_pair(-1,-1));
    }
    //cout << "RESULT: " << intersection->pattern << endl;
    return new IntervalPattern(intersection,thetas);
}


string IntervalPattern::to_csv() const
{
    ostringstream s;
    for (auto it=d->pattern->begin(); it!=d->pattern->end();++it) {
        s << "[" << it->first << "," << it->second << "]";
    }
    s << "S:"<< d->wtt;
    return s.str();
}

void IntervalPattern::serialize(Jetson & writer, const Config * cfg) const {
    writer.write(to_csv());
}

size_t IntervalPattern::hash() const{
    boost::hash<std::string> string_hash;
    return string_hash(to_csv());
}

IntervalPattern * IntervalPattern::clone() const {
    Description * newd = new Description();
    for (auto it=d->pattern->begin();it!=d->pattern->end();++it)
        newd->pattern->push_back(*it);
    newd->wtt = d->wtt;
    return new IntervalPattern(newd, thetas);
}