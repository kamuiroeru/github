#文字コード順でソートするプログラム

import sys,glob,MeCab,string,copy,time
from os.path import basename

from collections import defaultdict
dicTF = defaultdict(int)
dicIDF = defaultdict(int)
dicTemp = defaultdict(int)
doc_total = 0
word_total = 0

label = []
documents = []
start_MeCab = time.time()
for loop in glob.glob("./*.txt"):
    n = int(sys.argv[1])
    doc_total += 1
    sentence = ""
    with open(basename(loop), encoding = "utf-8") as a_file:
        sentence += "".join([arg1.strip() for arg1 in a_file])
    print(basename(loop))

    dic_eachTF = defaultdict(int)
    t = MeCab.Tagger("-F %f[6]\\n")
    lists = []
    for words in t.parse(sentence).split("\n"):
        if (words == "" or words == "EOS"):
            continue
        lists.append(words)

    dicTemp = copy.deepcopy(dicTF)
    i = 0
    lis_len = len(lists)
    for i in range(lis_len - n + 1):
        dicTF["-".join(lists[i:i+n])] += 1
        dic_eachTF["-".join(lists[i:i+n])] += 1
        word_total += 1

    for i,j in dicTF.items():
        if dicTemp[i] != j:
            dicIDF[i] += 1

    label.append(str(basename(loop).strip(".txt")))
    documents.append(dic_eachTF)
end_MeCab = time.time()

from math import log2
print("dicTF= " + str(len(dicTF)))
print("dicIDF=" + str(len(dicIDF)))

print("〜ファイル書き出し中〜")
start = time.time()
for loop in range(0, doc_total):
    with open("../out/" + str(label[loop]) + ".txt", "w") as f:
        seikika = 0.0
        w = 0.0
        for i,j in sorted(documents[loop].items()):
            w = j/word_total * (log2(doc_total/dicIDF[i]) + 1)
            f.write("{:20}\t{}\t{}\t{}\n".format(i,j,dicIDF[i],w))
print("処理時間" + "{0}".format(end_MeCab - start_MeCab) + "[sec]")
print("書込時間" + "{0}".format(time.time() - start) + "[sec]")
print("〜完了〜")
