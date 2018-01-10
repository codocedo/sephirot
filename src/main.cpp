#include "Config.h"
#include "IIntent.h"
#include "Concept.h"
#include "SetIntent.h"
//#include "HPIntent.h"
//#include "HPConcept.h"
//#include "PatternIntent.h"
//#include "PatternConcept.h"
#include "ConceptLattice.h"
#include "BiclusterLattice.h"
//#include "TBPattern.h"
//#include "LatticeIntent.h"
//#include "IntervalConcept.h"
//#include "IntervalPattern.h"
#include "StarIntent.h"
#include "IntentFactory.h"

#include <fstream>
#include <cstdlib>
#include <cstring>
#include <algorithm>    // std::set_intersection, std::sort
#include <iterator>
#include <vector>
#include <stdio.h>
#include <string.h>
#define SI_SUPPORT_IOSTREAMS
#include <SimpleIni.h>
#include <unistd.h>
#include <chrono>




using std::ifstream;
using std::cout;
using std::endl;
using std::ofstream;
using std::set_intersection;

std::vector< pair<Tvalue, Tvalue> > tolerance_blocks;

Tvalue e;
Tvalue e1;
bool debug;
bool optimize;
int bins=1;


/**
 * Experimental implementation of an Ad-Hoc concept lattice that directly
 * fetches the biclusters by applying a deep clean of partitions in the lattice.
 * Currently, only supported for partition pattern structures.
 */
BiclusterLattice mineBiclusters(std::vector< std::vector<Tvalue> > context, const Config * cfg) {
    IntentFactory intfac = IntentFactory();
    BiclusterLattice cl = BiclusterLattice(0, intfac.CreateIntent(context[0], cfg, 0));
    //cl.set_type_of_partition(type_of_partition);
    //std::ostream out(cout.rdbuf());
    //cl.print_lattice(out);
    cout << "________________________________" << endl;
	for(int obj=1; obj<context.size();obj++)
	{
        cout << "\rO: " << obj ;
        //cout << "********************************"<<endl << "O: " << obj << " - " ;
        cout.flush();
        //SetIntent intent = SetIntent(table[obj]);
        IIntent * pintent = intfac.CreateIntent(context[obj], cfg, obj);
        cl.add_object(obj,pintent);
	}
    cl.calculate_things();
    cout << endl;
    
    if (cfg->stability) {
        cout << "----> Calculating stability" << endl;
        cl.calculate_stability();
    }
    
    // THIS IS WHAT CLEANS THE LATTICE OF NON MAXIMAL BICLUSTERS
    cl.clean_lattice();
    
    //ofstream output_file(cfg->txt_output());
	//cl.print_lattice(output_file);
    //output_file.close();
    //cout << "Output written to: " << cfg->txt_output() << endl;
    cl.save_to_json(cfg);
    cout << "Output written to: " << cfg->json_output() << endl;
    
    return cl;
}

/**
 * Execute FCA using a given configuration stored in cfg.
 */
ConceptLattice execute(std::vector< std::vector<Tvalue> > context, const Config * cfg) {
    IntentFactory intfac = IntentFactory();
    ConceptLattice cl = ConceptLattice(0, intfac.CreateIntent(context[0], cfg, 0));
	for(int obj=1; obj<context.size();obj++)
	{
        cout << "\rO: " << obj ;
        cout.flush();
        IIntent * pintent = intfac.CreateIntent(context[obj], cfg, obj);
        cl.add_object(obj,pintent);
	}
    cl.calculate_things();
    cout << endl;
    
    if (cfg->stability) {
        cout << "----> Calculating stability" << endl;
        cl.calculate_stability();
    }
    
    ofstream output_file(cfg->txt_output());
	cl.print_lattice(output_file);
    output_file.close();
    cout << "Output written to: " << cfg->txt_output() << endl;
    cl.save_to_json(cfg);
    cout << "Output written to: " << cfg->json_output() << endl;
    
    return cl;
}

void help() {
    cout << "Sephirot - AddIntent for Pattern structures\nUsage:\n\n";
    cout << "-i [PATH]\t Path to ini file." << endl;
    cout << "INI FILE EXAMPLE:" << endl;
    cout << "" << endl;
}


int main(int argc, char* argv[])
{
    std::chrono::high_resolution_clock::time_point t1 = std::chrono::high_resolution_clock::now();
    std::cout << "________________________________\n\n";
    std::cout << "Executing Sephirot AddIntent ---\n";
    std::cout << "--------------------------------\n\n";
    istringstream s;
    opterr = 0;
    char * initfilepath = NULL;
    bool marche = false;
    
    debug = false;
    int c;
    
    while ((c = getopt (argc, argv, "i:")) != -1)
        switch (c)
    {
        case 'i': {
            initfilepath = optarg;
            marche = true;
            break;
        }
        case '?': {
            if (optopt == 'i')
                fprintf (stderr, "Option -%c requires the filepath to the init file.\n", optopt);
            else if (isprint (optopt))
                fprintf (stderr, "Unknown option `-%c'.\n", optopt);
            else
                fprintf (stderr,
                         "Unknown option character `\\x%x'.\n",
                         optopt);
            return 1;
        }
        default: {
            fprintf (stderr, "Unknown option `-%c'.\n", optopt);
            help();
            std::exit(0);
        }
    }
    
    if (!(marche)) {
        cout << "ERROR: Ini file not provided (use -i [ini file] to provide an ini file)" << endl << endl;
        exit(0);
    }
        
    
    if (!(file_exists(initfilepath))) {
        cout << "ERROR: The ini file provided does not exist" << endl;
        exit(0);
    }
    
    
    const Config * cfg = new Config(initfilepath);
    cfg->print();
    // READING THE CONTEXT
    //if (cfg->invert_context) table = invert_context(table);
    //else if (cfg->invert_matrix) table = invert_matrix(table);

    std::chrono::high_resolution_clock::time_point t3 = std::chrono::high_resolution_clock::now();
    execute(cfg->context, cfg);

    // WRITING REPORT OF EXECUTION TIME
    std::chrono::high_resolution_clock::time_point t2 = std::chrono::high_resolution_clock::now();
    ofstream reportFile;
    reportFile.open(cfg->outfilepath+".report.txt");
    reportFile << "Execution Report" << endl;
    reportFile << "Exec.Time: " << (double)((std::chrono::duration_cast<std::chrono::microseconds>(t2-t1)).count())/1000000.0 << " seconds" <<endl;
    reportFile << "FCA Time: " << (double)((std::chrono::duration_cast<std::chrono::microseconds>(t2-t3)).count())/1000000.0 << " seconds" <<endl;
    reportFile.close();
    
    
    //mineBiclusters(cfg->context,cfg);
    return 0;
}
