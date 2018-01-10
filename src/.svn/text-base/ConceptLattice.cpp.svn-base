#include "ConceptLattice.h"
#include <rapidjson/prettywriter.h>	// for stringify JSON
#include <rapidjson/filestream.h>	// wrapper of C stream for prettywriter as output
#include <cstdio>
#include <iostream>

Concept * ConceptLattice::create_concept(const Extent & e, const IIntent * i) {
    return new Concept(e,i);
}

ConceptLattice::ConceptLattice(int first_obj_num, const IIntent * first_intent) : size_var(1) {
    // bottom_concept is fake but necessary
    //if (debug) cout << "FIRST INTENT" << first_intent.to_csv()<<endl;

    IIntent * copy =first_intent->clone();
    //bottom_concept = new Concept(Extent(), copy);
    bottom_concept = create_concept(Extent(), copy);
    //bottom_concept->minimize_intent(first_intent);
    //if (debug) cout << "BOTTOM MINIMIZED" << endl;
    Extent extent = Extent();
    extent.push_back(first_obj_num);
    Concept* object_concept = create_concept(extent, first_intent);
    bottom_concept->add_parent(object_concept);
    object_concept->make_object_concept();
    //std::ostream out( cout.rdbuf());
    //print_lattice(out);
}

Concept * ConceptLattice::add_intent(Concept* generator_concept, const IIntent * intent,int obj_num)
{
    //if(debug) cout << "CALL: " << generator_concept->intent_var.to_csv() << " , " << intent.to_csv() <<endl<<endl;
    //if(debug) cout << endl << "Generator: " << generator_concept->extent_to_csv() <<" |  " << generator_concept->intent_var.to_csv() << endl;
    //if(debug) cout << "---------------------------------------------------------------" << endl;
    //if(debug) cout << "\nBEGIN [AddIntent object:" << obj_num << ", intent: " << intent.to_csv() << "]" << endl << "\t -> GENERATOR: " << endl << "\t\t -> EXTENT: " << generator_concept->extent_to_csv() << "\n\t\t -> INTENT: "<< generator_concept->intent_var.to_csv() << endl;
	generator_concept = get_maximal_concept(generator_concept, intent);
    //if(debug) cout << "\t -> MAXIMAL GENERATOR: " << endl << "\t\t -> EXTENT: " << generator_concept->extent_to_csv() << "\n\t\t -> INTENT: "<< generator_concept->intent_var.to_csv() << endl;
    //if(debug) cout << "MAXIMAL" << generator_concept->extent() << "|:" << generator_concept->intent_var.to_csv() << endl;
    
	if(generator_concept!=bottom_concept)
	{
		if (*generator_concept->intent_var == intent) {
            delete intent;
            intent = NULL;
			return generator_concept;
		}
	}
    Concept::Children generator_children = generator_concept->children();
	//const Children& generator_children =
	Concept::Children new_children;
	Concept* candidate = 0;
    Concept* child = 0;
	for (unsigned int i = 0;i < generator_children.size(); i++)
    {
        
        //if(debug) cout << "GenChild: " << generator_children[i]->extent_to_csv() << endl;
        //if (true){
        candidate = generator_children[i];
        
        if (!(*candidate->intent_var <= intent))
        {
            IIntent * new_candidate = *generator_children[i]->intent_var & intent;
            //SetIntent new_candidate = candidate->intent_var & intent;
            candidate = add_intent(candidate, new_candidate,obj_num);
        }
        
        bool add_parent = true;
        for (unsigned int j = 0; j < new_children.size(); j++)
        {
            child = new_children[j];
            if (*candidate->intent_var <= child->intent_var) {
                //if(debug) cout << "PREV CHILD: " << child->extent_to_csv() << endl;
                add_parent = false;
                break;
            } else if (*child->intent_var <= candidate->intent_var) {
                size_t len = new_children.size()-1;
                new_children[j] = new_children[len];
                new_children.resize(len);
                j--;
            }
        }
        if (add_parent)
        {
            //if(debug) cout << "NEW CHILDREN" << candidate->extent_to_csv() << endl;
            new_children.push_back(candidate);
        }
        //}

	}
    
    //if(debug) cout << "NEW CONCEPT:";
	Concept* new_concept = create_concept(generator_concept->extent(), intent);
    //if(debug) cout << new_concept->extent_to_csv() << obj_num << intent.to_csv() << endl;
    //if(debug) cout << "--" << endl << endl;
	size_var += 1;
	for (unsigned int i = 0;i < new_children.size();i++) {
		child = new_children[i];
		generator_concept->remove_child(child);
		new_concept->add_parent(child);
	}
	generator_concept->add_parent(new_concept);
	return new_concept;
}

Concept* ConceptLattice::get_maximal_concept(Concept* generator_concept, const IIntent* intent) const
{
	bool child_is_maximal = true;
	Concept *child;
	while (child_is_maximal) {
		child_is_maximal = false;
        const Concept::Children & children = generator_concept->children();
        //Children children = get_usable_children(generator_concept);
		for (unsigned int i=0;i<children.size();i++) {
			child = children[i];
            if (debug) cout << "get_maximal_children: " << child->extent_to_csv() << " >= " << child->print_children() << endl;
			if  (*intent <= child->intent_var) {
				generator_concept = child;
				child_is_maximal = true;
				break;
			}
		}
	}
	return generator_concept;
}


void ConceptLattice::add_object(Concept* concept, int obj) {
	concept->add_to_extents_in_my_sublattice(obj);
}



void ConceptLattice::add_object(int obj_num, const IIntent * intent)
{
    if(debug) cout << "SetIntent: " << intent->to_csv() << endl ;
    //if(debug) cout << "Bottom: " << bottom_concept->intent_var.to_csv() << endl ;
	bottom_concept->minimize_intent(intent);
	Concept* concept = add_intent(bottom_concept, intent,obj_num);
    //if(debug) cout << "Concept" << concept->intent_var.to_csv() << endl;
	add_object(concept, obj_num);
    concept->make_object_concept();
    
	// Can also use Writer for condensed formatting
    
    //std::ostream out( cout.rdbuf());
    //print_lattice(out);
}

void ConceptLattice::save_to_json(const Config * cfg) {
    Jetson writer = Jetson(cfg->json_output());
    writer.object();
    writer.write("ConceptLattice");
    writer.array();
    bottom_concept->serialize_chain(writer,cfg);
    writer.close_array();
    writer.close_object();
    writer.close();
    bottom_concept->clear_flag();
}

void ConceptLattice::clean_lattice() {
    bottom_concept->clean_lattice();
}

void ConceptLattice::print_lattice(std::ostream & file)
{
    if(debug) cout << endl;
	//bottom_concept->print_concepts(file);
    bottom_concept->print_chain(file,1);
    bottom_concept->clear_flag();
}

int ConceptLattice::size() {
	return size_var;
}

void ConceptLattice::calculate_stability() {
    bottom_concept->clear_flag();
    bottom_concept->initialize_stability();
    bottom_concept->clear_flag();
    while (bottom_concept->calculate_stability()) {
        bottom_concept->clear_flag();
    }
    bottom_concept->clear_flag();
}

void ConceptLattice::calculate_things() {
    bottom_concept->calculate_differences();
}



