import _ast
import ast
from typing import Dict
from functools import partial

from pyflowchart import Flowchart
from pyflowchart import ast_node


def iterate_fields_from_ast(
    ast_obj: _ast.AST, context: str = ""
) -> Dict[str, _ast.AST]:
    result = {}
    for ao in ast_obj.body:
        if hasattr(ao, "name"):
            result[context + "." + ao.name] = ao
            result.update(iterate_fields_from_ast(ao, context + "." + ao.name))
    return result


def field_ast_to_flowchart(
    field_ast: _ast.AST, inner, simplify, conds_align
) -> Flowchart:
    assert hasattr(field_ast, "body")
    assert field_ast.body, f"nothing to parse. Check given code and field please."

    f = field_ast.body if inner else [field_ast]
    p = ast_node.parse(f, simplify=simplify, conds_align=conds_align)
    return Flowchart(p.head)


def my_flowchart(code, inner=True, simplify=True, conds_align=False):
    code_ast = ast.parse(code)

    field_ast = iterate_fields_from_ast(code_ast)
    mapped = map(
        partial(
            field_ast_to_flowchart,
            inner=inner,
            simplify=simplify,
            conds_align=conds_align,
        ),
        field_ast.values(),
    )
    for flowchart in mapped:
        print(flowchart.flowchart())


if __name__ == "__main__":
    # read the code from a file
    with open("foobarbaz.py") as f:
        code = f.read()

    print(code)
    fc = my_flowchart(code, inner=True)
