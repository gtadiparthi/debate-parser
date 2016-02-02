# debate-parser
Contains Python code to do the following:
* parse debate transcripts, 
* create structured datasets, 
* generate word clouds from semi-structured debate transcripts,
* score the sentiments of the debate text
* produce a divergent chart for summarizing the sentiments

The accompanying articles with the entire output can be found at the following blog post: http://ml4ma.blogspot.com/

The raw data used for each of the debates are from the following sources:
* https://www.washingtonpost.com/news/the-fix/
* http://www.cbsnews.com/news/transcript-sixth-republican-top-tier-debate-2016/
The individual links to each original data source and created datasets are listed in the blogposts.

Run the following command to get the list of speakers from the raw debate transcript:
```
python get_speakers.py <input raw data> <output csv file>

```

To generate the word clouds run the following command, 

```
python main.py data/dem_debate1 dem_debate.csv
```
The word clouds are generated in images directory.

To generate sentiments using patternanalyzer and naive bayes, use the following command,

```
python combineDebateTranscripts.py
```

Acknowledgements go to nmoya who wrote a whatsapp parser https://github.com/nmoya/whatsapp-parser, which helped me quickly come up with a modified parser for other kinds of semi-structured data.

The divergent chart is inspired by the following chart about fact checking:
http://www.datarevelations.com/all-politicians-lie-some-more-than-others
