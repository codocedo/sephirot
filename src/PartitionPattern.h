//
//  PartitionPattern.h
//  Biclusterer
//
//  Created by Kyori on 01/09/14.
//  Copyright (c) 2014 INRIA. All rights reserved.
//

#ifndef __Biclusterer__PartitionPattern__
#define __Biclusterer__PartitionPattern__

#define EMPTY   0
#define SAFE    std::numeric_limits<unsigned int>::max()

#include <iostream>

#include "IIntent.h"
#include "Config.h"
#include <boost/dynamic_bitset.hpp>



/**
 * A partition of a set G is a set of subsets of G which we call components. All components have an empty intersection among each other and the union of all of them regenerates G.
 * ===========
 * This implementation of partitions uses a signature partitions. This is, instead of using a set of sets, we use a hash signature which uniquely identifies the partitions. For example, let G = {a,b,c,d,e}, a partition can be ac|d|be. Each component is assigned a unique number and a fixed order is stablished in G, i.e. a<b<c<d<e. Then, partition ac|d|be can be identified as 12132. This is, the first position representing the object a is in component 1. The second position representing object b is in component 2. The third position representing object c is in component 1, etc.
 * ============
 * This implementation also includes strip partitions, i.e. if a component contains one object, then it is stripped out of the partition. In the signature, this is characterized by a 0. For example, ac|d|bd which was previously identified by the signature 12132, as a stripped partition it is identified by 12102. A partition ab|c|d|e is identified as 11000. This, doesn't mean that c,d and e belong to the same component, but that they are in one-object components.
 * ============
 * This implementation also includes a ''minimal number of objects per component'' restriction. This works similarly to the strip partitions (which can be considered as having a minimal number of 2 objects per component). With a minimal number of 3 objects, the partition ad|bce can be identified as 01101.
 **/
class PartitionPattern : public IIntent
{
public:
    //typedef std::set<Tvalue> TComponent;
    //typedef std::vector< Tentity > TSignature;
    typedef Tentity * TSignature;
    typedef std::vector<std::vector<Tentity> > TParti;
    Tentity min_rows;
    
    
    struct Description{
        mutable TSignature pattern;
        mutable unsigned int min_rows;
        mutable boost::dynamic_bitset<> strip;
        mutable size_t size;
        Description(unsigned int mr, size_t size) : min_rows(mr), size(size) {
            //pattern = new TSignature();
            //pattern = std::vector<Tentity>(size,EMPTY);
            //cout << "SIZE: " << size << " | " << endl;
            pattern = new Tentity[size];
            for (int i=0;i<size;i++)
                pattern[i] = EMPTY;
        };
        ~Description() {
            delete pattern;
            pattern = NULL;
        }
        
        bool operator== (const Description * other) const;
        
        string to_csv() const;

    };
    mutable Description * d;
    
    PartitionPattern() {d = new Description(2,0); };
    PartitionPattern(Description * d) : d(d) { } ;
    ~PartitionPattern();

    
	//bool infimum_of_these_components_satisfies_e(int index1, int index2);
    
	PartitionPattern(std::vector<Tvalue> & attrs, const Config * cfg, unsigned int obj);
    
    PartitionPattern(const PartitionPattern& other);
	//PatternIntent(std::vector<Tvalue> attrs, char partition_type);
    
    /* INHERITED METHODS */
    void * desc() const { return d; }
    PartitionPattern * get_less_general_intent() const;
    bool operator== (const IIntent * other) const;
    bool operator<= (const IIntent * other) const;
    PartitionPattern * operator& (const IIntent * other) const;
    void join(const IIntent * other) const;
    string to_csv() const;
    size_t hash() const;
    PartitionPattern * clone() const;
    bool empty() const;
    void serialize(Jetson & writer, const Config * cfg) const;
    void clean(const IIntent * other) const;
    TParti signature2partition() const;
};


#endif /* defined(__Biclusterer__PartitionPattern__) */
