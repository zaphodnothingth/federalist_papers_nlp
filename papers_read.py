with open('C:\\Users\\astevens.ALIONSCIENCE\\Downloads\\federalist_all.txt', 'r') as file:
    papers = re.sub(r'\n\s*', ' ', file.read())
    
content_str = papers.split('The Federalist Papers')[3].split('End of the Project Gutenberg EBook of')[0]
papers_df = pd.DataFrame(
    re.findall('''
    FEDERALIST.? No.\s+  # Header
    (?P<no>\d+)  # federalist no.
    (?P<title>[\s\S]*?)(?=From)  # title is everything before 'from' which starts publication
    (?P<pulication>[\s\S]*?)(?=\.)  # publication is everything up to the period
    (?P<body>[\s\S]*?)(?=FEDERALIST|\Z)  # body is everything till the next header or the end of the string
    '''
    , content_str))
