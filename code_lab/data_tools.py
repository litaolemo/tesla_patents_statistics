# -*- coding:utf-8 -*-
# @author :litao
# @Time :2023/6/5 12:20
from bs4 import BeautifulSoup
def split_data(r):
    if not r:
        return "",""
    res_list = []
    res = r.text.split("\n")
    for index,r in enumerate(res):
        r=r.strip()
        if index < 7:
            continue
        if not r:
            continue
        if "-" in r:
            if r[4] == "-":
                continue
        if len(r) >=2:
            res_list.append(r)

    if len(res_list) == 2:
        return res_list[0],res_list[1]
    elif len(res_list) == 1:
        print(res_list)
        if "Ind" in res_list[0] or " Co" in res_list[0] or "Ltd" in res_list[0] or len(res_list[0]) <=20:
            return res_list[0],""
        else:
            return "",res_list[0]
    elif len(res_list) == 0:
        print(res_list)
        return "",""


def parse_data(res_data_text,patent_Citations,key,row):
    bf = BeautifulSoup(res_data_text,'html.parser')
    res_div = bf.find('div',class_='tr style-scope patent-result')
    soup = BeautifulSoup(res_data_text,'html.parser')
    res = soup.find_all("tr")
    n = 0
    for r in res:
        if r.attrs:
            if r.attrs.get("itemprop") in ["backwardReferencesOrig", "forwardReferences", "backwardReferencesFamily","backwardReferences","forwardReferencesFamily"]:
                p_num = r.text.split("\n")[3]
                patent_Citations[key][p_num] = dict(row)
                if "backward" in r.attrs.get("itemprop"):
                    cite_type = "backward"
                else:
                    cite_type = "forward"
                patent_Citations[key][p_num]["cite_type"] = cite_type
                Assignee,Title = split_data(r)
                # print(Assignee,Title)
                patent_Citations[key][p_num]["Assignee"] = Assignee
                patent_Citations[key][p_num]["Assignee_Title"] = Title

                n += 1
    print("total ",n," citations")
    return patent_Citations

import pandas as pd


def save_res(patent_Citations,file_name):
    output_list = []
    for key in patent_Citations:
        for key2 in patent_Citations[key]:
            output_list.append([key,key2,patent_Citations[key][key2]["priority_date"],patent_Citations[key][key2]["publication_date"],patent_Citations[key][key2].get("Assignee",""),patent_Citations[key][key2].get("Assignee_Title",""),patent_Citations[key][key2]["cite_type"],patent_Citations[key][key2]["assignee"],patent_Citations[key][key2]["snippet"]])

    data_pd = pd.DataFrame(output_list,columns=["Patent number","Cited by","Priority date","Publication date","Assignee","Title","cite_type","From","snippet"])
    data_pd.to_excel(file_name)