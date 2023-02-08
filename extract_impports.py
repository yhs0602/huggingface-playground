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
            for alias in node.names:
                module = alias.name
                refer_name = alias.asname if alias.asname else alias.name
                if module in sys.builtin_module_names:
                    imported_functions[refer_name] = ("built-in", module)
                else:
                    imported_functions[refer_name] = ("external", module)
        elif isinstance(node, ast.ImportFrom):
            module = node.module
            for name in node.names:
                if name.name == "*":
                    # import statement with wildcard, so we can't determine the imported functions
                    break
                refer_name = name.asname if name.asname else name.name
                if module in sys.builtin_module_names:
                    imported_functions[refer_name] = ("built-in", module)
                else:
                    # imported_functions[f"{refer_name}.{name.name}"] = f"{module}"
                    imported_functions[refer_name] = (module, module)

        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                # print(type(node.func.value))
                if isinstance(node.func.value, ast.Name):
                    # print(f"{node.func.value.id} is an attribute")
                    module = node.func.value.id
                    if module in imported_functions:
                        # print("Moudle in imported functions")
                        func_source = (imported_functions[module], "imported")
                    else:
                        # print("Module not in imported functions or attributes")
                        func_source = (module, "variable")
                    function_calls.append((f"{module}.{node.func.attr}", func_source))
                elif isinstance(node.func.value, ast.Call):
                    # print(f"{node.func.value} is a call")
                    function_calls.append(
                        (f"{node.func.value}.{node.func.attr}", "unknown")
                    )
            elif isinstance(node.func, ast.Name):
                # print(f"{node.func.id} is a name")
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


def process_one_file(file):
    print("Processing file: ", file)
    functions, calls = get_imported_functions_and_calls2(file)
    print(functions)
    print(calls)
    print("=========================================")
    usage_list = []
    for call in calls:
        if not call[1][1] == "imported":
            continue
        if call[1][0] == "external":
            first_part, other = call[0].split(".", maxsplit=1)
            print(f"from {first_part} use {other}")
            usage_list.append((first_part, other))
        else:
            print(f"from {call[1][0]} use {call[0]}")
            usage_list.append((call[1][0], call[0]))
    print(usage_list)


if __name__ == "__main__":
    # process_one_file("foo_to_flowchart.py")
    # process_one_file("test_import.py")
    # process_one_file("foobarbaz.py")
    # process_one_file("foo.py")
    # process_one_file("extract_impports.py")
    process_one_file("panda_import_test.py")
