import ast
from ast import *
from ipdb import set_trace as st
from macropy.core.macros import Macros
from macropy.core.walkers import Walker
from macropy.core.quotes import macros, q, u, name
import inspect

range2 = lambda x, y: range(x, y)

macros = Macros()

@macros.block
def h(tree, args, expand_macros, **kw):
    
    swaps = {
        Div: q[lambda f, g: f(g)], #application
        BitXor: q[lambda f, g: f(g)], #application
        BitAnd: q[lambda f, g: lambda x: f(g(x))], #composition
    }

    for i, item in enumerate(tree):
        if type(item) is not Expr:
            continue
        
        node = item.value
        if (type(node) is Subscript and type(node.value) is Attribute
            and type(node.value.value) is Name and node.value.value.id == 'L'
            and type(node.slice) is Slice): #multiple args NOT supported yet

            tree[i] = FunctionDef(
                name = node.value.attr,
                args = arguments(
                    args = [Name(id = node.slice.lower.id, ctx = Param())],
                    defaults = [], vararg = None, kwarg = None,
                ),
                body = [Return(value=node.slice.upper)],
                decorator_list = [],
            )
            
    @Walker
    def set2range(tree, **kw):
        if type(tree) is Set and len(tree.elts) == 1:

            if type(tree.elts[0]) is BinOp and type(tree.elts[0].op) is RShift:
                return Call(
                    func = q[range2],
                    args = [tree.elts[0].left, tree.elts[0].right],
                    keywords = []
                )
            else:
                return Call(func = q[range], args = tree.elts, keywords = [])
    
    @Walker
    def swapper(tree, stop, **kw):
        if type(tree) is BinOp:
            for swap_op, lamb in swaps.items():
                if isinstance(tree.op, swap_op):
                    return Call(
                        func = lamb,
                        args = [tree.left, tree.right],
                        keywords = [],
                    )

        elif (args and args[0].id == 'True' and type(tree) is Lambda
              and tree.args.args[0].id[0] == '_'):
            stop() 

    @Walker
    def currier(tree, **kw):
        if type(tree) is Call and not (type(tree.func) is Name and tree.func.id is 'curry'):
            
            curry_node = Call(
                func = q[curry],
                args = [tree.func],
                keywords = [],
            )

            return Call(
                func = curry_node,
                args = tree.args,
                keywords = tree.keywords,
            )

    # we want to run these walkers AFTER quicklambdas are expanded
    # in version < 1.1, order was out -> in
    # in version >= 1.1, order is in -> out
    # however i think there's no harm in calling expand_macros even in newer versions

    tree = expand_macros(tree)
    tree = set2range.recurse(tree)
    tree = swapper.recurse(tree)
    tree = currier.recurse(tree)
    
    return tree

def curry(fn, numargs = None, stack = (), kwds = {}):

    if hasattr(fn, 'curried'): 
        return fn

    if numargs is None:
        if 'builtin' in fn.__class__.__name__ or 'type' in fn.__class__.__name__:
            numargs = get_builtin_num_args(fn)

        else: #not a builtin
            spec = inspect.getargspec(fn)
            assert spec.varargs is None, 'cannot have varargs here'
            assert not stack, 'cannot have initial args for curry'
            numargs = len(spec.args)

    def f(*args, **kwargs):
        newargs = stack + args
        kwds.update(kwargs)
        
        if len(newargs) < numargs:
            return curry(fn, numargs = numargs, stack = newargs, kwds = kwds)
        elif len(newargs) == numargs:
            return fn(*newargs, **kwds)
        else:
            raise Exception('too many args')
        
    f.curried = True 
        
    return f

def get_builtin_num_args(builtin_fn):
    # this is very hacky... parse the docstring
    docstr = builtin_fn.__doc__
    docstr = docstr.split('\n')[0]
    i,j,k = docstr.find('('), docstr.find(')'), docstr.find('[')
    j = j if k == -1 else k
    assert i != -1 and j != -1 and i < j
    return 0 if i+1==j else docstr[i:j].count(',')+1
