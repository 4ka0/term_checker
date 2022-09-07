# Term Checker

A command line script to check whether correct terminology is being used in a translation regardless of the inflected form of the terminology.

For example, let’s say we have a source text that contains the Japanese word “買う” (meaning to buy or to purchase) and a glossary indicating that this should be translated only as “buy”.  The difficulty here is that there are several forms in which “buy” can appear in the translation, such as “buy”, “buying”, and “bought”.  However, this script is able to check whether “buy” appears in the translation regardless of the form in which it appears.  To do this, it basically compares the dictionary form of the target term and the dictionary forms of the words appearing in the translation.  The NLP library spaCy is used to help with this comparison process.

### Assumptions

It is assumed that the translation is a “.tmx” file and the terminology is listed in a “.txt” file in which a source term and a target term are separated by a tab character as in the example below.
```
source term<tab>target term
```
(here “\<tab\>” represents a tab character)

For example, in the case of a Japanese-to-English translation:
```
情報処理装置<tab>information processing device
```
If multiple target terms exist for a single source term, please enter these on separate lines as in the example below.
```
source term<tab>target term 1
source term<tab>target term 2
```
Again, in the case of a Japanese-to-English translation:
```
情報処理装置<tab>information processing device
情報処理装置<tab>information processing apparatus
```
### Running the script

```
python3 term-checker.py translation.tmx glossary.txt
```

Replace “translation.tmx” with the name of your translation file and “glossary.txt” with the name of your glossary file.

If the script finds any errors in your translation, these will be displayed in the terminal for you to inspect.

### Built using:

* Python 3.7.6
* spaCy
* spaCy en_core_web_sm (light-weight model for English)
* colorama 0.4.3 (to help make the output easier to read)
* translate-toolkit 2.5.0 (for handling tmx files)
* pytest 5.4.1 (for running tests)

### Example output:

(Please excuse the blurring but the translation text here is confidential.)

<img src="screenshot.png" width="650">
