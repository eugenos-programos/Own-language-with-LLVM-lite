import json 



if __name__ == '__main__':
    dict_ = {
        "MAX_STR_SIZE": 25
    }
    with open("src/confs.json", 'w', encoding='utf-8') as conffile:
        json.dump(dict_, conffile)


with open("src/confs.json", 'r', encoding='utf-8') as conffile:
    confs = json.load(conffile)


MAX_STR_SIZE = confs["MAX_STR_SIZE"]
