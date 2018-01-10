//
//  Concept.cpp
//  BiLinkage
//
//  Created by Kyori on 06/02/14.
//  Copyright (c) 2014 Kyori. All rights reserved.
//

#include "Concept.h"
#include <iostream>
#include <sstream>
#include <fstream>
#include <math.h>
#include <vector>
#include <set>
#include <rapidjson/filestream.h>	// wrapper of C stream for prettywriter

using std::vector;
using std::cout;
using std::ostringstream;
using std::endl;
using std::ofstream;
using std::set;


extern Tvalue e;

Concept::~Concept() {
    delete intent_var;
    intent_var = NULL;
}

Concept::Concept(const Extent & ext)
:  extent_var(ext), children_var(), flag_var(false), diff(INT_MAX), object_concept(false){
}

Concept::Concept(const Extent & ext, const IIntent * inten)
: extent_var(ext), children_var(), flag_var(false), diff(INT_MAX), intent_var(inten), object_concept(false) {
}

const Extent & Concept::extent() {
	return extent_var;
}

void Concept::minimize_intent(const IIntent * other)
{
    intent_var->join(other);
    //intent_var.attributes.insert(other.attributes.begin(),other.attributes.end());
}

void Concept::add_parent(Concept * concept) {
    //cout << "LINK CREATION " << extent_to_csv() << " => " << concept->extent_to_csv() << endl;
	children_var.push_back(concept);
}

void Concept::remove_child(Concept * concept) {
    //cout << "LINKG REMOVAL " << extent_to_csv() << " => " << concept->extent_to_csv()  << endl;
	for (unsigned int i=0;i<children_var.size();i++) {
        if (children_var[i]==concept) {
            children_var[i] = children_var[children_var.size()-1];
            children_var.resize(children_var.size()-1);
            break;
        }
    }
}

const Concept::Children & Concept::children() const
{
	return children_var;
}

void Concept::add_to_extents_in_my_sublattice(int obj) {
	add_to_extent(obj);
	clear_flag();
}

void Concept::print_concepts(std::ostream & file)
{       //bottom_concept
    file << "<{}>@sep@<>@sep@<";
    file << print_children();
    file << ">@sep@<0>@sep@0 .-" << endl;
	set_flag();
    for (unsigned int i=0;i<children_var.size();i++)
        children_var[i]->print_chain(file,1);
	clear_flag();
}

bool Concept::flag() {
	return flag_var;
}

void Concept::set_flag() {
	flag_var = true;
}

void Concept::clear_flag() {
	if (!flag_var) return;
	flag_var = false;
	for (unsigned int i=0;i<children_var.size();i++) children_var[i]->clear_flag();
}

void Concept::recalculate_intent()  {
    /*
    set< type_of_patterns > cleaning = clean_intent();
    int i =0;
    for (auto it = intent().pattern.begin();it!=intent().pattern.end();++it) {
        
		if ((cleaning.find(*it) != cleaning.end())) {
			intent_var.bicluster[i] = false;
        }
        i++;
	}*/
}

/*void Concept::add_to_extent(int obj)
{
	if (!flag_var) {
        extent_var.push_front(obj);
        set_flag();
        recalculate_intent();
        std::forward_list<int> toerase;
        Children toadd;
        std::set<size_t> mine;
        for (unsigned int i = 0; i < children_var.size(); i++) {
            mine.insert(children_var[i]->intent_var.h);
            children_var[i]->add_to_extent(obj);
            if ((children_var[i]->intent_var.bicluster.size() != 0) &&(children_var[i]->intent_var.bicluster.count() == 0)) {
                toerase.push_front(i);
                for (auto it=children_var[i]->children_var.begin();it!=children_var[i]->children_var.end();++it)
                    toadd.push_back(*it);
                    //children_var.push_back(*it);
            }
        }
        for (auto it=toerase.begin();it!=toerase.end();++it)
            children_var.erase(children_var.begin()+*it);
        
        for (auto it=toadd.begin();it!=toadd.end();++it) {
            bool add = true;
            for (unsigned int i = 0; i < children_var.size(); i++) {
                if (children_var[i]->intent() <= (*it)->intent())
                    add = false;
            }
            if (add)
                children_var.push_back(*it);
        }
    }
} */

void Concept::add_to_extent(int obj)
{
	if (!flag_var) {
        extent_var.push_back(obj);
        set_flag();
        for (unsigned int i = 0; i < children_var.size(); i++) {
            children_var[i]->add_to_extent(obj);
        }
    }
}


void Concept::clean_lattice()
{       //bottom_concept
	set_flag();
    for (unsigned int i=0;i<children_var.size();i++)
        children_var[i]->clean_chain();
	clear_flag();
}

