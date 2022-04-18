#!/usr/bin/python3
# -*- coding: utf-8 -*-


from datetime import datetime
from database.db import Db
from yaspin import yaspin


from parsers import abscds
from parsers import partner_lider
from parsers import atlantbeton
from parsers import prom_beton
from parsers import s_paritet
from parsers import betonsnab
from parsers import beton24
from parsers import mc_ru
# from parsers import mkm_metal
from parsers import agrupp
from parsers import mcena_ru


def main():

    parser_list = [
        agrupp.main,  # return bad html
        mc_ru.main,
        # mkm_metal.main,
        mcena_ru.main,

        beton24.main,
        betonsnab.main,
        s_paritet.main,
        atlantbeton.main,
        prom_beton.main,
        partner_lider.main,
        abscds.main,
    ]

    db = Db()

    counter_of_parsers = 1

    for parser in parser_list:
        with yaspin(text=f'Processing parser #{counter_of_parsers} / {len(parser_list)}...', color='cyan') as spinner:
            try:
                # if True -> will be request and resave html
                data = parser(refresh=True)

                # print(data)

                db.InsertMany(data)

                spinner.text = 'Completed!'
                spinner.ok('🆗')

            except:
                print
                spinner.fail('Error!')

            counter_of_parsers += 1


if __name__ == '__main__':
    main()
