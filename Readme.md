Use Python 3.8.10

Install requirements which are in requirements.txt

pip install -r requirements.txt 

Then move to IRLed_2017/src and run the command

```bash run.bash```

This will clearn the document in the first step

It will train tf-idf model on the cleaned document an vectore the judgments on both judgement and paragraph level

After that with cosine similarity all the document will be ranked using all the methods

Lastly result for all the methods will be printed this might take 1 hour from start to end.
