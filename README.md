# Term checker

A command line script to check whether correct terminology is being used in a translation (tmx file).

Terminology is assumed to be listed in a tab-delimited text file in the following format:
```
source_term <tab> target_term
```

If multiple target terms exist for a given source term, it is assumed that these are entered on separate lines rather than all on the same line, e.g.:
```
source_term <tab> target_term_1
source_term <tab> target_term_2
source_term <tab> target_term_3
```

### Installation

Download **term_checker.py** from here and place in any directory of your choosing.

### Running the script

From the directory containing this script, terminal:
```
python3 term_checker.py translation.tmx glossary.txt
```

### Prerequisites

* Python 3
* [colorama 0.4.3](https://pypi.org/project/colorama/)
* [translate-toolkit 2.5.0](https://pypi.org/project/translate-toolkit/)
* [pytest 5.4.1](https://docs.pytest.org/en/latest/getting-started.html) (for running the tests)

### Built using:

* Python 3.7.6
* Visual Studio Code 1.44.2
* macOS 10.14.6

### License

Licensed under the MIT License.
