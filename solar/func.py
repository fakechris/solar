# -*- encoding: utf-8 -*-


# http://wiki.apache.org/solr/FunctionQuery/
SOLR_FUNCTIONS = [
    'constant', 'literal', 'field', 'ord', 'rord', 'sum', 'sub', 'product',
    'div', 'pow', 'abs', 'log', 'sqrt', 'map', 'scale', 'query', 'linear',
    'recip', 'max', 'min', 'ms',
    # Math
    'rad', 'deg', 'sqrt', 'cbrt', 'ln', 'exp', 'sin', 'cos', 'tan',
    'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh', 'ceil', 'floor', 'rint',
    'hypo', 'atan2', 'pi', 'e',
    # Relevance - Solr 4.0
    'docfreq', 'termfreq', 'totaltermfreq', 'sumtotaltermfreq', 'idf', 'tf',
    'norm', 'maxdoc', 'numdocs',
    # Boolean - Solr 4.0
    'true', 'false', 'exists', ('if', 'if_'), ('def', 'def_'), ('not', 'not_'),
    ('and', 'and_'), ('or', 'or_'),
    # Distance
    'dist', 'sqedist', 'geodist', 'hsin', 'ghhsin', 'geohash', 'strdist', 'top',
    ]

class Function(object):
    name = None
    
    def __init__(self, *args, **kwargs):
        self.name = self.name or self.__class__.__name__
        self.args = args
        self.weight = kwargs.get('weight')
        self.others = kwargs.get('others', [])

    def __xor__(self, other):
        obj = type(self)(*self.args, weight=other)
        return obj

    def __add__(self, other):
        obj = type(self)(*self.args, weight=self.weight, others=self.others)
        obj.others.append(other)
        return obj
    
    def __str__(self):
        weight = '^%s' % self.weight if self.weight else ''
        parts = []
        parts.append(
            '%s(%s)%s' % (
                self.name,
                ','.join(unicode(a) for a in self.args),
                weight
                )
            )
        for other in self.others:
            parts.append(str(other))
        return ' '.join(parts)

def function_factory(cls_name, name):
    return type(cls_name, (Function,), {'name': name})
    
for _func_name in SOLR_FUNCTIONS:
    if isinstance(_func_name, tuple):
        _name, _cls_name  = _func_name
    else:
        _name, _cls_name = _func_name, _func_name
    globals()[_cls_name] = function_factory(_cls_name, _name)
