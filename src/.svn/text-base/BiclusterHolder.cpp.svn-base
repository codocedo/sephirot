//
//  BiclusterHolder.cpp
//  Biclusterer
//
//  Created by Kyori on 08/09/14.
//  Copyright (c) 2014 INRIA. All rights reserved.
//

#include "BiclusterHolder.h"

void BiclusterHolder::serialize_chain(Jetson & writer, const Config * cfg) {
    if (!flag_var) {
        set_flag();
        Serialize(writer,cfg);
        for (unsigned int i=0;i<children_var.size();i++) {
            BiclusterHolder * ch = static_cast<BiclusterHolder *>(children_var[i]);
            ch->serialize_chain(writer,cfg);
        }
    }
}

void BiclusterHolder::Serialize(Jetson & writer, const Config * cfg) const {
    writer.object();
    writer.write("id");
    writer.write(intent_var->hash());
    const PartitionPattern * p = static_cast<const PartitionPattern *>(intent_var);
    if ((extent_var.size() > 1) && (!(p->empty()))) {
        writer.write("Objects");
        writer.array();
        
        
        unsigned int support = 0;
        if (cfg->obj_mapping_on) {
            for (auto it=extent_var.begin(); it!=extent_var.end();++it) {
                auto it2 = cfg->obj_map.find(*it);
                if (it2 != cfg->obj_map.end())
                    writer.write(it2->second[0]);
                else
                    writer.write("NOT_FOUND");
                support++;
            }
        }
        else {
            for (auto it=extent_var.begin(); it!=extent_var.end();++it) {
                writer.write(*it);
                support++;
            }
        }
        writer.close_array();
        writer.write("Support");
        writer.write(support);
        writer.write("Attributes");
        intent_var->serialize(writer,cfg);
    }
    writer.write("Parents");
    writer.array();
    for (auto it=children_var.begin(); it!=children_var.end();++it)
        writer.write((*it)->intent_var->hash());
    writer.close_array();
    
    if (cfg->stability) {
        writer.write("Stability");
        writer.write(sdata.stability);
        //writer->String("Count",5);
        //writer->Int(sdata.count);
        //writer->String("SS",2);
        //writer->LongLong(sdata.subsets);
    }
    writer.close_object();
}