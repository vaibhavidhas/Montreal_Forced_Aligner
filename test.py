# test_mfa_errors.py
import os
from praatio import tgio

# ==== CONFIGURE ====
# Folder where your MFA TextGrid outputs are
TEXTGRID_FOLDER = r"C:\Users\Client\Desktop\MFA_Project\output"
REPORT_FILE = r"C:\Users\Client\Desktop\MFA_Project\alignment_report.txt"

# ==== FUNCTION TO CHECK ALIGNMENT ====
def analyze_textgrid(file_path):
    tg = tgio.openTextgrid(file_path)
    
    # Get word tier (usually named 'words' in MFA output)
    word_tier_name = 'words'
    phone_tier_name = 'phones'
    
    results = {
        "oov_words": [],
        "skipped_phones": [],
        "timing_offsets": []
    }
    
    # ---- WORD TIER ----
    if word_tier_name in tg.tierNameList:
        word_tier = tg.tierDict[word_tier_name]
        for start, end, label in word_tier.entryList:
            label_clean = label.strip()
            if label_clean in ["<unk>", "", None]:
                results["oov_words"].append((start, end, label))
    else:
        print(f"Warning: '{word_tier_name}' tier not found in {file_path}")
    
    # ---- PHONE TIER ----
    if phone_tier_name in tg.tierNameList:
        phone_tier = tg.tierDict[phone_tier_name]
        for start, end, label in phone_tier.entryList:
            label_clean = label.strip()
            if label_clean in ["spn", "", None]:
                results["skipped_phones"].append((start, end, label))
            else:
                # Detect if timing is too short or unusual (approx offset)
                duration = end - start
                if duration < 0.01:  # 10 ms as arbitrary short threshold
                    results["timing_offsets"].append((start, end, label))
    else:
        print(f"Warning: '{phone_tier_name}' tier not found in {file_path}")
    
    return results

# ==== MAIN ====
def main():
    all_results = {}
    
    tg_files = [f for f in os.listdir(TEXTGRID_FOLDER) if f.endswith(".TextGrid")]
    
    for tg_file in tg_files:
        full_path = os.path.join(TEXTGRID_FOLDER, tg_file)
        result = analyze_textgrid(full_path)
        all_results[tg_file] = result
    
    # Write report
    with open(REPORT_FILE, "w") as f:
        for tg_file, result in all_results.items():
            f.write(f"=== File: {tg_file} ===\n")
            
            f.write("OOV Words:\n")
            if result["oov_words"]:
                for start, end, label in result["oov_words"]:
                    f.write(f"  {label} ({start:.2f}-{end:.2f})\n")
            else:
                f.write("  None\n")
            
            f.write("Skipped Phonemes:\n")
            if result["skipped_phones"]:
                for start, end, label in result["skipped_phones"]:
                    f.write(f"  {label} ({start:.2f}-{end:.2f})\n")
            else:
                f.write("  None\n")
            
            f.write("Timing Offsets (very short phones):\n")
            if result["timing_offsets"]:
                for start, end, label in result["timing_offsets"]:
                    f.write(f"  {label} ({start:.2f}-{end:.2f})\n")
            else:
                f.write("  None\n")
            
            f.write("\n")
    
    print(f"Report generated at: {REPORT_FILE}")

if __name__ == "__main__":
    main()
