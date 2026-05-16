-- imports
needsPackage "RandomIdeals"
needsPackage "BoijSoederberg"
needsPackage "JSON"

varCount = 3 -- number of variables
genCount = 3 -- number of generators
idealCount = 100000 -- number of ideals to generate

degMin = 1 -- lower bound for random degrees
degMax = 50 -- upper bound for random degrees

-- generate uniquely identifiable file in format "ideals[# of variables],[# of generators]-[index].json"
fileIndex = 1
filepath = "generated/binomials,"
fileID = concatenate(toString varCount, "v,", toString genCount, "g,", toString idealCount, "i")
while fileExists concatenate(filepath, fileID, "-", toString fileIndex, ".json") do (
    fileIndex += 1
)

f = concatenate(filepath, fileID, "-", toString fileIndex, ".json") << ""

-- define ring
R = (ZZ/101)[x_1..x_(varCount)]

-- define mutable hash table to pair (grobner bases of) ideals with respective betti tables
mhash = new MutableHashTable

-- generate ideals and match to betti tables
startTime = currentTime();
for i from 1 to idealCount do (
    I = randomPureBinomialIdeal({random(degMin,degMax),random(degMin,degMax),random(degMin,degMax)}, R);
    Istr = toString gens I;
    mhash#Istr = toString matrix betti I;

    elapsed = currentTime() - startTime;
    -- stdio << concatenate(ascii 13, fileID, "-", toString fileIndex, ": completed ", toString i, " ideals -- elapsed: ", toString elapsed, "s") << flush;
)

finalhash = new HashTable from mhash;

f << toJSON finalhash

f << close
