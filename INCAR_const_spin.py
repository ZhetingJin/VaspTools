# read INCAR file
incarfilename = "INCAR"
incarfile = open(incarfilename, 'r')
lines = incarfile.readlines()
incarfile.close()

# find the MAGMOM line
for i, line in enumerate(lines):
    # print the original lines
    print(line.strip())
    line_split = line.strip().split()
    
    # if empty line, skip
    if len(line_split) == 0:
        continue
        
    # if MAGMOM is found, then add the constrained spin parameters
    if line_split[0] == "MAGMOM":
        print("I_CONSTRAINED_M = 2")
        M_CONSTR = "M_CONSTR ="
        for ele in line_split[2:24]:
            ele_split = ele.split("*")
            if "*" in ele:
                unit = " 0 0 " + ele_split[1]
                M_CONSTR += int(ele_split[0])*unit
            else:
                M_CONSTR += " 0 0 " + ele_split[0]
                
        print(M_CONSTR)
