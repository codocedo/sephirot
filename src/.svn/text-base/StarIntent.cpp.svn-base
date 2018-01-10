//
//  StarIntent.cpp
//  Sephirot
//
//  Created by Kyori on 08/07/14.
//  Copyright (c) 2014 Kyori. All rights reserved.
//
#include "Utils.h"
#include "StarIntent.h"



StarIntent * StarIntent::clone() const {
    return new StarIntent(this->pattern);
}

StarIntent::~StarIntent() {
    delete pattern;
    pattern = NULL;
}

StarIntent::StarIntent(std::vector<Tvalue> attrs, const Config * cfg, unsigned int obj) {
    int dims = 1;
    for (auto  it =attrs.begin();it!=attrs.end();++it)
        if (*it == -1)
            dims++;
    if (dims != cfg->htypes.size()) {
        cout << "ERROR: Line "<< obj+1 << " contain " << attrs.size() <<  " dimension while it should contain " << cfg->htypes.size() << endl;
        exit(0);
    }
    pattern = new StarPattern();
    IntentFactory intfac = IntentFactory();
    bool goon = true;
    auto begin = attrs.begin();
    int counter = 0;
    while (goon) {
        auto cut = std::find(begin, attrs.end(), -1);
        if (cut == attrs.end())
            goon = false;
        std::vector<Tvalue> v1(begin,cut);
        //SetIntent * si = new SetIntent(v1, cfg, obj);
        //for (auto it=cfg->htypes.begin();it!=cfg->htypes.end();++it)
          //  cout << *it << "," ;
        
        //cout <<endl<< &v1 << " | " << cfg->htypes[counter] << ", i=" <<counter << endl;
        IIntent * si = intfac.CreateIntentSpec(v1, cfg, obj,cfg->htypes[counter++]);
        pattern->push_back(si);
        begin = ++cut;
    }
    //cout << "FINISHED" << endl;
    //cout << to_csv()<< endl;
    //pattern = THet(SetIntent(v1,cfg),PatternIntent(v2,cfg));
}

StarIntent::StarIntent(StarPattern * opattern){
    pattern = new StarPattern();
    for (auto it = opattern->begin();it!=opattern->end();++it)
        pattern->push_back((*it)->clone());
};

void StarIntent::join(const IIntent * other) const {
    StarPattern * op = static_cast<StarPattern *>(other->desc());
    for (unsigned int i =0;i<pattern->size();i++) {
        pattern->at(i)->join(op->at(i));
    }
}

bool StarIntent::operator== (const IIntent * other) const
{
    StarPattern * op = static_cast<StarPattern *>(other->desc());
    for (int i =0; i<pattern->size(); i++) {
        if (!(*pattern->at(i) == op->at(i)))
            return false;
    }
    return true;
}

bool StarIntent::operator<= (const IIntent * other) const
{
    StarPattern * op = static_cast<StarPattern *>(other->desc());
    for (unsigned int i =0;i<pattern->size();i++) {
        if (!(*pattern->at(i) <= op->at(i))) {
            return false;
        }
    }
    return true;
}

StarIntent * StarIntent::operator& (const IIntent * other) const {
    StarPattern * op = static_cast<StarPattern *>(other->desc());
    StarPattern * v1 = new StarPattern();
    for (unsigned int i =0;i<pattern->size();i++) {
        v1->push_back(*pattern->at(i) & op->at(i));
    }
    StarIntent * r = new StarIntent(v1);
    return r;
}

void StarIntent::serialize(Jetson & writer, const Config *cfg) const{
    //writer->StartObject();
    //writer->String("Intent",3);
    writer.array();
    for (auto it=pattern->begin();it!=pattern->end();++it)
        (*it)->serialize(writer,cfg);
    writer.close_array();
    //writer->EndObject();
}

size_t StarIntent::hash() const{
    boost::hash<std::string> string_hash;
    return string_hash(to_csv());
}

std::string StarIntent::to_csv() const {
    ostringstream s;
    for (auto it = pattern->begin();it!=pattern->end();++it) {
        s << (*it)->to_csv() << " - ";
    }
    return s.str();
}