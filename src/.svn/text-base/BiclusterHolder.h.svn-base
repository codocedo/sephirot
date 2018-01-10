//
//  BiclusterHolder.h
//  Biclusterer
//
//  Created by Kyori on 08/09/14.
//  Copyright (c) 2014 INRIA. All rights reserved.
//

#ifndef __Biclusterer__BiclusterHolder__
#define __Biclusterer__BiclusterHolder__

#include <iostream>
#include "Concept.h"
#include "PartitionPattern.h"


/**
 * Biclusters can be obtained from standard partition pattern structures.
 In fact, the only implementation difference is how formal concepts are written in the output. This class wraps concept to generate a new serialization that allows to directly write biclusters.
 */
class BiclusterHolder : public Concept {
public:
    BiclusterHolder(const Extent & extent, const IIntent * intent) : Concept(extent,intent) { };
    void serialize_chain(Jetson & writer, const Config * cfg);
    void Serialize(Jetson & writer, const Config * cfg) const;
};

#endif /* defined(__Biclusterer__BiclusterHolder__) */
