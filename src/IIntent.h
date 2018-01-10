//
//  IIntent.h
//  Sephirot
//
//  Created by Kyori on 08/07/14.
//  Copyright (c) 2014 Kyori. All rights reserved.
//

#ifndef Sephirot_IIntent_h
#define Sephirot_IIntent_h



#include <iostream>
#include "Config.h"


/**
 Intent interface.
 This interface gives the basic behaviour for any intent that can be supported by Sephirot.
 Each intent has to implement each one of these actions. Furthermore, each intent should have a given associated description, e.g. a set pattern intent will have a set intent associated. This should be returned by desc() and then cast down to the actual type.
 */
class IIntent
{
public:
    virtual ~IIntent(){}
    //mutable size_t h;
    // Obtain the description associated to the intent.
    virtual void * desc() const = 0;
    // Compare if two intents are equal, e.g. {a,b} == {c,d} --> false.
    virtual bool operator== (const IIntent * other) const = 0;
    // Compare if an intent is less general than another. Always consider that a \sqcap b = a \iff a <= b. i.e. {a,b} intersected with {a} = {a} \iff {a} <= {a,b}
    virtual bool operator<= (const IIntent * other) const = 0;
    // Apply the similarity operator to two intents, e.g. for sets it is intersection.
    virtual IIntent * operator& (const IIntent * other) const = 0;
    // Generates a unique hash for the content of the intent (use string hash together with to_csv).
    virtual size_t hash() const = 0;
    // Generates a csv version of the intent.
    virtual std::string to_csv() const = 0;
    // Apply join operation to two intents. In AddIntent, only reserved for being applied to the more general intent with another intent, so it can be a naive approximation of the join operation or simply an empty function (the most general intent would be empty).
    virtual void join(const IIntent * other) const = 0;
    // Generate a copy in memory of this intent.
    virtual IIntent * clone() const = 0;
    // Use the JSON wrapper to write the intent to a JSON format.
    virtual void serialize(Jetson & writer, const Config * cfg) const =0;
    // Clean the intent with another intent, generally a less general intent. This can be used to output the attribute intents.
    virtual void clean(const IIntent * other) const = 0;
    // Check if the intent is empty.
    bool empty() const { return false; };
};


#endif
