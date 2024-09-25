#This is a script to rescale protein-water interactions in Martini
#F. Emil Thomasen 23.06.2021

#Parse commandline arguments
import argparse
parser = argparse.ArgumentParser(description='This is a script to rescale protein-water interactions in Martini')
parser.add_argument("-i", "--input", type=str, help="Input: Martini topology file")
parser.add_argument("-o", "--output", type=str, help="Output: Martini topology file with rescaled protein-water interactions")
#edit_start_ym
parser.add_argument("-p", "--rescaling_p", type=float, default=1, help="Lambda: Rescaling factor for epsilon in p-water LJ-potential")
parser.add_argument("-m", "--rescaling_m", type=float, default=1, help="Lambda: Rescaling factor for epsilon in m-water LJ-potential")
parser.add_argument("-c", "--rescaling_c", type=float, default=1, help="Lambda: Rescaling factor for epsilon in c-water LJ-potential")
parser.add_argument("-q", "--rescaling_q", type=float, default=1, help="Lambda: Rescaling factor for epsilon in q-water LJ-potential")
parser.add_argument("-d", "--rescaling_d", type=float, default=1, help="Lambda: Rescaling factor for epsilon in d-water LJ-potential")
parser.add_argument("-n", "--nr_proteins",  type=int, default=1, help="Number of proteins in topology. One protein by default")
args = parser.parse_args()

topfile = args.input
outputfile = args.output
rescaling_p = args.rescaling_p
rescaling_m = args.rescaling_m
rescaling_c = args.rescaling_c
rescaling_q = args.rescaling_q
rescaling_d = args.rescaling_d
nr_proteins = args.nr_proteins

print(f'Rescaling protein-water interactions in {topfile} with p_lambda={rescaling_p} n_lambda={rescaling_m} c_lambda={rescaling_c} q_lambda={rescaling_q} d_lambda={rescaling_d} and writing new toplogy file {outputfile}.')

#edit_end_ym
#Read topology file lines
with open(topfile, 'r') as f:
    toplines = f.readlines()

######################################
####       GET PROTEIN BEADS      ####
######################################

#Find start of protein molecule
proteinfound=False
for i,topline in enumerate(toplines):
    if '[ moleculetype ]' in topline:
        if 'Protein' in toplines[i+1]:
            protein_start_line = i+1
            proteinfound=True
            break           
assert proteinfound==True, 'Could not find protein molecule in topology. Make sure your protein is named something with "Protein".'

#Find start of protein beads
for i in range(protein_start_line,len(toplines)):
    if '[ atoms ]' in toplines[i]:
            beads_start_line = i+1
            break

#Make list of protein beads edit_start_ym
polar_beads = []
apolar_beads = []
midpolar_beads = []
monions_beads = []
diions_beads = []
for i in range(beads_start_line,len(toplines)):
    if 'P' in toplines[i].split()[1]:
    	polar_beads.append(toplines[i].split()[1])
    
    if '[' in toplines[i+1] or len(toplines[i+1].split())==0:
        beads_end_line = i+1
        break

for i in range(beads_start_line,len(toplines)):
    if 'C' in toplines[i].split()[1]:
    	apolar_beads.append(toplines[i].split()[1])
    
    if '[' in toplines[i+1] or len(toplines[i+1].split())==0:
        beads_end_line = i+1
        break

for i in range(beads_start_line,len(toplines)):
    if 'N' in toplines[i].split()[1]:
    	midpolar_beads.append(toplines[i].split()[1])
    
    if '[' in toplines[i+1] or len(toplines[i+1].split())==0:
        beads_end_line = i+1
        break
        
for i in range(beads_start_line,len(toplines)):
    if 'Q' in toplines[i].split()[1]:
    	monions_beads.append(toplines[i].split()[1])
    
    if '[' in toplines[i+1] or len(toplines[i+1].split())==0:
        beads_end_line = i+1
        break
        
for i in range(beads_start_line,len(toplines)):
    if 'D' in toplines[i].split()[1]:
    	diions_beads.append(toplines[i].split()[1])
    	
    if '[' in toplines[i+1] or len(toplines[i+1].split())==0:
        beads_end_line = i+1
        break
        
print(list(set(polar_beads)))
print(list(set(apolar_beads)))
print(list(set(midpolar_beads)))
print(list(set(monions_beads)))
print(list(set(diions_beads)))
#edit_end_ym

#If there is more than one protein, also get beads from other proteins
if nr_proteins > 1:
    for protein in range(nr_proteins-1):
        
        #Find start of protein molecule (but after end of previous protein)
        proteinfound=False
        for i in range(beads_end_line,len(toplines)):
            if '[ moleculetype ]' in toplines[i]:
                if 'Protein' in toplines[i+1]:
                    protein_start_line = i+1
                    proteinfound=True
                    break
        assert proteinfound==True, 'Could not find protein molecule in topology. Make sure your protein is named something with "Protein".'

        #Find start of protein beads
        for i in range(protein_start_line,len(toplines)):
            if '[ atoms ]' in toplines[i]:
                    beads_start_line = i+1
                    break

        #Append beads to list of protein beads
        for i in range(beads_start_line,len(toplines)):

            polar_beads.append(toplines[i].split()[1])
            
            #Stop if next line is the beginning of new toplogy stuff
            #(if your toplogy file is strangely formatted, maybe this will cause a problem)
            if '[' in toplines[i+1] or len(toplines[i+1].split())==0:
                beads_end_line = i+1
                break


