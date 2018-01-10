//
//  BiclusterLattice.h
//  Biclusterer
//
//  Created by Kyori on 08/09/14.
//  Copyright (c) 2014 INRIA. All rights reserved.
//

#ifndef __Biclusterer__BiclusterLattice__
#define __Biclusterer__BiclusterLattice__

#include <iostream>
#include "ConceptLattice.h"
#include "BiclusterHolder.h"

/**
 * Biclusters can be obtained from standard partition pattern structures and a standard pattern concept lattice.
 In fact, the only implementation difference is how formal concepts are written in the output. This class wraps the partition concept lattice to contain biclusters holders instead of concepts (wrappers of concepts) that are spetialized as writting biclusters. Also, it implements a new strategy for cleaning partitions and thus, writing only maximal biclusters.
 */
class BiclusterLattice : public ConceptLattice {
public:
    BiclusterLattice(int first_obj_num, const IIntent * first_intent) : ConceptLattice(first_obj_num,first_intent) { };
    void save_to_json(const Config * cfg);
    // Clean partitions to write only maximal biclusters.
    void clean_concepts() { bottom_concept->clean_chain(); }
protected:
    Concept * create_concept(const Extent & e, const IIntent * i);
};
#endif /* defined(__Biclusterer__BiclusterLattice__) */
