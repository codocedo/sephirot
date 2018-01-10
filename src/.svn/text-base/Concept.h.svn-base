//
//  Concept.h
//  BiLinkage
//
//  Created by Kyori on 06/02/14.
//  Copyright (c) 2014 Kyori. All rights reserved.
//

#ifndef BiLinkage_Concept_h
#define BiLinkage_Concept_h
#include "IIntent.h"
#include "Config.h"
#include <set>
#include <vector>

//using std::vector;
using std::set;

struct StabilityData {
    int count;
    double subsets;
    double stability;
};

class Concept
{
protected:
    bool flag();
    void set_flag();
    void recalculate_intent();
    void add_to_extent(int obj);
    
    size_t diff;
    Extent extent_var;
    bool flag_var;
    bool object_concept;

    
public:
    StabilityData sdata;
    typedef std::vector<Concept * > Children;
    const IIntent * intent_var;
    Children children_var;
    
    // CONSTRUCTORS
    Concept(const Extent & extent, const IIntent * intent);
    Concept(const Extent & extent);
    
    // DESTRUCTOR
    ~Concept();
    
    // ACCESSORS
    const Extent & extent();
    const Children& children() const;
    
    // PRINT METHODS
    void print_chain(std::ostream & file,int level);
    void print_concepts(std::ostream & file);
    string to_str(int level) const;
    string extent_to_csv() const;
    string print_children() const;
    
    
    // INTENT METHODS
    void minimize_intent(const IIntent * intent);
    //set< TPattern > clean_intent() const;

    // CONCEPT METHODS
    void add_parent(Concept* concept);
    void remove_child(Concept * concept);
    void make_object_concept() { object_concept = true; };
    bool is_object_concept() const {return object_concept; };

    // LATTICE METHODS
    void add_to_extents_in_my_sublattice(int obj);
    void traverse_the_lattice( );
    void clean_lattice();
    void clean_chain();
    void calculate_differences();
    void calc_chain();
    void calc_diff(Extent ext);
    void initialize_stability();
    bool calculate_stability();
    void propagate_subsets(int subsets);
    void clear_flag();
    

    // BICLUSTERING METHODS
    //void clean_chain();
    //void get_maximal_biclusters_print_std();
    //set< std::vector<int> > classes_of_tolerance;
    
    void serialize_chain(Jetson & writer, const Config * cfg) {
        if (!flag_var) {
            set_flag();
            Serialize(writer,cfg);
            for (unsigned int i=0;i<children_var.size();i++)
                children_var[i]->serialize_chain(writer,cfg);
        }
    }
    
    void Serialize(Jetson & writer, const Config * cfg) const {
        writer.object();
        writer.write("id");
        writer.write(intent_var->hash());
        
        writer.write("Extent");
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
        writer.write("Intent");
        intent_var->serialize(writer,cfg);
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
};


#endif
