import pandas as pd
import html5lib

from os import listdir
from os.path import isfile, join
from itertools import islice, tee
from datetime import date, datetime


class ReadMarketData(object):
    """
    This Class will load all csv market Data and aggrigate them in to a one DataFrame
    """
    def __init__(self):
        pass

    def get_file_realDate(self, filePath):
        with open(filePath, 'r') as infile:
            lines_gen = islice(infile, 3)
            i = 0
            for line in lines_gen:
                if (i == 1):
                    fileDate = datetime.strptime(
                        line.replace('*', '').strip(), '%d/%m/%Y')
                    return fileDate
                i = i+1

    def allFiles(self, filePath):
        onlyfiles = [join(filePath, f) for f in listdir(filePath) if isfile(join(filePath, f))]
        return onlyfiles

    def readData(self, filePath):
        try:
            dataDate = self.get_file_realDate(filePath)
            df = pd.read_csv(filePath,
                             skiprows=3, encoding='iso8859_8')
            df['day'] = dataDate
            df.set_index(["day", "מס' ני\"ע"])
            df = df.loc[:, ["day", "מס' ני\"ע", "מחיר קניה", "מחיר פדיון"]]
            return df
        except Exception as e:
            print("error on readcsv:", filePath, e)

    def aggrigate_All_Data(self, folderPath):
        frames = []
        for filePath in self.allFiles(folderPath):
            frames.append(self.readData(filePath))
        return pd.concat(frames)