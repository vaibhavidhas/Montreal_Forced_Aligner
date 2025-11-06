import subprocess
import os

# Define paths
base_dir = r"C:\Users\Client\Desktop\MFA_Project"
input_dir = os.path.join(base_dir, "input")
dict_path = os.path.join(base_dir, "custom_dict.txt")
output_dir = os.path.join(base_dir, "output")

# Activate environment (Windows)
activate_env = "conda activate aligner_1 && "

# Step 1: G2P
subprocess.run(f'{activate_env}mfa g2p english_us_arpa "{input_dir}" "{base_dir}\\custom_dict"', shell=True)

# Step 2: Align
subprocess.run(f'{activate_env}mfa align "{input_dir}" "{dict_path}" english_us_arpa "{output_dir}" --clean', shell=True)

print("MFA pipeline finished successfully.")
