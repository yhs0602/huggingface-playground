import _ast
import ast
from typing import List

from pyflowchart import Flowchart
from pyflowchart import ast_node


def iterate_fields_from_ast(ast_obj: _ast.AST, context: str = "") -> List[_ast.AST]:
    result = []
    for (
        ao
    ) in (
        ast_obj.body
    ):  # raises AttributeError: ast_obj along the field path has no body
        if hasattr(ao, "name"):
            result.append(context + "." + ao.name)
            result.extend(iterate_fields_from_ast(ao, context + "." + ao.name))
    return result


def find_field_from_ast(ast_obj: _ast.AST, field: str) -> _ast.AST:
    """Find a field from AST.

    This function finds the given `field` in `ast_obj.body`, return the found AST object
    or an `_ast.AST` object whose body attribute is [].
    Specially, if field="", returns `ast_obj`.

    A field is the *path* to a `def` code block in code (i.e. a `FunctionDef` object in AST). E.g.

    ```
    def foo():
        pass

    class Bar():
        def fuzz(self):
            pass
        def buzz(self, f):
            def g(self):
                f(self)
            return g(self)

    Bar().buzz(foo)
    ```

    Available path:

    - "" (means the whole ast_obj)
    - "foo"
    - "Bar.fuzz"
    - "Bar.buzz"
    - "Bar.buzz.g"

    Args:
        ast_obj: given AST
        field: path to a `def`

    Returns: an _ast.AST object
    """
    if field == "":
        return ast_obj

    field_list = field.split(".")
    try:
        for fd in field_list:
            for (
                ao
            ) in (
                ast_obj.body
            ):  # raises AttributeError: ast_obj along the field path has no body
                if hasattr(ao, "name") and ao.name == fd:
                    ast_obj = ao
        assert ast_obj.name == field_list[-1], "field not found"
    except (AttributeError, AssertionError):
        ast_obj.body = []

    return ast_obj


def my_flowchart(code, field, inner=True, simplify=True, conds_align=False):
    code_ast = ast.parse(code)

    result = iterate_fields_from_ast(code_ast)
    print(result)
    field_ast = find_field_from_ast(code_ast, field)

    assert hasattr(field_ast, "body")
    assert (
        field_ast.body
    ), f"{field}: nothing to parse. Check given code and field please."

    f = field_ast.body if inner else [field_ast]
    p = ast_node.parse(f, simplify=simplify, conds_align=conds_align)
    return Flowchart(p.head)


if __name__ == "__main__":
    # read the code from a file
    with open("foobarbaz.py") as f:
        code = f.read()

    print(code)
    fc = my_flowchart(code, field="", inner=True)
    print(fc)
    print(fc.flowchart())
