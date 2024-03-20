import json
import os


async def create_json(name):
    if not os.path.isdir("jsons/"):
        raise ValueError(f"Указанный каталог не существует")

    count = sum([1 for file in os.listdir("jsons") if os.path.isfile(os.path.join("jsons", file))])

    filename = f"jsons/tasks_{count}.json"

    json_dict = {
        "tasks": {},
        "other": {}
    }

    json_str = json.dumps(json_dict)

    # Сохраняем строку JSON в файл
    with open(filename, "w") as f:
        f.write(json_str)


async def add_tasks(*tasks, filename):
    with open(filename) as js:
        json_dict = json.load(js)
    count = len(json_dict["tasks"])
    temp_dict = json_dict["tasks"]
    for task in tasks:
        temp_dict[count + 1] = f"{task}"

    json_dict["tasks"] = temp_dict
    json_str = json.dumps(json_dict)

    with open(filename, "w") as f:
        f.write(json_str)
