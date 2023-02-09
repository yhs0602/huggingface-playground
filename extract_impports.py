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
        # print(node, type(node), node.__dict__)
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
                    imported_functions[refer_name] = (module, refer_name)
        elif isinstance(node, ast.Call):
            full_name = ""
            node = node.func
            while isinstance(node, ast.Attribute):
                full_name = node.attr + "." + full_name
                node = node.value
            if isinstance(node, ast.Name):
                module = node.id
                full_name = full_name.removesuffix(".")
                # print(f"Module: {module}, full_name: {full_name}")
                if module in imported_functions:
                    func_source = (imported_functions[module], "imported")
                else:
                    func_source = (module, "valriable")
                function_calls.append((full_name, func_source))
        elif isinstance(node, ast.FunctionDef):
            defined_vars.add(node.name)

    return imported_functions, function_calls


def process_one_file(file):
    print("Processing file: ", file)
    functions, calls = get_imported_functions_and_calls2(file)
    # print(functions)
    # print(calls)
    print("=========================================")
    usage_list = []
    for call in calls:
        if not call[1][1] == "imported":
            continue
        if call[1][0] == "external":
            first_part, other = call[0].split(".", maxsplit=1)
            # print(f"from {first_part} use {other}")
            usage_list.append((first_part, other))
        else:
            # print(f"from {call[1][0]} use {call[0]}")
            usage_list.append((call[1][0], call[0]))
    print(usage_list)
    for usage in usage_list:
        if usage[0][0] == "external":
            print(f"from {usage[0][1]} use {usage[1]}")
        else:
            print(f"from {usage[0][0]} use {usage[0][1]}.{usage[1]}")


if __name__ == "__main__":
    process_one_file("foo_to_flowchart.py")
    process_one_file("test_import.py")
    process_one_file("foobarbaz.py")
    process_one_file("foo.py")
    process_one_file("extract_impports.py")
    process_one_file("panda_import_test.py")
