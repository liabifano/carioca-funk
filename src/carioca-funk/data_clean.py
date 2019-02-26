import os
import json
import pandas as pd

from datetime import datetime

from string import punctuation
from nltk.tokenize import word_tokenize

import settings as s

PATH_SONGS = os.path.join(s.PATH_DATA, 'songs.txt')
PATH_SINGERS = os.path.join(s.PATH_DATA, 'singers.txt')
PATH_POPULARITY = os.path.join(s.PATH_DATA, 'popularity.txt')

PATH_TREATEDDATA = os.path.join(s.PATH_DATA, 'data.csv')


def read(path):
    with open(path, "r") as ins:
        r = []
        for line in ins:
            r.append(json.loads(line))

    return r


LOOKUP_MONTHS = {'Janeiro': 1, 'Fevereiro': 2, 'Março': 3, 'Abril': 4, 'Maio': 5,
                 'Junho': 6, 'Julho': 7, 'Agosto': 8, 'Setembro': 9, 'Outubro': 10,
                 'Novembro': 11, 'Dezembro': 12}

def fix_date(x):
    split = x.split(' ')
    month = LOOKUP_MONTHS.get(split[0])
    year = int(split[-1])

    return datetime(year, month, 1)

def clean_lyrics(s):
    return [w.lower()
            for w in sum([word_tokenize(l)
                          for l in s], [])
            if w not in punctuation and w.isalpha()]



if __name__ == '__main__':
    all_songs = pd.DataFrame(read(PATH_SONGS))
    singers = pd.DataFrame(read(PATH_SINGERS))
    popularity = pd.DataFrame(read(PATH_POPULARITY))

    popularity['date'] = popularity.year.apply(fix_date)


    all_songs['styles'] = (all_songs.details
                       .apply(lambda x: [s['descr'] for s in x['style']])
                       .apply(lambda x: list(set(['Funk Carioca' if s=='Funk' else s for s in x]))))
    songs = all_songs[all_songs.styles.apply(lambda x: 'Funk Carioca' in x)]
    songs['lyrics_ok'] = all_songs.lyrics.apply(clean_lyrics)
    songs['singer_id'] = songs.details.apply(lambda x: x['discus_url'].split('/')[1])

    singers = singers[singers.song_names.apply(lambda x: x!=[])]
    singers['singer_id'] = singers.photo_url.str.split('/').apply(lambda x: x[3])

    data = songs.merge(singers).merge(popularity)

    print('Dataset shape: {}'.format(str(data.shape)))
    print('Dataset is here: {}'.format(PATH_TREATEDDATA))

    data.to_csv(PATH_TREATEDDATA, index=False)
