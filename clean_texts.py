import os, re

# 🔹 Path to your input transcript folder
input_dir = r"C:\Users\Client\Desktop\MFA_Project\transcripts"

# 🔹 Path to cleaned output folder
output_dir = r"C:\Users\Client\Desktop\input"

os.makedirs(output_dir, exist_ok=True)

# --- STEP 1: Rename .TXT → .txt only ---
for fname in os.listdir(input_dir):
    old_path = os.path.join(input_dir, fname)
    new_name = fname

    if fname.endswith(".TXT"):
        new_name = fname[:-4] + ".txt"

    new_path = os.path.join(input_dir, new_name)
    if new_path != old_path:
        os.rename(old_path, new_path)

print("✅ Renamed .TXT → .txt")

# --- STEP 2: Clean up the text files ---
for fname in os.listdir(input_dir):
    if fname.endswith(".txt"):
        with open(os.path.join(input_dir, fname), "r", encoding="utf8") as f:
            text = f.read()

        # Clean the text: remove punctuation/numbers, normalize spaces
        text = re.sub(r"[^a-zA-Z' ]+", " ", text)
        text = re.sub(r"\s+", " ", text)
        text = text.lower().strip()

        # Save cleaned text into output folder
        with open(os.path.join(output_dir, fname), "w", encoding="utf8") as f:
            f.write(text)

print(f"✅ Cleaned text files saved in {output_dir}")
