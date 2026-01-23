-- imports
needsPackage "RandomIdeals"
needsPackage "BoijSoederberg"
needsPackage "JSON"

-- file open
f = "generated/ideals.json" << ""

-- define ring
R = ZZ[x,y]

-- define mutable hash table to pair (grobner bases of) ideals with respective betti tables
x = new MutableHashTable

--
getNewIdeal = method()
getNewIdeal(MutableHashTable) := x -> (
    I = randomMonomialIdeal({random(50,150), random(50,150)},R);
    Istr = toString gens gb I;
    if not x#?Istr then I else getNewIdeal(x)
)

-- generate ideals and match to betti tables
for i from 1 to 1000 do (
    I = getNewIdeal(x);

    Istr = toString gens gb I;
    x#Istr = toString matrix betti I;
)

hashx = new HashTable from x

f << toJSON hashx

f << close