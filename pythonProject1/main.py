import os
import os.path
import re


def print_files_to_console(files):
    for file in files:
        print(file)


def make_concatenated_file(files, path):
    concatenated_file = open(path, "w")
    for file in files:
        reader = open(file["path"], "r", encoding="utf8")
        for line in reader:
            concatenated_file.write(line)
        else:
            concatenated_file.write("\n")
        reader.close()
    concatenated_file.close()


def get_name_of_file(file):
    return file["name"]


def get_path_of_file(file):
    return file["path"]


def sort_files_by_parameter(files, parameter):
    files.sort(key=parameter)


def sort_files_by_name(files):
    sort_files_by_parameter(files, get_name_of_file)


def sort_files_by_path(files):
    sort_files_by_parameter(files, get_path_of_file)


def add_unique(list_, item_):
    for item in list_:
        if item["path"] == item_["path"]:
            break
    else:
        list_.append(dict(path=item_["path"], name=item_["name"]))


def check_for_emptiness(list_):
    list_is_empty = True
    if not list_:
        return list_is_empty
    for item in list_:
        if item.get("path"):
            list_is_empty = False
            break
    return list_is_empty


def pop_not_empty(list_):
    for item in list_:
        if item.get("path"):
            return item


def item_in_list_by_path(list_, path):
    for item in list_:
        if not item.get("path"):
            continue
        if item["path"] == path:
            return True
    else:
        return False


def count_items_in_list_by_path(list_, path):
    count = 0
    for item in list_:
        if not item.get("path"):
            continue
        if item["path"] == path:
            count += 1
    return count


def pop_by_path(list_, path):
    for item in list_:
        if not item.get("path"):
            continue
        if item["path"] == path:
            return item
    else:
        return False


def pop_item_by_requirements(list_, item, paths):
    if item.get("require"):
        paths.append(item["path"])
        if item["require"] not in paths:
            if item_in_list_by_path(list_, item["require"]):
                next_item = pop_by_path(list_, item["require"])
                return pop_item_by_requirements(list_, next_item, paths)
            else:
                return item
        else:
            paths.append(item["require"])
            return dict(item="Loop Error. Loop: ", loop=paths)


def pop_list_by_requirements(list_):
    item_ = pop_not_empty(list_)
    sorted_list = []
    while not check_for_emptiness(list_):
        path_list = []
        item = pop_item_by_requirements(list_, item_, path_list)
        if item.get("loop"):
            print(item["item"])
            for path in item["loop"]:
                print(path + " -> ")
            else:
                print("...")
            return False
        else:
            if count_items_in_list_by_path(list_, item["path"]) == 1:
                add_unique(sorted_list, item)
            item.clear()
        item_ = pop_not_empty(list_)
    return sorted_list


def sort_files_by_requirements(files):
    link_list = []
    no_req_list = []
    file_has_requirements = False
    for file in files:
        reader = open(file["path"], "r", encoding="utf8")
        for line in reader:
            for requirement in re.findall(r"require \'[^\']*\'", line):
                if requirement:
                    link_list.append(dict(path=file["path"], require=requirement[9:-1:], name=file["name"]))
                    file_has_requirements = True
        reader.close()
        if not file_has_requirements:
            no_req_list.append(file)
        file_has_requirements = False
    sorted_link_list = pop_list_by_requirements(link_list)
    if sorted_link_list:
        no_req_list.extend(sorted_link_list)
    files.clear()
    files.extend(no_req_list)


def scan_dir_and_sub_dirs_for_text_files(path):
    cur_dir = path
    sub_dirs = []
    text_files = []
    dir_contents = os.listdir(cur_dir)
    for content in dir_contents:
        if os.path.isdir(cur_dir + "\\" + content):
            sub_dirs.append(cur_dir + "\\" + content)
        elif content.endswith(".txt"):
            text_files.append(dict(path=(cur_dir + "\\" + content), name=content))
    for sub_dir in sub_dirs:
        text_files.extend(scan_dir_and_sub_dirs_for_text_files(sub_dir))
    return text_files


def output_for_sorting_by_name_of_file(files, path):
    sort_files_by_name(files)
    make_concatenated_file(files, path)


def output_for_sorting_by_requirements(files, path):
    sort_files_by_requirements(files)
    make_concatenated_file(files, path)


root_dir = "D:\\PycharmProjects\\testsProject1"
paths_to_concatenated_files = ["D:\\PycharmProjects\\testsResultsProject1\\concatenated_by_name.txt",
                               "D:\\PycharmProjects\\testsResultsProject1\\concatenated_by_requirements.txt"]
txt_files = scan_dir_and_sub_dirs_for_text_files(root_dir)

print("Unsorted")
print_files_to_console(txt_files)

output_for_sorting_by_name_of_file(txt_files, paths_to_concatenated_files[0])

print("Sorted by name")
print_files_to_console(txt_files)

output_for_sorting_by_requirements(txt_files, paths_to_concatenated_files[1])

print("Sorted by requirements")
print_files_to_console(txt_files)
