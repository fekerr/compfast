def print_interpreter_versions(data):
    version_info_lines = [
        "\nInterpreter                     Version Info",
        "===========                     ============"
    ]
    for index, item in enumerate(data, start=1):
        line = f"{index:2}. {item['Interpreter']:<25} {item['Version']}"
        print(line)
        version_info_lines.append(line)
    return version_info_lines

def print_runtimes(data):
    runtime_info_lines = [
        "\nRuntimes (seconds, #K loops):",
        "============================="
    ]
    for index, item in enumerate(data, start=1):
        line = f"{index}. {item['First Runtime (s)']:.3f}, {item['Second Runtime (s)']:.3f} ({item['Estimated Iterations (K)']}K); {item['Loop Runtime (s)']:.3f}, {item['Loop Runtime (s)']:.3f} ({item['Estimated Iterations (K)']}K)"
        print(line)
        runtime_info_lines.append(line)
    return runtime_info_lines

def print_paths(paths_list):
    path_info_lines = [
        "\nPaths:",
        "====="
    ]
    for index, path in enumerate(paths_list, start=1):
        line = f"{index}. {path}"
        print(line)
        path_info_lines.append(line)
    return path_info_lines

