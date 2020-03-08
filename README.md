# JottiinShell
A shell extension to [jotti.in](https://jotti.in/) to allow for note taking in terminal.

## Usage
Jotti requires an account at [jotti.in](https://jotti.in/)

To write a note simply call:

`jotti "this is my note!"`

To view your notes call:

`jotti --notes`

or

`jotti --view-notes`

To save your credentials:

`jotti --auth`

## Download executable
[Windows](https://sourceforge.net/projects/jotti/files/jotti.exe)

[Ubuntu](https://sourceforge.net/projects/jotti/files/jotti)

## Compilation
1. Install [python](https://www.python.org/).
2. Install pyinstaller with `pip install pyinstaller`
3. Compile binary with `pyinstaller --onefile jotti.py`
4. Executable is located in the dist folder.

