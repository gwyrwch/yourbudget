from json import JSONEncoder


class AutoJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            return obj._json()
        except AttributeError:
            return JSONEncoder.default(self, obj)



