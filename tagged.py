"""
-----------------------------------------------------------------------
tagged.py
-----------------------------------------------------------------------

Creating a csv of each sentence with reference to the document it came
from and the classification of that sentence.
"""
import glob
import json
import pandas as pd

files = glob.glob("out/*")

dfs = []
for file in files:
    with open(file, "r") as f:
        data = json.load(f)
        rows = []
        # iterate over sentences in document and check whether they're in
        # the "segment" section from the tagger app.
        for i, sentence_i in enumerate(data["sentences"]):
            for j, sentence_j in enumerate(data["segment"]):
                # in the very rare circumstance that two parsed sentences are the same
                # check that the next (or previous) sentence is the same on both sets
                # to minimize duplicates.
                if sentence_i == sentence_j:
                    try:
                        if data["sentences"][i+1] == data["segment"][j+1]:
                            rows.append(
                                {
                                    "document": file,
                                    "sentence": sentence_i,
                                    "label": 1
                                }
                            )
                            break
                    except IndexError:
                        try:
                            if data["sentences"][i-1] == data["segment"][j-1]:
                                rows.append(
                                {
                                    "document": file,
                                    "sentence": sentence_i,
                                    "label": 1
                                })
                                break
                        except IndexError:
                            break
            else:
                rows.append(
                    {
                    "document": file,
                    "sentence": sentence_i,
                    "label": 0
                    }
                )
        dfs.append(pd.DataFrame(rows))
    
df = pd.concat(dfs)
df.to_csv("data.csv")