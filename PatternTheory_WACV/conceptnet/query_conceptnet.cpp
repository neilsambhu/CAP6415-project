/*-------------------------------------------------------------------------------------------------------------/
/ Author: maups                                                                                                /
/ Date: 03/21/2020                                                                                             /
/ TODO: * speed up queries by saving relations per concept                                                     /
/       * save memory by converting concepts/relations to ids                                                  /
/------------------------------------------------------------------------------------------------------------ */
#include <iostream>
#include <fstream>
#include <map>
#include <set>
#include <vector>
#include <algorithm>

using namespace std;

// Start concept, relation, end concept, weight
#define edge tuple<string,string,string,double>

// ConceptNet graph
class ConceptNet {
	private:
		// vector of weights for edges (edges may have duplicates with different weights on ConceptNet)
		map<tuple<string,string,string>, vector<double>> edge_weights;
		// maps pair<concept,relation> to conceps
		map<pair<string,string>,set<string>> inbonds, outbonds;
		// set of relation types
		set<string> relations;

	public:
		ConceptNet(string);

		vector<edge> query_concept(string, bool);
		vector<edge> query_edge(string, string);
};

// Loads a processed CSV file (see get_english_edges.cpp)
ConceptNet::ConceptNet(string filename) {
	// Open file
	ifstream ifp(filename, ifstream::in);

	// Read all lines
	string s;
	while(getline(ifp, s)) {
		// Four columns separated by tab space
		// 1st item -> relation name
		// 2nd item -> start concept name
		// 3rd item -> end concept name
		// 4th item -> edge weight

		// Get relation name
		size_t pos1 = 0, pos2 = s.find('\t', pos1);
		string rel = s.substr(pos1, pos2-pos1);

		// Get start concept name
		pos1 = pos2+1;
		pos2 = s.find('\t', pos1);
		string start = s.substr(pos1, pos2-pos1);

		// Get start concept name
		pos1 = pos2+1;
		pos2 = s.find('\t', pos1);
		string end = s.substr(pos1, pos2-pos1);

		// Get edge weight
		pos1 = pos2+1;
		double weight = stod(s.substr(pos1));

		// Insert inbonds & outbonds
		outbonds[make_pair(start,rel)].insert(end);
		inbonds[make_pair(end,rel)].insert(start);

		// Save weight
		edge_weights[make_tuple(start,rel,end)].push_back(weight);

		// Save relation type
		relations.insert(rel);
	}

	ifp.close();
}

// Look for other concepts with an edge to the query one, set outbonds_only to true if inbonds are not necessary
vector<edge> ConceptNet::query_concept(string concept, bool outbonds_only = false) {
	vector<edge> r;
	for(string rel : relations) {
		// Look for outbonds
		if(outbonds.count(make_pair(concept,rel)) > 0)
			for(string end : outbonds[make_pair(concept,rel)])
				for(double w : edge_weights[make_tuple(concept,rel,end)])
					r.push_back(make_tuple(concept,rel,end,w));
		if(!outbonds_only) {
			// Look for inbonds
			if(inbonds.count(make_pair(concept,rel)) > 0)
				for(string start : inbonds[make_pair(concept,rel)]) {
					// Do not get 'self'-edges twice
					if(start == concept)
						continue;
					for(double w : edge_weights[make_tuple(start,rel,concept)])
						r.push_back(make_tuple(start,rel,concept,w));
				}
		}
	}
	return r;
}

// Look for edges between concept1 and concept2
vector<edge> ConceptNet::query_edge(string concept1, string concept2) {
	vector<edge> r;
	for(string rel : relations) {
		// 1 -> 2
		if(edge_weights.count(make_tuple(concept1,rel,concept2)) > 0)
			for(double w : edge_weights[make_tuple(concept1,rel,concept2)])
				r.push_back(make_tuple(concept1,rel,concept2,w));
		// 2 -> 1
		if(edge_weights.count(make_tuple(concept2,rel,concept1)) > 0)
			for(double w : edge_weights[make_tuple(concept2,rel,concept1)])
				r.push_back(make_tuple(concept2,rel,concept1,w));
	}
	return r;
}

// Pandora box
int main(int argc, char **argv) {
	// Usage instructions
	if(argc != 2) {
		cerr << "Usage: " << argv[0] << " [input_edges.csv]" << endl;
		return 1;
	}

	// Load ConceptNet edges
	ConceptNet cnet(argv[1]);

	// Query edges from one concept
	vector<edge> edges = cnet.query_concept("banana");
	// Sort edges in descending order by weight
	std::sort(edges.rbegin(), edges.rend(), [](edge const& a, edge const& b){ return get<3>(a) < get<3>(b); });

	// Print recovered edges
	cout << "---------------------------------------------" << endl;
	cout << "Query concept: " << "banana" << endl;
	cout << "Number of edges: " << edges.size() << endl;
	cout << "---------------------------------------------" << endl << endl;
	for(auto e : edges)
		cout << get<0>(e) << " -> " << get<1>(e) << " -> " << get<2>(e) << " (" << get<3>(e) << ")" << endl;
	cout << endl;

	// Query edges between two concepts
	edges = cnet.query_edge("banana", "fruit");

	// Print recovered edges
	cout << "---------------------------------------------" << endl;
	cout << "Query edge: " << "banana" << " <-> " << "fruit" << endl;
	cout << "Number of edges: " << edges.size() << endl;
	cout << "---------------------------------------------" << endl << endl;
	for(auto e : edges)
		cout << get<0>(e) << " -> " << get<1>(e) << " -> " << get<2>(e) << " (" << get<3>(e) << ")" << endl;
	cout << endl;
}

