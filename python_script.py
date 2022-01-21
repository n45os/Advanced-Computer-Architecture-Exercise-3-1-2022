from os import listdir
import os
import sys
# import pandas as pd
import csv
import math

from energy import get_energy

folder_path = ""#sys.argv[1]

def get_info(folder):
    with open(f"{folder}/my_stats.csv", 'r') as f:
        reader = csv.reader(f)
        # d = {
		# 	"cpi" : 0,
		# 	"l1ds" : 0,
		# 	"l1is" : 0,
		# 	"l2s": 0,
		# 	"l1da": 0,
		# 	"l1ia" : 0,
		# 	"l2a" : 0,
		# 	"cl" : 0
		# }
        big_d = {}
        i=0
        for row in reader:
            
            d = {
			"cpi" : float(row[0]),
			"l1ds" : float(row[1]),
			"l1is" : float(row[2]),
			"l2s": float(row[3]),
			"l1da": float(row[4]),
			"l1ia" : float(row[5]),
			"l2a" : float(row[6]),
			"cl" : float(row[7]),
			"formula": float(0),
            "energy" : 0,
            "leakage" : 0,
            "dynamic" : 0,
            "total" : 0,
            "delay" : 0,
            "area" : 0
			}
            big_d[i] = d
            i+=1
    return big_d

def calculate_formula(info_dict):
    for d in info_dict:
        # cpi = d["cpi"]
        # first = math.pow(cpi,3)
        # second = (3*(math.log(info_dict[d]["l1is"],2) + math.log(info_dict[d]["l1info_dict[d]s"],2)) +math.log(info_dict[d]["l2s"],8))
        formula = pow(info_dict[d]["cpi"],3) * (3*(math.log(info_dict[d]["l1is"],2) + math.log(info_dict[d]["l1ds"],2)) +\
                    	math.log(info_dict[d]["l2s"],8) + 80/math.log(info_dict[d]["l1is"],2) + \
                        80/math.log(info_dict[d]["l1ds"],2) + 8/math.log(info_dict[d]["l2s"],8) +\
                        math.log(info_dict[d]["l1ia"],2) + math.log(info_dict[d]["l1da"],2) + math.log(info_dict[d]["l2a"],2)+\
                        math.log(info_dict[d]["cl"],4)/2)
        info_dict[d]["formula"] = formula
    return info_dict

def get_e_d(folder, info_dict= {}):
    for d in info_dict:
        filename = f'specbzip__l1ds_{int(info_dict[d]["l1ds"])}__l1id_{int(info_dict[d]["l1is"])}__l2s_{int(info_dict[d]["l2s"])}__l1da_{int(info_dict[d]["l1da"])}__l1ia_{int(info_dict[d]["l1ia"])}__l2a_{int(info_dict[d]["l2a"])}__cl_{int(info_dict[d]["cl"])}'
   #    with open(f"{folder_path}/{filename}", 'r') as f:
   #         pass
        os.system(f"python GEM5ToMcPAT.py {folder}/{filename}/stats.txt {folder}/{filename}/config.json inorder_arm.xml -o made_xmls/{filename}")
        os.system(f"../mcpat/mcpat -infile made_xmls/{filename} -print_level 5 > made_prints/{filename}")
        # os.system(f"python print_energy.py made_prints/{filename} folder/{filename}/stats.txt")
        info_dict[d]["energy"], info_dict[d]["leakage"], info_dict[d]["dynamic"], info_dict[d]["total"], info_dict[d]["runtime"], info_dict[d]["area"] = get_energy(f"made_prints/{filename}", f"{folder}/{filename}/stats.txt" )
    return info_dict
def dict_to_csv(dict, filename):
    header = "formula,energy,area,delay"
    with open("filename", 'w') as f:
        f.write(header)
        for d in dict:
            input = f'{dict[d]["formula"]},{dict[d]["energy"]},{dict[d]["area"]},{dict[d]["runtime"]}'
            f.write(input)
        
    

dict = get_info("spec_results_p2_specbzip")
dict = calculate_formula(dict)
dict = get_e_d("spec_results_p2_specbzip",dict)
dict_to_csv(dict, "big_stats.csv")


print(dict)
