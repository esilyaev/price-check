#!/usr/bin/python3
# -*- coding: utf-8 -*-


import json
from datetime import datetime
from parsers import mc_ru
# from parsers import mkm_metal
from parsers import agrupp
from database.db import Db


def main():
    """
    Insert new parsers in this list and method main
    be run automatically (must be return list in format:
    {
      'name': Name of product
      'price' : int price
    })
    after get data - save this to json
    """

    parser_list = [
        agrupp.main,  # return bad html
        mc_ru.main,
        # mkm_metal.main,
    ]

    db = Db()

    i = 0

    for parser in parser_list:
        time = datetime.now().strftime("%Y-%m-%d")

        # if True -> will be request and resave html
        data = parser(refresh=False)

        file_name = f"{time}_{i}.json"

        db.InsertMany(data)


if __name__ == '__main__':
    main()
