# CodeLake


<img align="right" width=300 height=300 border-radius=50% src="https://user-images.githubusercontent.com/87585798/152438330-94652935-0809-4385-bf24-29cfcef0340a.png">
CodeLake is a handy parser that helps to download all your submissions from codeforces.com and save them in offline storage.

## Features

- Parsing submissions by user nickname
- Filtering by submission result/status
- Downloading the problem statement for each submission
- Sorting submissions by problems (2 submissions for 1 problem will be in the same folder)
- Saving parsed submission in extension appropriate to language it was written


## Installation
**Open your favorite Terminal and run these commands.**

*Clone repository.*
```sh
git clone https://github.com/CyCJIuK47/CodeLake.git
```
*Change the current directory to the place where you cloned the repository and install all the dependencies.*

```sh
cd path/where/you/cloned/the/project
pip install -r requirements.txt
```
## How to use
1. Open CodeLake folder and run `CodeLake.py`.
2. After GUI is opened write the nickname you want to parse.
3. In the Options menu choose a directory to store to (no need to create a new folder inside, the script will make it by itself).
4. Choose parsing filters or enable downloading problem statements for submissions.
