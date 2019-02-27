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


if __name__ == '__main__':
    data = pd.read_csv(data_clean.PATH_TREATEDDATA)

    u.clean_folder(s.PATH_VIEWS)

    view_n_songs(data)
    view_n_styles(data)
