import os


def count_lines(file):
    line_count = 0
    with open(file) as f:
        try:
            for _ in f:
                line_count += 1
        except UnicodeDecodeError:
            pass  # TODO: Fix this
    return line_count


def index_dir(root_dir):
    files = []
    for dir_path, _, filenames in os.walk(root_dir):
        if os.path.basename(dir_path)[0] == "." and len(os.path.basename(dir_path)) > 1:
            continue
        print(os.path.basename(dir_path))
        for filename in filenames:
            files.append(os.path.join(dir_path, filename))
    return files


def total_lines(files):
    lines = []
    for file in files:
        line_count = count_lines(file)
        path_split = os.path.splitext(file)
        file_type = (path_split[1] if not path_split[1] == "" else path_split[0])
        duplicate_file_type = False
        if len(lines) > 0:
            for _, result in enumerate(lines):
                if result["file type"] == file_type:
                    result["line count"] = str(line_count + int(line_count))
                    duplicate_file_type = True
        if not duplicate_file_type:
            lines.append({
                "file type": file_type,
                "line count": str(line_count)
            })
    return lines


def print_results(results, root_dir):
    print("Results for /" + root_dir + ":")
    print("File Type | Number of lines")
    print("---------------------------")
    for file in results:
        print(file["file type"] + " | " + file["line count"])


def count_directory(root_dir):
    print_results(total_lines(index_dir(root_dir)), root_dir)


# TODO: Possible other method: create class for a set file type
# TODO: Ignored file types/directories?
count_directory(input("Root directory: "))
