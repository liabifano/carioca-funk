import os
import ast
import pandas as pd
from collections import Counter

import settings as s
import utils as u
import data_clean as data_clean


def view_n_songs(data):
    view = pd.DataFrame(data
                        .groupby(['singer_name', 'photo_url', 'singer_styles', 'date'])
                        .size()
                        .sort_values(ascending=False)
                        .reset_index()
                        .rename(columns={0: 'n_songs'}))

    view.to_csv(os.path.join(s.PATH_VIEWS, 'n_songs.csv'), index=False)


def view_n_styles(data):
    view = (pd.DataFrame([{'style': k, 'count': v}
                          for k,v in Counter(sum(data.styles.apply(ast.literal_eval), [])).items()])
            .sort_values('count', ascending=False)[['style', 'count']])

    view.to_csv(os.path.join(s.PATH_VIEWS, 'n_styles.csv'), index=False)


def view_n_words(data):
    view = []
    for s in data.singer_name.unique():
        filtered = data[data.singer_name == s]
        tops = filtered[filtered.is_top_song] if len(filtered.top_songs.iloc[0]) >=25 else pd.DataFrame()

        d = {'singer_name': s,
             'photo_url': filtered.photo_url.iloc[0],
             'n_songs': len(filtered),
             'n_unique_words': len(set(sum(filtered.lyrics_ok.values, []))),
             'n_unique_words_top25': len(set(sum(tops.lyrics_ok.values, []))) if len(tops)>0 else np.nan}

        view.append(d)

    pd.DataFrame(view).to_csv(os.path.join(s.PATH_VIEWS, 'n_words.csv'), index=False)


if __name__ == '__main__':
    data = pd.read_csv(data_clean.PATH_TREATEDDATA)

    u.clean_folder(s.PATH_VIEWS)

    view_n_songs(data)
    view_n_styles(data)
