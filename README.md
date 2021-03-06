# Image Preview
![plot](https://cdn.discordapp.com/attachments/795277227423301643/947602124563415090/unknown.png "Display Image")

---
![lines](https://img.shields.io/tokei/lines/github/lucascompython/counting-lines)
# Counting lines, files and folders in a directory 

This projects counts all lines of code(except compiled), files and directories in a folder.

## Installation and Execution 
```sh
git clone https://github.com/lucascompython/counting-lines.git
cd counting-lines
pip3 install -r requirements.txt
python3 main.py
```
## Features

This program supports argument parsing.

Example:
```sh
python3 main.py --path ~/Desktop -d node_modules -i .ini --verbose
```
Use this to get some help:
```sh
python3 main.py --help
```
### Requirements

- `Python` obviously...
- [`Colorama`](https://pypi.org/project/colorama/)
- [`PrettyTable`](https://pypi.org/project/prettytable/)

