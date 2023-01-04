from typing import Callable

import nltk
import wikipedia
from pandas import DataFrame

from wiki_data_for_ai.extract_from_wikipedia import find_all_pages
from wiki_data_for_ai.sections import extract_sections

nltk.download('punkt', quiet=True)
def get_wiki(title: str = '2020 Summer Olympics',
             title_filter: Callable[[str], bool] = lambda title: '2020' in title and 'olympi' in title.lower(),
             verbose=False,
             language='en') \
        -> DataFrame:
    """
    Recursively find all the pages that are linked to the Wikipedia title, divide into sections,
    and create a title / heading / content / tokens dataframe.
    :param language: wikipedia language version. Default is English 'en'
    :param verbose:
    :param title: str, Wikipedia title
    :param title_filter: callable, receives title, returns bool. A wikipedia page will only be processed when title_filter(title) returns true
    :return: pandas.DataFrame
    """
    res = []
    wikipedia.set_lang(language)
    pages = find_all_pages(title, title_filter, verbose)
    for page in pages:
        res += extract_sections(page.content, page.title)
    df = DataFrame(res, columns=["title", "heading", "content", "tokens"])
    df = df[df.tokens > 40]
    df = df.drop_duplicates(['title', 'heading'])
    df = df.reset_index().drop('index', axis=1)  # reset index
    return df
