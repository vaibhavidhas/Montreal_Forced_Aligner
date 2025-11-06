
# Forced Alignment using Montreal Forced Aligner (MFA)

This project demonstrates how to perform **forced alignment** between speech audio (`.wav`) and its corresponding transcript (`.txt`) using the **Montreal Forced Aligner (MFA)** — a powerful tool built on top of **Kaldi** for aligning speech to phonetic transcriptions.

---

## Overview

**Goal:** Automatically generate `.TextGrid` files that align each word and phoneme with its precise timestamp in the audio.

**Inputs:**
- `.wav` audio files (Mono, 16kHz recommended)
- `.txt` transcript files (cleaned text)

**Outputs:**
- `.TextGrid` files containing word and phone-level alignments (viewable in [Praat](https://www.fon.hum.uva.nl/praat/))

---

## 1. Installation

### Step 1: Install Anaconda
Download and install [Anaconda](https://www.anaconda.com/download).

Then open **Anaconda Prompt** (Windows) or Terminal (Mac/Linux).

### Step 2: Create MFA environment
```bash
conda create -n aligner python=3.9 -y
conda activate aligner


### Step 3: Install Montreal Forced Aligner

```bash
pip install montreal-forced-aligner
```

To verify installation:

```bash
mfa version
```

---

## 2. Download Pretrained Models

MFA provides pretrained dictionaries and acoustic models.

| Model name        | Description                                           |
| ----------------- | ----------------------------------------------------- |
| `english_mfa`     | General American English, trained on LibriSpeech      |
| `english_us_arpa` | US English tuned for ARPAbet pronunciation dictionary |
| `english_mfa_lm`  | Larger model with language-model smoothing            |
| `english_uk_mfa`  | British English accent model                          |
| `english_mfa_v2`  | Updated, more accurate version of general model       |

`english_us_arpa`
Description:

Acoustic model tuned to work with ARPAbet-based dictionaries (like english_us_arpa dictionary).

Use when:

Your pronunciation dictionary uses ARPAbet phonemes (e.g., AH0, K, T),
not IPA symbols (like /ə/, /k/, /t/).

You built or used a custom ARPA dictionary via G2P (grapheme-to-phoneme) conversion.
Hence Acoustic model english_us_arpa was used

For **English (US)** alignment:

```bash
mfa model download dictionary english_us_arpa
mfa model download acoustic english_us_arpa
```

This will store the models in:

```
C:\Users\<username>\Documents\MFA\pretrained_models\
```
 4. (Optional) Create a Custom Dictionary

Sometimes MFA labels words as UNK (unknown) or SPN (spoken noise).
This happens when those words are not found in the default dictionary (english_us_arpa).

You can fix this by creating a custom pronunciation dictionary.

Example: custom_dict.txt
justice  JH AH1 S T AH0 S
massachusetts  M AE2 S AH0 CH UW1 S AH0 T S
dukakis  D UW0 K AA1 K IH0 S
hennessy  HH EH1 N AH0 S IY0


Each line contains:
word [tab or space] ARPAbet phonemes

You can mix your new entries with the pretrained dictionary if needed.

 5. Run Alignment
Option 1: Using Pretrained Dictionary
```
mfa align "PATH TO INPUT .txt and .wav files" english_us_arpa english_us_arpa "PATH TO OUTPUT"
```

Option 2: Using Custom Dictionary
```
mfa align "PATH TO INPUT .txt and .wav files" "PATH TO CUSTOM DICTIONARY.txt" english_us_arpa "PATH TO OUTPUT"
```


Input folder: .wav and .txt pairs

Dictionary: custom or pretrained

Acoustic model: english_mfa

Output folder: where .TextGrid files are saved

---

## 3. Prepare Dataset

Your input folder should contain **paired** `.wav` and `.txt` files:

```
input/
│
├── sample1.wav
├── sample1.txt
├── sample2.wav
├── sample2.txt
```

> Each `.txt` file must have **the same name** as its corresponding `.wav` file.

### Optional: Clean text automatically

Use this helper script to clean transcripts before alignment.
Good to clean text. MFA lower cases the words but punctuations or numbers can create UNKNOWN words in the output.

```python
# clean_texts.py
import os, re

input_dir = r"C:\Users\Client\Desktop\MFA_Project\transcripts"
output_dir = r"C:\Users\Client\Desktop\input"

os.makedirs(output_dir, exist_ok=True)

for fname in os.listdir(input_dir):
    if fname.lower().endswith(".txt"):
        with open(os.path.join(input_dir, fname), "r", encoding="utf8") as f:
            text = f.read()

        text = re.sub(r"[^a-zA-Z' ]+", " ", text)
        text = re.sub(r"\s+", " ", text)
        text = text.lower().strip()

        with open(os.path.join(output_dir, fname), "w", encoding="utf8") as f:
            f.write(text)

print(f" Cleaned text files saved in {output_dir}")
```

Run it:

```bash
python clean_texts.py
```

---


## 5. Output

After alignment, the output folder will contain:

```
output/
├── sample1.TextGrid
├── sample2.TextGrid
```

Each `.TextGrid` file includes:

* **word tier** – word-level boundaries
* **phone tier** – phoneme-level boundaries

You can open these in **Praat**:

1. Open Praat → *File → Open → Read from file…*
2. Select both `.wav` and `.TextGrid`
3. View alignment → *View & Edit*
   
---

## 6. Example Folder Structure

```
MFA_Project/
│
├── input/
│   ├── audio1.wav
│   ├── audio1.txt
│   ├── audio2.wav
│   ├── audio2.txt
│
├── output/
│   ├── audio1.TextGrid
│   ├── audio2.TextGrid
│
├── clean_texts.py
├── clean_transcripts
├── Transcripts
│   ├── audio1.txt
│   ├── audio2.txt
├── WAV
│   ├── audio2.wav
│   ├── audio2.wav
├──custom_dict.txt
├── PRAAT
├── run_mfa_file
└── README.md
```
Go to Command Line and inside the directory type 
```
python run_mfa_pipeline.py
```


---

## References

* [Montreal Forced Aligner Documentation](https://montreal-forced-aligner.readthedocs.io/)
* [MFA Pretrained Models](https://github.com/MontrealCorpusTools/mfa-models)
* [Praat Software](https://www.fon.hum.uva.nl/praat/)

---


