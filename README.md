# Term checker

Script to check whether correct terminology is being used in a translation (tmx file).

Terminology is assumed to be listed in a tab-delimited text file in the following format:
```
source_term __<tab>__ target_term
```

If multiple target terms exist for a given source term, it is assumed that these are entered on separate lines rather than all on the same line, e.g.:
```
source_term <tab> target_term_1
source_term <tab> target_term_2
source_term <tab> target_term_3
```

## Running the script

From the terminal:
```
python3 term_checker.py translation.tmx glossary.txt
```

## Prerequisites

* python 3
* colorama 0.4.3
* translate-toolkit 2.5.0
* pytest 5.4.1

## Built using:

* Visual Studio Code
* macOS 10.14.6

## License

This project is licensed under the MIT License.