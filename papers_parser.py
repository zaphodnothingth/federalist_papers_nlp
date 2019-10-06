import re
import pandas as pd

# merge entire text file & convert line endings + spaces to single line endings
with open('C:\\Users\\astevens.ALIONSCIENCE\\Downloads\\federalist_all.txt', 'r') as file:
    papers = re.sub(r'\n\s*', '\n', file.read())
# remove gutenberg front and end matter
content_str = papers.split('The Federalist Papers')[3].split('End of the Project Gutenberg EBook of')[0]
# divide papers into rows, parse sections into columns
papers_df = pd.DataFrame(re.findall(
    r"""
    FEDERALIST.?\sNo.\s+(?P<no>\d+)             # Find beginning of Paper, record number
    \n(?P<title>[\s\S]*?)(?=\n(?:From|For))     # title is everything up to newline followed by either `For` or `From`
    \n(?P<pulication>[\s\S]*?)(?=\.).           # publication is everything up to a period
    \n(?P<author>[\s\S]*?)(?=\nTo\s)            # author(s) is everything up to `To`
    \n(?P<addressee>[\s\S]*?)(?=[:.])[:.]       # addressee is everything up to a colon
    \n(?P<body>[\s\S]*?)(?=FEDERALIST|\Z)       # everything up to next paper or end of string recorded as body
    """, content_str, re.VERBOSE))
papers_df.rename({0:'no', 1:'title', 2:'publication', 3:'author', 4:'addressee', 5:'body'}, axis=1, inplace=True)
