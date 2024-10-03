#This is a script to rescale solute-solvent interactions as a function of Temperature in Martini3 
#function: ε' = ε * (T/T0) ^ α 
#Yingmin Jiang 27.09.2024

#Parse commandline arguments
import argparse
parser = argparse.ArgumentParser(description='This is a script to rescale solute-solvent interactions with temperature in Martini 3')
parser.add_argument("-i", "--input", type=str, help="Input: Martini topology file")
parser.add_argument("-o", "--output", type=str, help="Output: Martini topology file with rescaled protein-water interactions")
parser.add_argument("-p", "--rescaling_p", type=float, default=0, help="alpha: Rescaling factor for epsilon in P_beads-water LJ-potential")
parser.add_argument("-n", "--rescaling_n", type=float, default=0, help="alpha: Rescaling factor for epsilon in N_beads-water LJ-potential")
parser.add_argument("-c", "--rescaling_c", type=float, default=0, help="alpha: Rescaling factor for epsilon in C_beads-water LJ-potential")
parser.add_argument("-q", "--rescaling_q", type=float, default=0, help="alpha: Rescaling factor for epsilon in Q_beads-water LJ-potential")
parser.add_argument("-d", "--rescaling_d", type=float, default=0, help="alpha: Rescaling factor for epsilon in D_neads-water LJ-potential")
parser.add_argument("-t", "--temperature", type=float, default=300, help="simulation temperature")
args = parser.parse_args()

topfile = args.input
outputfile = args.output
rescaling_p = args.rescaling_p
rescaling_n = args.rescaling_n
rescaling_c = args.rescaling_c
rescaling_q = args.rescaling_q
rescaling_d = args.rescaling_d
simulation_t = args.temperature


print(f'Rescaling protein-water interactions in {topfile} with p_alpha={rescaling_p} n_alpha={rescaling_n} c_alpha={rescaling_c} q_alpha={rescaling_q} d_alpha={rescaling_d} at {simulation_t}K and writing new toplogy file {outputfile}.')

#Read topology file
with open(topfile, 'r') as f:
    toplines = f.readlines()

satisfied_lines = 0
modified_toplines = []
for topline in toplines:
    columns = topline.split()
    if len(columns) >= 2:
        if "W" in columns[0] and "P" in columns[1]:
            rescaling_alpha = rescaling_p
        elif "W" in columns[0] and "N" in columns[1]:
            rescaling_alpha = rescaling_n
        elif "W" in columns[0] and "C" in columns[1]:
            rescaling_alpha = rescaling_c
        elif "W" in columns[0] and "Q" in columns[1]:
            rescaling_alpha = rescaling_c
        elif "W" in columns[0] and "D" in columns[1]:
            rescaling_alpha = rescaling_d
        else:
            rescaling_alpha = None
        
        if rescaling_alpha is not None:
            original_epsilon = float(columns[4])
            T = simulation_t
            T0 = 300
            #Calculate the new epsilon
            new_epsilon = original_epsilon * (T/T0) ** rescaling_alpha
                
            # Create a new line with the rescaled epsilon
            new_topline = f'    {columns[0]}    {columns[1]}  {columns[2]} {columns[3]}    {new_epsilon:.4f} ; alpha={rescaling_alpha}, Original epsilon={original_epsilon} \n'
            modified_toplines.append(new_topline) 
            satisfied_lines += 1
                
        else:
            modified_toplines.append(topline)
    else:
        modified_toplines.append(topline)
                
#write output file
#Write new topology file
with open(outputfile,'w') as f:   
    f.writelines(modified_toplines)

print(f"Total number of lines that satisfied the condition: {satisfied_lines}")       
print('Finished!')

