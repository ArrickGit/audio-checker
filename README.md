# Audio Checker

This script scans audio files, groups them by line ID, compares each language duration against English, and writes the result to a CSV report.

## Expected Folder Structure

Audio can be placed inside language folders:

```text
audio/
  eng/
    VO_AUDIO_01_02_03_CA_06_002_CHAR@234#ENG.wav
  jpn/
    VO_AUDIO_01_02_03_CA_06_002_CHAR@234#JPN.wav
  ger/
    VO_AUDIO_01_02_03_CA_06_002_CHAR@234#GER.wav
```

The script searches recursively, so files inside subfolders will be found.

## Expected Filename Format

Example:

```text
VO_AUDIO_01_02_03_CA_06_002_CHAR@234#ENG.wav
```

The script reads:

```text
Scene: AUDIO_01_02_03_CA
Line ID: 234
Language: ENG
```

## Python Environment In VS Code On Windows

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run this once:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate the environment again.

In VS Code:

1. Press `Ctrl+Shift+P`
2. Select `Python: Select Interpreter`
3. Choose `.venv\Scripts\python.exe`

## Install Requirements

From the `audioChecker` folder:

```powershell
pip install -r requirements.txt
```

## Run The Program

From the project folder:

```powershell
python main.py
```

By default, the script reads from:

```text
audioChecker/audio
```

and writes:

```text
audioChecker/audio_duration_report.csv
```

## Change The Input Folder

Option 1: pass the folder when running the script:

```powershell
python main.py "C:\path\to\audio_folder"
```

Option 2: edit this line in `main.py`:

```python
folder_path = Path(__file__).parent / "audio"
```

## Change The Output CSV Path Or Name

Option 1: pass the input folder and output CSV path when running:

```powershell
python main.py "C:\path\to\audio_folder" "C:\path\to\audio_duration_report.csv"
```

Option 2: edit this line in `main.py`:

```python
default_output_path = Path(__file__).parent / "audio_duration_report.csv"
```

## CSV Output

The CSV columns are:

```text
Line ID, Scene, ENG Duration, SCH Duration, JPN Duration, SPA Duration, FRE Duration, ITA Duration, BRA Duration, GER Duration, Biggest Diff
```

Output values:

```text
NIL = audio file for that language was not found
- = duration matches English after rounding to 2 decimal places
number = duration is different from English
```
