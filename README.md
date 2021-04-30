# Term Checker

A command line script to check whether correct terminology is being used in a translation regardless of the inflected form of the terminology.

For example, let’s say we have a source text that contains the Japanese word “買う” (meaning to buy or to purchase) and a glossary indicating that this should be translated only as “buy”.  The difficulty here is that there are several forms in which “buy” can appear in the translation, such as “buy”, “buying”, and “bought”.  However, this script is able to check whether “buy” appears in the translation regardless of the form in which it appears.  To do this, it basically compares the dictionary form of the target term and the dictionary forms of the words appearing in the translation.  A natural language processing library called spaCy is used to help with this comparison process.

### Assumptions

It is assumed that the translation is a “.tmx” file and the terminology is listed in a “.txt” file in which a source term and a target term are separated by a tab character as in the example below.

source term<tab>target term
(here “<tab>” represents a tab character)

For example, in the case of a Japanese-to-English translation:

情報処理装置<tab>information processing device

If multiple target terms exist for a single source term, please enter these on separate lines as in the example below.

source term<tab>target term 1
source term<tab>target term 2

Again, in the case of a Japanese-to-English translation:

情報処理装置<tab>information processing device
情報処理装置<tab>information processing apparatus

### Running the script

To run the script on macOS, carry out the following steps.

1. Download the script to a location of your choice on your computer.
2. Open the Finder app and navigate to the folder that contains the script.
3. Use the mouse to right-click on this folder.
4. Select Services > New Terminal at Folder. This will open the Terminal app.
5. In the Terminal app, enter the following command making sure to replace “translation.tmx” with the name of your translation file and “glossary.txt” with the name of your glossary file.

```
python3 term-checker.py translation.tmx glossary.txt
```

If the script finds any errors in your translation, these will be displayed in the terminal for you to inspect.

### Prerequisites

* Python 3
* [Spacy](https://spacy.io/usage)
* [Spacy en_core_web_sm](https://spacy.io/models/en) (light-weight model for English)
* [colorama 0.4.3](https://pypi.org/project/colorama/) (to make output easier to read)
* [translate-toolkit 2.5.0](https://pypi.org/project/translate-toolkit/) (for handling tmx files)
* [pytest 5.4.1](https://docs.pytest.org/en/latest/getting-started.html) (for running the tests)

### Built using:

* Python 3.7.6
* Visual Studio Code 1.44.2
* macOS 10.14.6

### Example output:

(Please excuse the blurring but the translation text here is confidential.)

<img src="screenshot.png" width="650"></br>

### License

Licensed under the MIT License.
