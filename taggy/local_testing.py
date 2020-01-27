import os

from taggy import Core

core = Core()
for item in os.listdir(os.path.join('tests','docs')):
    text = open(os.path.join('tests', 'docs', item), 'r').read()
    core.add_document()
    res = wc.count_words(text=text)
    for x in list(res.keys())[:10]:
        print(f'#{x} - {res[x]}'),
    print("===")