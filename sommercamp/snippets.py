# Hier importieren wir die benötigten Softwarebibliotheken.
from os.path import abspath, exists
from sys import argv
from pyterrier import started, init
if not started():
    init()
import pandas as pd
from pyterrier import IndexFactory, apply
from pyterrier.batchretrieve import BatchRetrieve
from pyterrier.terrier import Retriever
from pyterrier.text import get_text, snippets, sliding, scorer

index = IndexFactory.of(abspath("/workspaces/sommercamp/data/index"))

br = Retriever(index, wmodel="BM25",num_results=3)
text_getter = get_text(index, metadata=["text", "url", "title"])

def _fn(iterdict):
    ret = []
    for index, result in iterdict.iterrows():
        result = result.to_dict()
        result["docno"] = str(index)
        ret += [result]
    return pd.DataFrame(ret)

sliding_text = sliding(text_attr="text", prepend_title=False, length=50, stride=25)

snippet_pipeline = br >> text_getter >> apply.generic(_fn)\
    >> sliding_text >> scorer(wmodel="Tf", body_attr="text")

covered_ids = set()
for _, i in snippet_pipeline.search("magnus").sort_values("score", ascending=False).iterrows():
    docno = i["docno"].split("%")[0]
    print(i.keys())
    if docno not in covered_ids:
        print(i["url"], i["score"], i["text"])
        covered_ids.add(docno)