# Skills tagger and classifier

This repository holds two flask apps and the workings behind them which provides a systematic way of tagging and classifying tech job posts for segmenting out their skills section.

## Data

There are two repositories and one data file that contain relavent data. These are:
 - files, which contains ~1500 job postings from Indeed with from searching for software roles.
 - out, json files from the tagger flask app,
 - data.csv, tagged data used for training and testing the ML algorithm

## tagger.py

Tagger is a mini flask app that takes in job data files and allows a user to copy and paste from the text into a textbox that will submit the section for tagging. This current is set up to do skills tagging for tech roles.


## tagged.py

tagged.py matches the tagged sentences back with the original document, generating a csv of the given format:
| index | document | sentence | label |
| ----- | -------- | -------- | ----- |

## training.py

The actual training of the ML model. Currently, this version uses a Multinomial Naive Bayes classifier for the task. In the future, I may implement other models / methodologies. This algorithm is currently 86% accurate (for tech roles found on Indeed).

## classify.py

Classify is a mini flask app that takes in a job description as input and then outputs found text relating to skills section.

## utils.py

Common methods used across the repo. parse_sentences transforms job descriptions into tokenised 'sentence-like' pieces; preprocessing does all that nlp magic: tokenising, lowercasing, filtering, removing stopwords, lematising.
