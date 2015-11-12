# debate-parser
Contains Python code to parse debate transcripts, create structured datasets, and generate word clouds from semi-structured debate transcripts

The accompanying articles with the entire output can be found at the following blog post: http://ml4ma.blogspot.com/

The data used for each of the debates are from:
https://www.washingtonpost.com/news/the-fix/

The individual links to each original data source and created datasets are elaborated in the blogposts.

Run the following command:
```
python main.py data/dem_debate1 dem_debate.csv
```
The word clouds are generated in images directory.

Acknowledgements go to nmoya who wrote a whatsapp parser https://github.com/nmoya/whatsapp-parser, which helped me quickly come up with a modified parser for other kinds of semi-structured data.

