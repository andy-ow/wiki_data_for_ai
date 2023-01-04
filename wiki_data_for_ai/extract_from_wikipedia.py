from collections.abc import Callable
from typing import List, Set, Optional

import wikipedia
from wikipedia import WikipediaPage


def __filter_titles(titles: List[str], title_filter: Callable[[str], bool], verbose: bool):
    """
    Get the titles for which title_filter returns true.
    """

    filtered_titles = [title for title in titles if title_filter(title)]
    if verbose:
        print(f'These titles will be ignored: {[t for t in titles if t not in filtered_titles]}.')

    return filtered_titles


def __get_wiki_page(title) -> Optional[WikipediaPage]:
    """
    Get the wikipedia page given a title
    """
    try:
        return wikipedia.page(title)
    except wikipedia.exceptions.DisambiguationError as e:
        return wikipedia.page(e.options[0])
    except wikipedia.exceptions.PageError:
        return None


def __recursively_find_all_pages(titles: List[str],
                                 title_filter: Callable[[str], bool],
                                 verbose: bool,
                                 titles_so_far: Set[str],
                                 ) -> List[WikipediaPage]:
    """
    Recursively find all the pages that are linked to the Wikipedia titles in the list.
    Pages will only be processed and returned if title_filter(page_title) returns true.
    """
    all_pages = []

    titles = list(set(titles) - titles_so_far)
    titles = __filter_titles(titles, title_filter, verbose)
    if verbose:
        print(f'New titles: {len(titles)}\nProcessed titles: {len(titles_so_far)}\n')
    titles_so_far.update(titles)
    for title in titles:
        page = __get_wiki_page(title)
        if page is None:
            continue
        if verbose:
            print(f'Wikipedia page url: {page.url}\n')
        all_pages.append(page)

        new_pages = __recursively_find_all_pages(page.links, title_filter, verbose, titles_so_far)
        for pg in new_pages:
            if pg.title not in [p.title for p in all_pages]:
                all_pages.append(pg)
        titles_so_far.update(page.links)
    return all_pages


def find_all_pages(title: str,
                   title_filter: Callable[[str], bool],
                   verbose: bool = False,
                   ) -> List[WikipediaPage]:
    """
    Recursively find all the pages that are linked to the Wikipedia title.
    :param title: string, title of the start Wikipedia page
    :param title_filter: if title_filter(title) is false, then the title will be ignored.
    :param verbose: bool
    :return: list of Wikipedia pages
    """
    return __recursively_find_all_pages(titles=[title], title_filter=title_filter, verbose=verbose, titles_so_far=set())
