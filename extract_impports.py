import ast

import sys


def get_dot_separated_parts(string):
    parts = string.split(".")
    result = []
    for i in range(len(parts)):
        result.append(".".join(parts[i:]))
    return result


def get_imported_functions_and_calls2(file):
    with open(file, "r") as f:
        tree = ast.parse(f.read())

    imported_functions = {}
    function_calls = []
    defined_vars = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            module = node.names[0].name
            if module in sys.builtin_module_names:
                imported_functions[module] = "built-in"
            else:
                partial_names = get_dot_separated_parts(module)
                for name in partial_names:
                    imported_functions[name] = module
        elif isinstance(node, ast.ImportFrom):
            module = node.module
            for name in node.names:
                if name.name == "*":
                    # import statement with wildcard, so we can't determine the imported functions
                    break
                if module in sys.builtin_module_names:
                    imported_functions[f"{module}.{name.name}"] = "built-in"
                else:
                    # imported_functions[f"{module}.{name.name}"] = f"{module}"
                    imported_functions[f"{name.name}"] = f"{module}"

        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                print(f"{node.func.value.id} is an attribute")
                module = node.func.value.id
                if module in imported_functions:
                    print("Moudle in imported functions")
                    func_source = (imported_functions[module], "imported")
                else:
                    print("Module not in imported functions or attributes")
                    func_source = (module, "variable")
                function_calls.append((f"{module}.{node.func.attr}", func_source))
            elif isinstance(node.func, ast.Name):
                print(f"{node.func.id} is a name")
                if node.func.id in imported_functions:
                    func_source = (imported_functions[node.func.id], "imported")
                elif node.func.id in defined_vars:
                    func_source = (node.func.id, "local_variable")
                else:
                    func_source = (node.func.id, "variable-or-builtin")
                function_calls.append((f"{node.func.id}", func_source))
        elif isinstance(node, ast.FunctionDef):
            defined_vars.add(node.name)

    return imported_functions, function_calls


if __name__ == "__main__":
    file = "foo_to_flowchart.py"  # replace this with the name of your Python file
    functions, calls = get_imported_functions_and_calls2(file)
    print(functions)
    print(calls)
    print("=========================================")
    for call in calls:
        if not call[1][1] == "imported":
            continue
        print(f"The function '{call[0]}' is imported from '{call[1][0]}'")
