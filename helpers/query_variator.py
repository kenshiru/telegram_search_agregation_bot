class QueryVariator:
    def __init__(self, custom_fields=None):
        if custom_fields is not None and type(custom_fields) in (list, tuple, set):
            self._fields = custom_fields
        else:
            self._fields = ('firstname', 'lastname', 'birthday')

        self._info = {}

    def ask_info(self):
        for field in self._fields:
            self._info[field] = input('Type "{field_name}":'.format(field_name=field))

    def get_query(self):
        return " ".join([self._info[field_name] for field_name in self._fields])
