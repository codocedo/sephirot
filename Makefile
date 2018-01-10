CC=g++
INC=-I./rapidjson/include/  -I./simpleini/ -I/opt/local/include/
SRC=src/
OBJ=obj/
BIN=bin/
CFLAGS=-Wno-deprecated -std=gnu++0x -O3 
FILES=Concept.cpp Intent.cpp SetIntent.cpp ConceptLattice.cpp 
OLD_FILES_PS=Concept.cpp PatternConcept.cpp Intent.cpp SetIntent.cpp PatternIntent.cpp ConceptLattice.cpp HPIntent.cpp HPConcept.cpp TBPattern.cpp LatticeIntent.cpp IntervalConcept.cpp IntervalPattern.cpp StarIntent.cpp
FILES_PS=Utils.cpp Config.cpp Concept.cpp TBIntent.cpp SetIntent.cpp IntervalPattern.cpp ConceptLattice.cpp StarIntent.cpp IntentFactory.cpp PartitionPattern.cpp BiclusterLattice.cpp BiclusterHolder.cpp
SEPHIROTMAIN_PS = $(OBJ)main.o
SEPHIROTMAIN = $(OBJ)main2.o
SOURCES=$(addprefix $(SRC),$(FILES))
SOURCES_PS=$(addprefix $(SRC),$(FILES_PS))
OBJECTS=$(addprefix $(OBJ),$(FILES:.cpp=.o))
OBJECTS_PS=$(addprefix $(OBJ),$(FILES_PS:.cpp=.o))

EXECUTABLE=$(BIN)sephirot2
EXECUTABLE_PS=$(BIN)sephirot


all: $(EXECUTABLE_PS)

$(EXECUTABLE_PS): $(OBJECTS_PS) $(SEPHIROTMAIN_PS)
	$(CC) $(CFLAGS) $(INC) $(OBJECTS_PS) $(SEPHIROTMAIN_PS) -o $(EXECUTABLE_PS)

s1: $(OBJECTS) $(SEPHIROTMAIN)
	$(CC) $(CFLAGS) $(INC) $(OBJECTS) $(SEPHIROTMAIN) -o $(EXECUTABLE)

#$(EXECUTABLE): $(OBJECTS)
#	$(CC) $(SRC)$(OBJECTS) $(INC) -o $@

$(OBJ)%.o: $(SRC)%.cpp
	$(CC) $(CFLAGS) -c $(INC) $< -o $@

clean:
	rm  $(OBJ)*.o $(EXECUTABLE_PS)
run: all
	./$(EXECUTABLE_PS) -f datasets/toy.txt

