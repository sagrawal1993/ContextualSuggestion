"""
This Module will provide the methods to get the retrieved method.
These method will give the articles given the queries.
We require to pass the data-source as well to get the articles to retrive{Related to the query.}
"""


class AbstractIR:
    def __init__(self, datasource):
        self.datasource = datasource
        pass

    def getArticles(self, query):
        pass