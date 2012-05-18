REPO_BOOL_OPTIONS = ('private', 'has_issues', 'has_wiki', 'has_downloads')

class Repo(object):

    def __init__(self, **kw):
        self.__dict__.update(kw)

    def __repr__(self):
        return '<Repo "%s">' % self.name

    def __str__(self):
        return self.__repr__()

    def dumps(self):
        return self.__dict__
