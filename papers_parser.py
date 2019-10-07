''' notes
reviewing data: for item1, item2 in zip(papers_df.no, papers_df.pulication): print(item1, item2)
TODO:

'''

import re
import pandas as pd

# merge entire text file & convert line endings + spaces to single line endings
with open('./data/federalist_all.txt', 'r') as file:
    papers = re.sub(r'\n\s*', '\n', file.read())
# remove gutenberg front and end matter
content_str = papers.split('The Federalist Papers')[3].split('End of the Project Gutenberg EBook of')[0]
# divide papers into rows, parse sections into columns
papers_df = pd.DataFrame(re.findall(
    r"""
    FEDERALIST.?\sNo.\s+(?P<no>\d+)             # Find beginning of Paper, record number
    \n(?P<title>[\s\S]*?)(?=\n(?:From|For))     # title is everything up to newline followed by either `For` or `From` - required altering no 58 - no pub included
    \n(?P<publication>[\s\S]*?)(?=\.).           # publication is everything up to a period
    \n(?P<author>[\s\S]*?)(?=\nTo\s)            # author(s) is everything up to `To`
    \n(?P<addressee>[\s\S]*?)(?=[:.])[:.]       # addressee is everything up to a colon
    \n(?P<body>[\s\S]*?)(?=FEDERALIST|\Z)       # everything up to next paper or end of string recorded as body
    """, content_str, re.VERBOSE))
papers_df.rename({0:'no', 1:'title', 2:'publication', 3:'author', 4:'addressee', 5:'body'}, axis=1, inplace=True)

for number, text in zip(papers_df.no, papers_df.body): 
    with open('./data/bodies/{}.txt'.format(number), 'w') as writefile:
        writefile.write(text)

# manual counting
manual_terms = ['authority', 'sovereign', 'tyranny', 'liberty', 'union', 'administer', 'confederacy', 'american states', 'federal', 'common interest', 'military', 'government', 'law', 'jealousy', 'coercion', 'political', 'principle', 'principal', 'sufficient', 'equal']
manual_freq_15 = [7, 5, 0, 0, 12, 3, 7, 0, 5, 2, 2, 15, 6, 2, 2, 7, 7, 2, 0, 0]
manual_freq_18 = [6, 3, 4, 3, 6, 4, 12, 1, 6, 0, 0, 8, 5, 3, 1, 2, 1, 1, 1, 4]
manual_df = pd.DataFrame(zip(manual_terms, manual_freq_15, manual_freq_18))
manual_df.rename({0:'Term', 1:'manual_freq_15', 2:'manual_freq_18'}, axis=1, inplace=True)

# readin termine & 5filters results to DFs
termine15 = pd.read_csv('./data/results/15_termine.csv')
termine15['Term'] = termine15['Term'].str.lower()
termine15.rename({'Rank':'15_termine_rank', 'Score':'15_termine_score'}, axis=1, inplace=True)
termine18 = pd.read_csv('./data/results/18_termine.csv')
termine18['Term'] = termine18['Term'].str.lower()
termine18.rename({'Rank':'18_termine_rank', 'Score':'18_termine_score'}, axis=1, inplace=True)
fivefilters15 = pd.read_csv('./data/results/15_5filters.csv')
fivefilters15['Term'] = fivefilters15['Term'].str.lower()
fivefilters15.rename({'Occurrence':'15_5filters_freq', 'Word count':'15_ngram_length'}, axis=1, inplace=True)
fivefilters18 = pd.read_csv('./data/results/18_5filters.csv')
fivefilters18['Term'] = fivefilters18['Term'].str.lower()
fivefilters18.rename({'Occurrence':'18_5filters_freq', 'Word count':'18_ngram_length'}, axis=1, inplace=True)


df_15 = pd.merge(termine15, fivefilters15, on='Term', how='outer')
df_15_inner = pd.merge(termine15, fivefilters15, on='Term', how='inner')
df_18 = pd.merge(termine18, fivefilters18, on='Term', how='outer')
df_18_inner = pd.merge(termine18, fivefilters18, on='Term', how='inner')
df_term_5filt = pd.merge(df_15, df_18, on='Term', how='inner')

df_full = pd.merge(manual_df, df_15, on='Term', how='left')
df_full = pd.merge(df_full, df_18, on='Term', how='left')

df_full.to_csv("./data/results/df_full.csv", index=False)
df_15_inner.to_csv("./data/results/df_15_inner.csv", index=False)
df_18_inner.to_csv("./data/results/df_18_inner.csv", index=False)
