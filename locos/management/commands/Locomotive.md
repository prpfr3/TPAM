### Locomotive_L1_BRD_Extract.py

A once only extract of BRD Locomotives
Should not need to be repeated as the data has not been known to change
Outputs to Locomotive_BRD.csv

### Locomotive_L2_BRD_Merge_Classinfo.py

Again would normally be a once only extract although further cleansing of the Class information could make a reload beneficial

Inputs:- 

"Locomotive_BRD.csv"
"Class_BRD_Steam_Cleansed.csv"

Outputs:-

"Locomotive_BRD_Enhanced.csv"

Note that BRD classes are not held in a TPAM table. Only a url reference to the BRD class webpage is held.

### Locomotive_L3_BRD_Load.py

Inputs:-

"Locomotive_BRD_Enhanced.csv"

Outputs:-

Populated Locomotive table.

An identifier is created from a merger of companies and BRD locomotive numbers where available. 
