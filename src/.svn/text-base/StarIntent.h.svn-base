//
//  StarIntent.h
//  Sephirot
//
//  Created by Kyori on 08/07/14.
//  Copyright (c) 2014 Kyori. All rights reserved.
//

#ifndef __Sephirot__StarIntent__
#define __Sephirot__StarIntent__

#include <iostream>
#include "SetIntent.h"
#include "IntentFactory.h"
//#include "PatternConcept.h"

//typedef std::pair<SetIntent,PatternIntent> THet;

typedef std::vector<IIntent * > StarPattern;
class StarIntent : public IIntent {
public:
    StarPattern * pattern;
    StarIntent() { };
    ~StarIntent();
    void * desc() const { return pattern; }
    StarIntent(std::vector<Tvalue> attrs, const Config * cfg, unsigned int obj);
    StarIntent(StarPattern * pattern);
    bool operator== (const IIntent * other) const;
    bool operator<= (const IIntent * other) const;
    StarIntent * operator& (const IIntent * other) const;
    size_t hash() const;
    std::string to_csv() const;
    void join(const IIntent * other) const;
    
    void serialize(Jetson & writer, const Config * cfg) const;
    StarIntent * clone() const;
    void clean(const IIntent * other) const { };
};
/*
class StarConcept : public PatternConcept {
private:
    StarIntent intent_var;
public:
    typedef std::vector<StarConcept * > Children;
    Children children_var;
    // ACCESORS
    StarIntent intent() const { return intent_var; }
    Children children() const { return children_var; }
    StarConcept (const Extent & ext, const StarIntent & inten) : PatternConcept(ext), intent_var(inten) { };
    void minimize_intent(const StarIntent * intent);
    std::string to_str(int level) const;
    void print_chain(std::ostream & file, int level);
    template <typename Writer>
    void serialize_chain(Writer& writer, const config & cfg) {
        if (!flag_var) {
            set_flag();
            Serialize(writer,cfg);
            for (unsigned int i=0;i<children_var.size();i++)
            children_var[i]->serialize_chain(writer, cfg);
        }
    }
    template <typename Writer>
    void Serialize(Writer& writer, const config & cfg) const {
        cout << "Calling starconcept" << endl;
        writer.StartObject();
        writer.String("id",2);
        writer.Int64(intent_var.hash());
        
		writer.String("Extent",6);
        writer.StartArray();
        unsigned int support = 0;
        for (auto it=extent_var.begin(); it!=extent_var.end();++it) {
            writer.Uint(*it);
            support++;
        }
        writer.EndArray();
        writer.String("Support",7);
        writer.Uint(support);
        writer.String("Intent",6);
        intent().Serialize(writer, cfg);
        
        writer.String("Parents",7);
        writer.StartArray();
        for (auto it=children().begin(); it!=children().end();++it)
        writer.Int64((*it)->intent().hash());
        writer.EndArray();
        if (cfg.stability) {
            writer.String("Stability",9);
            writer.Double(sdata.stability);
            writer.String("Count",5);
            writer.Int64(sdata.count);
        }
        writer.String("Type",4);
        if (children_var.size() == 0)
        writer.String("T",1);
        else if (extent_var.size() == 0)
        writer.String("B",1);
        else if (is_object_concept())
        writer.String("O",1);
        else
        writer.String("N",1);
        writer.EndObject();
    }
    
};

inline void StarConcept::print_chain(std::ostream & file, int level)
{
	if (flag_var) return;
	file<<to_str(level);
    level += 1;
    
	set_flag();
	for (unsigned int i=0;i<children_var.size();i++)
    children_var[i]->print_chain(file,level);
}

inline std::string StarConcept::to_str(int level) const
{
    ostringstream str;
    str << "<";
    str << intent_var.hash();
    str << ">@sep@<";
    str << intent_var.to_csv();
    cout << intent_var.to_csv();
    //str << clean_intent();
    //str << intent_var.to_csv(clean_intent());
    str << ">@sep@<";
    str << extent_to_csv();
    str << ">@sep@<";
    str << print_children();
    //str << ">@sep@<" << diff << ">@sep@"<< intent_var.opening() <<endl;
    str << ">" << endl;
    return str.str();
}

inline void StarConcept::minimize_intent(const StarIntent * other)
{
    for (unsigned int i=0;i<intent_var.pattern.size();i++) {
        intent_var.pattern[i]->attributes.insert(other->pattern[i]->attributes.begin(),other->pattern[i]->attributes.end());
    }
}
*/
#endif /* defined(__HFCA__StarIntent__) */
