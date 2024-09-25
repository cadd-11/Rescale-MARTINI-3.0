import os
import re
import math

# Define the parent directory path where the files are located
parent_directory = "/media/yingmin/LaCie/Project1/CG_30chains/modify_martini3/s2_-2_0.7q"

# Search for specific files in the parent directory and its subdirectories
files = []
for root, _, filenames in os.walk(parent_directory):
    for filename in filenames:
        if filename.endswith("martini_v3.0.0.itp"):
            files.append(os.path.join(root, filename))

# Loop through each file
for file_path in files:
    # Extract the number from the folder name
    folder_name = os.path.basename(os.path.dirname(file_path))
    folder_number = re.search(r'\d+', folder_name).group()
    
    # Read the file content
    with open(file_path, "r") as f:
        toplines = f.readlines()
    
    satisfied_lines = 0
    # Modify lines containing "W" and "W" or "P" and "C" in the first and second column
    modified_toplines = []
    for topline in toplines:
        columns = topline.split()
        if len(columns) >= 2:
            if "W" in columns[0] and "C" in columns[1]:
                rescaling_n = float(math.pow(int(folder_number) / 300, -2))
            elif "W" in columns[0] and "P" in columns[1]:
                rescaling_n = float(math.pow(int(folder_number) / 300, 0))
            elif "W" in columns[0] and "Q" in columns[1]:
                rescaling_n = float(math.pow(int(folder_number) / 300, 0.7))
            else:
                rescaling_n = None
                
            if rescaling_n is not None:
               
                original_epsilon = float(columns[4])
            
                
                #Calculate the new epsilon
                new_epsilon = original_epsilon * rescaling_n

                # Create a new line with the rescaled epsilon
                new_topline = f'    {columns[0]}    {columns[1]}  {columns[2]} {columns[3]}    {new_epsilon:.4f} ; n_Lambda={rescaling_n:.2f}, Original epsilon={original_epsilon} \n'
            
                modified_toplines.append(new_topline)   
                satisfied_lines += 1
                
            else:
                modified_toplines.append(topline)
        else:
            modified_toplines.append(topline)

    # Save the modified content to a new file
    #rescaling_n_formatted = "{:.2f}".format(rescaling_n)
    new_file_name = f"martini_v3.0.0_beta_{folder_number}.itp"
    new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
    with open(new_file_path, "w") as f:
        f.writelines(modified_toplines)
    
    print(f"Modified file created: {new_file_path}")
    print(f"Total number of lines that satisfied the condition: {satisfied_lines}")
    print(f"'\u03BC' of CW:{float(math.pow(int(folder_number) / 300, -2))}")
    print(f"'\u03BC' of PW:{float(math.pow(int(folder_number) / 300, 0))}")
    print(f"'\u03BC' of QW:{float(math.pow(int(folder_number) / 300, 0.7))}")
  