#####################################################
####     RESCALE PROTEIN-WATER INTERACTIONS      ####
#####################################################

#Find nonbonded interaction parameters
for i,topline in enumerate(toplines):
    if '[ nonbond_params ]' in topline:
        nonbonded_start_line = i+1
        break

#Make list of new toplogy lines for creating output file
new_toplines = toplines[:nonbonded_start_line]

#Loop through nonbonded lines to find interactions between W and protein beads
for i in range(nonbonded_start_line,len(toplines)):
    
    #Check if line contains a W bead
    if 'W' in toplines[i]:
        
        #Check if line contains polar bead
        if toplines[i].split()[0] in polar_beads or toplines[i].split()[1] in polar_beads:
            #Rescale epsilon
            new_epsilon = float(toplines[i].split()[4])*rescaling_p
            #Create new line with rescaled epsilon
            new_topline = f'    {toplines[i].split()[0]}    {toplines[i].split()[1]}  {toplines[i].split()[2]} {toplines[i].split()[3]}    {new_epsilon} ; p_Lambda={rescaling_p}, Original epsilon={toplines[i].split()[4]} \n'

#edit_start_ym          
        #Check if line contains apolar bead
        elif toplines[i].split()[0] in apolar_beads or toplines[i].split()[1] in apolar_beads:
           #Rescale epsilon
           new_epsilon = float(toplines[i].split()[4])*rescaling_c
           #Create new line with rescaled epsilon
           new_topline = f'    {toplines[i].split()[0]}    {toplines[i].split()[1]}  {toplines[i].split()[2]} {toplines[i].split()[3]}    {new_epsilon} ; c_Lambda={rescaling_c}, Original epsilon={toplines[i].split()[4]} \n'
           
        #Check if line contains intermediate_polar bead
        elif toplines[i].split()[0] in midpolar_beads or toplines[i].split()[1] in midpolar_beads:
           #Rescale epsilon
           new_epsilon = float(toplines[i].split()[4])*rescaling_m
           #Create new line with rescaled epsilon
           new_topline = f'    {toplines[i].split()[0]}    {toplines[i].split()[1]}  {toplines[i].split()[2]} {toplines[i].split()[3]}    {new_epsilon} ; m_Lambda={rescaling_m}, Original epsilon={toplines[i].split()[4]} \n'   
        
        #Check if line contains monovalent ions bead
        elif toplines[i].split()[0] in monions_beads or toplines[i].split()[1] in monions_beads:
           #Rescale epsilon
           new_epsilon = float(toplines[i].split()[4])*rescaling_q
           #Create new line with rescaled epsilon
           new_topline = f'    {toplines[i].split()[0]}    {toplines[i].split()[1]}  {toplines[i].split()[2]} {toplines[i].split()[3]}    {new_epsilon} ; q_Lambda={rescaling_q}, Original epsilon={toplines[i].split()[4]} \n'
        
        #Check if line contains divalent ions bead edit_jym
        elif toplines[i].split()[0] in diions_beads or toplines[i].split()[1] in diions_beads:
           #Rescale epsilon
           new_epsilon = float(toplines[i].split()[4])*rescaling_d
           #Create new line with rescaled epsilon
           new_topline = f'    {toplines[i].split()[0]}    {toplines[i].split()[1]}  {toplines[i].split()[2]} {toplines[i].split()[3]}    {new_epsilon} ; d_Lambda={rescaling_d}, Original epsilon={toplines[i].split()[4]} \n'
        
              
        #If not, new topology line will be the same as the old one
        else: new_topline = toplines[i]
            
    #If not, new topology line will be the same as the old one
    else:
        new_topline = toplines[i]
    
    #Append new topology line to list
    new_toplines.append(new_topline)
    
    #Stop if next line is the beginning of new toplogy stuff
    #(if your toplogy file is strangely formatted, maybe this will cause a problem)
    if '[' in toplines[i+1]:
        nonbonded_end_line = i+1
        break

####################################
####     WRITE OUTPUT FILE      ####
####################################

#Make sure new toplogy and old topology have the same length
assert len(new_toplines+toplines[nonbonded_end_line:])==len(toplines), 'Output topology was not the same length as input. There is a problem somewhere.'

#Write new topology file
with open(outputfile,'w') as f:
    for line in new_toplines:
        f.write(line)
    for line in toplines[nonbonded_end_line:]:
        f.write(line)
        
print('Finished!')
