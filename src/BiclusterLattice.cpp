//
//  BiclusterLattice.cpp
//  Biclusterer
//
//  Created by Kyori on 08/09/14.
//  Copyright (c) 2014 INRIA. All rights reserved.
//

#include "BiclusterLattice.h"


Concept * BiclusterLattice::create_concept(const Extent & e, const IIntent * i) {
    return new BiclusterHolder(e,i);
}

void BiclusterLattice::save_to_json(const Config * cfg) {
    Jetson writer = Jetson(cfg->json_output());
    writer.object();
    writer.write("Biclusters");
    writer.array();
    BiclusterHolder * bc = static_cast<BiclusterHolder *>(bottom_concept);
    bc->serialize_chain(writer,cfg);
    writer.close_array();
    writer.close_object();
    writer.close();
    bottom_concept->clear_flag();
}