void Concept::clean_chain() {
    
    if (flag_var) return;
        set_flag();
    for (auto it = children_var.begin();it!=children_var.end();++it) {
        intent_var->clean((*it)->intent_var);
    }
    for (auto it = children_var.begin();it!=children_var.end();++it) {
        (*it)->clean_chain();
    }
    /*
    std::forward_list<int> toerase;
    Children toadd;
    std::set<size_t> mine;
    
	for (unsigned int i=0;i<children_var.size();i++) {
        children_var[i]->clean_chain();
        
        if ((children_var[i]->intent_var.bicluster.size() != 0) &&(children_var[i]->intent_var.bicluster.count() == 0)) {
            toerase.push_front(i);
            for (auto it=children_var[i]->children_var.begin();it!=children_var[i]->children_var.end();++it)
                toadd.push_back(*it);
            //children_var.push_back(*it);
        }
    }
    for (auto it=toerase.begin();it!=toerase.end();++it)
        children_var.erase(children_var.begin()+*it);
    
    for (auto it=toadd.begin();it!=toadd.end();++it) {
        bool add = true;
        for (unsigned int i = 0; i < children_var.size(); i++) {
            if ((*it)->intent() <= children_var[i]->intent())
                add = false;
        }
        if (add)
            children_var.push_back(*it);
    }

    
    recalculate_intent();
     */
}

void Concept::print_chain(std::ostream & file, int level)
{
	if (flag_var) return;
    file<<to_str(level);
    level += 1;

	set_flag();
	for (unsigned int i=0;i<children_var.size();i++)
        children_var[i]->print_chain(file,level);
}

string Concept::extent_to_csv() const
{
    if (extent_var.begin() == extent_var.end())
        return "empty";
    ostringstream str;
    for (auto it = extent_var.begin();it!=extent_var.end();++it)
    {
        str << *it;
        str << ",";
    }
    return str.str();
}

string Concept::print_children() const {
    ostringstream str;
    for (unsigned int i=0;i<children_var.size();i++) {
        str << children_var[i]->intent_var->hash() << "|";
    }
    return str.str();
}

void Concept::calc_diff(Extent ext) {
    std::vector<int> interit;
    std::set_difference(extent_var.begin(),extent_var.end(), ext.begin(),ext.end(), std::back_inserter(interit));
    if (interit.size() < diff) {
        diff = interit.size();
    }
}

void Concept::initialize_stability()
{
    if (flag_var)
        return;
	set_flag();
    sdata.stability=0;
    sdata.subsets=pow(2,extent_var.size());
    sdata.count = 0;
    for (unsigned int i=0;i<children_var.size();i++) {
        children_var[i]->initialize_stability();
        children_var[i]->sdata.count++;
    }
}

void Concept::propagate_subsets(int subsets)
{
    if (flag_var)
        return;
	set_flag();
    sdata.subsets-=subsets;
    for (unsigned int i=0;i<children_var.size();i++) {
        children_var[i]->propagate_subsets(subsets);
    }
}

bool Concept::calculate_stability() {
    if (flag_var)
        return true;
    set_flag();
    if ((sdata.count == 0) &&  (children_var.size() == 0))
        return false;
    else if (sdata.count == 0) {
        sdata.count = -1;
        sdata.stability = sdata.subsets/ pow(2,extent_var.size());
        //cout << sdata.stability << ":" << sdata.subsets << "/" << pow(2,extent_var.size()) << endl;
        for (unsigned int i=0;i<children_var.size();i++) {
            //cout << intent_var.hash() << "|"<<extent_to_csv() << ": " << sdata.subsets <<" - " <<children_var[i]->intent_var.hash()<< "|" << children_var[i]->extent_to_csv() << ": " << children_var[i]->sdata.subsets<<endl;
            children_var[i]->propagate_subsets(sdata.subsets);
            children_var[i]->sdata.count--;
        }
        clear_flag();
        set_flag();
        return true;
    }
    else if (sdata.count == -1) {
        bool r = true;
        for (unsigned int i=0;i<children_var.size();i++)
            r &= children_var[i]->calculate_stability();
        return r;
    }
    else
        return true;
}

void Concept::calculate_differences()
{       //bottom_concept
	set_flag();
    for (unsigned int i=0;i<children_var.size();i++) {
        children_var[i]->calc_chain();
        children_var[i]->calc_diff(extent_var);
    }
	clear_flag();
}

void Concept::calc_chain() {
    if (!flag_var) {
        set_flag();
        for (unsigned int i=0;i<children_var.size();i++)
        {
            children_var[i]->calc_chain();
            children_var[i]->calc_diff(extent_var);
        }
    }
}



string Concept::to_str(int level) const
{
    ostringstream str;
    str << "<";
    str << intent_var->hash();
    str << ">@sep@<";
    //str << clean_intent();
    str << intent_var->to_csv();
    //str << intent_var.to_csv(clean_intent());
    str << ">@sep@<";
    str << extent_to_csv();
    str << ">@sep@<";
    str << print_children();
    //str << ">@sep@<" << diff << ">@sep@"<< intent_var.opening() <<endl;
    str << ">" << endl;
    return str.str();
}




