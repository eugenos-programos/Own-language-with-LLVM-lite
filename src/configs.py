import json 



if __name__ == '__main__':
    dict_ = {
        "MAX_STR_SIZE": 20,
        "MAX_ARR_SIZE": 1000
    }
    with open("src/confs.json", 'w', encoding='utf-8') as conffile:
        json.dump(dict_, conffile)


with open("src/confs.json", 'r', encoding='utf-8') as conffile:
    confs = json.load(conffile)


MAX_STR_SIZE = confs["MAX_STR_SIZE"]
MAX_ARR_SIZE = confs["MAX_ARR_SIZE"]
