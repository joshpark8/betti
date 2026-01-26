-- imports
needsPackage "RandomIdeals"
needsPackage "BoijSoederberg"
needsPackage "JSON"

-- number of variables
varCount = 4

-- number of generators
genCount = 3

-- generate uniquely identifiable file in format "ideals[# of variables],[# of generators]-[index].json"
fileIndex = 1
filepath = "generated/ideals"
fileID = concatenate(toString varCount, ",", toString genCount)
while fileExists concatenate(filepath, fileID, "-", toString fileIndex, ".json") do (
    fileIndex += 1
)

f = concatenate(filepath, fileID, "-", toString fileIndex, ".json") << ""

-- define ring
R = (ZZ/101)[x_1..x_(varCount)]
-- R = QQ[x,y,z]

-- define mutable hash table to pair (grobner bases of) ideals with respective betti tables
mhash = new MutableHashTable

-- define list of generator grades

L = new MutableList
for i from 1 to genCount do (
    L#(i-1) = random(50,100)
)

-- generate ideals and match to betti tables
elapsedTime for i from 1 to 1000 do (
    I = randomMonomialIdeal({random(50,100),random(50,100),random(50,100)}, R);
    Istr = toString gens gb I;
    mhash#Istr = toString matrix betti I;
)

finalhash = new HashTable from mhash;

f << toJSON finalhash

f << close
