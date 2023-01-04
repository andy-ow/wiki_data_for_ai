from wiki_data_for_ai import get_wiki

if __name__ == '__main__':
    df = get_wiki('Podatki',
                  title_filter=lambda title: any([x in title.lower() for x in ['podatek', 'podatki', 'podatkowe', 'podatkowa']]),
                  verbose=True)
    df.to_csv('podatki.csv')

