#include <iostream>
#include <fstream>

using namespace std;


int main(int argc, char **argv) {
	// Usage instructions
	if(argc != 3) {
		cerr << "Usage: " << argv[0] << " [conceptnet-assertions-5.X.X.csv] [output_edges.csv]" << endl;
		return 1;
	}

	// Open files
	ifstream ifp(argv[1], ifstream::in);
	ofstream ofp(argv[2], ofstream::out);

	// Read all lines
	string s;
	while(getline(ifp, s)) {
		// Items separated by tab space
		// 2nd item -> relation
		// 3rd item -> start concept
		// 4th item -> end concept
		// 5th item -> json with 'weight' field

		// Get relation
		size_t pos1 = s.find('\t')+1, pos2 = s.find('\t', pos1);
		string r = s.substr(pos1, pos2-pos1);

		// Get name of the relation
		r = r.substr(3, r.find('/',3)-3);

		// Get start concept
		pos1 = pos2+1;
		pos2 = s.find('\t', pos1);
		string a = s.substr(pos1, pos2-pos1);

		// Discard edge if concept is not in English
		if(a.substr(0,6) != "/c/en/")
			continue;

		// Get name of the concept
		a = a.substr(6, a.find('/',6)-6);

		// Get end concept
		pos1 = pos2+1;
		pos2 = s.find('\t', pos1);
		string b = s.substr(pos1, pos2-pos1);

		// Discard edge if concept is not in English
		if(b.substr(0,6) != "/c/en/")
			continue;

		// Get name of the concept
		b = b.substr(6, b.find('/',6)-6);

		// Get edge weight
		double w = stod(s.substr(s.find("\"weight\":", pos2)+9));

		// Save edge
		ofp << r << "\t" << a << "\t" << b << "\t" << w << endl;
	}

	ifp.close();
	ofp.close();
}

