//
//  IntentFactory.h
//  Sephirot
//
//  Created by Kyori on 09/07/14.
//  Copyright (c) 2014 Kyori. All rights reserved.
//

#ifndef __Sephirot__IntentFactory__
#define __Sephirot__IntentFactory__

#include "SetIntent.h"
#include "StarIntent.h"
#include "IntervalPattern.h"
#include "PartitionPattern.h"
#include "TBIntent.h"
#include "Config.h"

#include <iostream>
class IntentFactory {
public:
    static IIntent * CreateIntent(std::vector<Tvalue> inat, const Config * cfg, unsigned int obj);
    static IIntent * CreateIntentSpec(std::vector<Tvalue> inat, const Config * cfg, unsigned int obj, unsigned int type);
};

#endif /* defined(__Sephirot__IntentFactory__) */
