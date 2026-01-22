-- imports
needsPackage "RandomIdeals"
needsPackage "BoijSoederberg"
needsPackage "JSON"

-- file open
f = "generated/ideals.json" << ""

-- define ring
R = ZZ[x,y]

x = new MutableHashTable
-- generate ideals and match to betti tables
for i from 1 to 100 do (
    I = randomMonomialIdeal({random(5,10), random(5,10), random(5,10)},R);

    Istr = toString I;
    Ibetti = matrix betti I;
    x#Istr = toString Ibetti;
)

hashx = new HashTable from x

f << toJSON hashx

f << close