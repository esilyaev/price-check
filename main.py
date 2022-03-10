#!/usr/bin/python3
# -*- coding: utf-8 -*-


from datetime import datetime
from parsers import mc_ru
# from parsers import mkm_metal
from parsers import agrupp
from parsers import mcena_ru
from database.db import Db
from yaspin import yaspin


def main():

    parser_list = [
        agrupp.main,  # return bad html
        mc_ru.main,
        # mkm_metal.main,
        mcena_ru.main
    ]

    db = Db()

    counter_of_parsers = 1

    for parser in parser_list:
        with yaspin(text=f'Processing parser #{counter_of_parsers} / {len(parser_list)}...', color='cyan') as spinner:

            # if True -> will be request and resave html
            data = parser(refresh=True)

            # print(data)

            db.InsertMany(data)

            spinner.text = 'Completed!'
            spinner.ok('🆗')
            counter_of_parsers += 1


if __name__ == '__main__':
    main()
