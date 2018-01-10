//
//  IntentFactory.cpp
//  Sephirot
//
//  Created by Kyori on 09/07/14.
//  Copyright (c) 2014 Kyori. All rights reserved.
//

#include "IntentFactory.h"

IIntent * IntentFactory::CreateIntent(std::vector<Tvalue> inat, const Config * cfg, unsigned int obj) {
    switch (cfg->fca_type) {
        case TFCA::BINARY:
            return new SetIntent(inat, cfg, obj);
            break;
        case TFCA::HETEROGENEOUS:
            return new StarIntent(inat,cfg,obj);
            break;
        case TFCA::INTERVAL:
            return new IntervalPattern(inat,cfg,obj);
            break;
        case TFCA::PARTITION:
            return new PartitionPattern(inat,cfg,obj);
            break;
        case TFCA::TBLOCKS :
            return new TBIntent(inat,cfg,obj);
            break;
        default:
            cout << "ERROR: PLEASE, PROVIDE A VALID FCA TYPE." << endl;
            exit(0);
            break;
    }
}

IIntent * IntentFactory::CreateIntentSpec(std::vector<Tvalue> inat, const Config * cfg, unsigned int obj, unsigned int type) {
    switch (type) {
        case TFCA::BINARY:
            return new SetIntent(inat, cfg, obj);
            break;
        case TFCA::HETEROGENEOUS:
            return new StarIntent(inat,cfg,obj);
            break;
        case TFCA::INTERVAL:
            return new IntervalPattern(inat,cfg,obj);
            break;
        case TFCA::PARTITION:
            return new PartitionPattern(inat,cfg,obj);
            break;
        case TFCA::TBLOCKS :
            return new TBIntent(inat,cfg,obj);
            break;
        default:
            cout << "ERROR: PLEASE, PROVIDE A VALID FCA TYPE." << endl;
            exit(0);
            break;
    }
}