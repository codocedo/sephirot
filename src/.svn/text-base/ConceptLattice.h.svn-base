//
//  ConceptLattice.h
//  BiLinkage
//
//  Created by Kyori on 06/02/14.
//  Copyright (c) 2014 Kyori. All rights reserved.
//

#ifndef BiLinkage_ConceptLattice_h
#define BiLinkage_ConceptLattice_h
#include "IntentFactory.h"
#include "Concept.h"
#include "Config.h"


extern bool debug;
extern bool prettyjson;

class ConceptLattice
{
public:
    char type_of_partition;
    ConceptLattice() {};

    ConceptLattice(int first_obj_num, const IIntent * first_intent);
    
    
    void add_object(int obj_num, const IIntent * intent);
    void print_lattice(std::ostream & file);
    void set_type_of_partition(char type_of_partition) { type_of_partition = type_of_partition; }
    void clean_lattice();
    int size();
    void calculate_things();
    void calculate_stability();
    void save_to_json(const Config * cfg);
    void clean_concepts() { bottom_concept->clean_chain(); }
protected:
    Concept* add_intent(Concept * generator_concept, const IIntent * intent,int obj_num);
    Concept* get_maximal_concept(Concept *  generator_concept, const IIntent * intent) const;
    Concept * create_concept(const Extent & e, const IIntent * intent);
    void add_object(Concept * concept, int obj);
    Concept * bottom_concept;
    Concept * top_concept;
    //std::vector<TConcept *> object_concepts;
    int size_var;
};

#endif