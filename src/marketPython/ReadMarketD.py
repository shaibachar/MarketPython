import pandas as pd
import html5lib
import numpy

from os import listdir
from os.path import isfile, join
from itertools import islice, tee
from datetime import date, datetime
from domain.Tradable import Tradable


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
        onlyfiles = [join(filePath, f) for f in listdir(
            filePath) if isfile(join(filePath, f))]
        return onlyfiles

    def readData(self, filePath):
        try:
            dataDate = self.get_file_realDate(filePath)
            df = pd.read_csv(filePath,
                             skiprows=3, encoding='iso8859_8')
            df['day'] = dataDate
            df.set_index(["day", "מס' ני\"ע"])
            # df = df.loc[:, ["day", "מס' ני\"ע", "מחיר קניה", "מחיר פדיון"]]
            # df = df.dropna()
            return df
        except Exception as e:
            print("error on readcsv:", filePath, e)

    def aggrigate_All_Data(self, folderPath):
        frames = []
        filesList = self.allFiles(folderPath)
        print("fileList:", len(filesList))
        try:
            count = 0
            for i in range(len(filesList)):
                frames.append(self.readData(filesList[i]))
                count = count + 1
        except Exception as e:
            print("error while reading file:", e)

        return pd.concat(frames, sort=False)

    def export_to_csv(self, folderPath):
        frames = self.aggrigate_All_Data(folderPath)
        frames.to_csv('../aggrigate.csv')

    def aggrigate_All_Data_in_tradables(self, csv_file_path):
        df = pd.read_csv(csv_file_path)
        tradables = []
        for index, row in df.iterrows():
            tradableId = row["מס' ני\"ע"]
            bid = row["מחיר קניה"]
            ask = row["מחיר פדיון"]
            date = row["day"]

            t = Tradable(tradableId, bid, ask, 0, 0, date)
            tradables.append(t)

        return tradables

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False


# rmd = ReadMarketData()
# # data = rmd.readData('../resources/Data_20180408.csv')
# # print(data)
# data = rmd.aggrigate_All_Data_in_tradables('../aggrigate.csv')
# print("data size:",len(data))
# # rmd.export_to_csv('../resources/')
