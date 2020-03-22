import json
import sys

# Check comments on get_english_edges.cpp

if len(sys.argv) != 3:
	print("Usage: " + sys.argv[0] + " [conceptnet-assertions-5.X.X.csv] [output_edges.csv]", file=sys.stderr)
	sys.exit(1)

with open(sys.argv[1]) as ifp:
	ofp = open(sys.argv[2], "w")

	line = ifp.readline()
	while line:
		elem = line.split('\t')
		meta = json.loads(elem[4])
		if elem[2].startswith('/c/en/') and elem[3].startswith('/c/en/'):
			ofp.write(elem[1].split('/')[2] + '\t' + elem[2].split('/')[3] + '\t' + elem[3].split('/')[3] + '\t' + str(meta['weight']) + '\n')
		line = ifp.readline()

	ofp.close()

