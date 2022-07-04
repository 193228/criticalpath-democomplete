import json

import pandas as pd
import pandas.io.json
from pandas.io.json import json_normalize


def readJson():
    # Opening JSON file
    f = open('./config/materias_ids_v2.json', encoding="utf8")

    # returns JSON object as
    # a dictionary
    data = json.load(f)

    f.close()

    df2 = pandas.json_normalize(data)

    for index, materia in df2.iterrows():
        print(materia['relacionMateria'])

def getCriticalPath():
    print("")

if __name__ == '__main__':
    readJson()