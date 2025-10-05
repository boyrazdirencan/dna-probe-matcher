# DNA Probe Sequence Matcher

## Overview
This application helps find exact matches of probe sequences within a target DNA sequence. It supports both forward (5'→3') and reverse complement (3'→5') orientations. This tool is particularly useful for molecular biology applications such as qPCR probe design and validation.

## Applications
- **qPCR Analysis**: Design and validate TaqMan probes, molecular beacons, and other qPCR detection probes
- **Primer Design**: Verify primer specificity against target sequences
- **Sequence Validation**: Confirm probe binding sites in genomic sequences
- **Research Applications**: General DNA sequence analysis and matching

## Quick Start

### Direct Execution (Recommended)
1. Open terminal/command prompt
2. Navigate to this directory
3. Run: `python dna_probe_matcher.py`
4. The GUI will open and you can start using the tool

## How to Use

### 1. Prepare Your Probe File
- Create a CSV file with two columns: 'Probe_Name' and 'Sequence'
- Each row should contain one probe with its name and nucleotide sequence
- Example:
```
Probe_Name,Sequence
Probe_001,ATGCGTCC
Probe_002,GGATCCGA
```

### 2. Using the Application
1. Click '📁 Upload Probe CSV' to upload your probe sequences
2. Enter or paste your target DNA sequence in the text area (A, T, G, C nucleotides only)
3. Click '🔍 Search Matches' to find all probe matches
4. Results will display in the table below with position, orientation, and matched sequence
5. Use '💾 Save Results' to export matches to CSV file
6. Use '🗑️ Clear All' to reset the application

### 3. Understanding Results
- **Probe Name**: The name of the probe that matched
- **Match Type**: Direction of match (5'→3' or 3'→5')
- **Start Position**: Starting position in the target sequence (1-based)
- **End Position**: Ending position in the target sequence (1-based)
- **Matched Sequence**: The actual sequence that matched

## Demo File
This package includes `probes_demo_short.csv` with example probes for testing:
```
Probe_Name,Sequence
Probe_5to3,GCGT
Probe_3to5,ACGC
Probe_NoMatch,TTTT
```
You can test with target sequences like `ATGCGT` to see matches in both orientations.

## Features
- Upload probe sequences from CSV file
- Search for matches in target DNA sequences
- Display results with position, orientation, and sequence
- Export results to CSV file
- User-friendly graphical interface with Tkinter
- Support for both forward and reverse complement matching
- Real-time character counter for sequence input
- Validation of nucleotide sequences
- Error handling and user feedback

## Requirements
- Python 3.x
- Tkinter (usually included with Python)
- Built-in Python modules: `tkinter`, `csv`, `typing`

## Supported Characters
- Only A, T, G, C nucleotides are supported in target sequences
- Case is ignored (a, t, g, c are treated same as A, T, G, C)

## Testing with Short Sequences
The application can be tested with short DNA sequences. For example, if your target sequence is `ATGCGT` and you have a probe `GCGT`, it will find a match. The demo file includes short sequences that are perfect for testing the application's functionality.

## Troubleshooting
- If you get a "module not found" error, ensure Python is installed with Tkinter support
- Make sure your CSV file has the correct format with 'Probe_Name' and 'Sequence' columns
- Target sequences should only contain valid nucleotides (A, T, G, C)
- Very large sequences may take time to process

## Files in this Package
- `dna_probe_matcher.py` - Main application
- `README.md` - This file
- `probes_demo_short.csv` - Example probe file for testing

## Example Workflow
1. Prepare a CSV file with your probe sequences
2. Run the application directly with `python dna_probe_matcher.py`
3. Upload your probe CSV file
4. Paste your target DNA sequence in the text area
5. Click "Search Matches"
6. Review results in the table
7. Export results if needed

© 2025 DNA Analysis Tool