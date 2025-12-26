-- load package for generating random ideals
loadPackage "RandomIdeals"

-- create file object; possibly parameterize to enumerate? or run outside script to rename when cleaning
f = "ideals/generated ideals/ideals_n.txt" << ""

-- define ring and list of grades of ideals
R = QQ[x,y,z]
L = {3,3,3,3}

-- generate 50 random monomial ideals and write to file
for i from 1 to 50 do (
    I = randomMonomialIdeal(L,R);
    f << I << endl;
)

f << close