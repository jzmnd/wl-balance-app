# -*- coding: utf-8 -*-
"""
codeslib.py
Library for code tables

Created by Jeremy Smith on 2017-10-04
"""

import os
import pandas as pd


FEATURES = ['TEAGE', 'TESEX', 'GEMETSTA', 'GESTFIPS',
            'TELFS', 'TRDPFTPT',
            'TRSPPRES', 'TESPEMPNOT',
            'TESCHENR', 'TESCHLVL', 'PEEDUCA',
            'PTDTRACE',
            'TRCHILDNUM', 'TRNUMHOU',
            'TRMJOCGR', 'TRDTOCC1',
            'TRMJIND1', 'TEIO1COW', 'TRERNWA',
            'TUDIS']

CATFEATURES = ['GEMETSTA', 'GESTFIPS',
               'TELFS', 'TRDPFTPT',
               'TRSPPRES', 'TESPEMPNOT',
               'TESCHENR', 'TESCHLVL',
               'PTDTRACE',
               'TRMJOCGR', 'TRDTOCC1',
               'TRMJIND1', 'TEIO1COW',
               'TUDIS']

NUMCATS = [4, 57, 6, 3, 4, 3, 3, 3, 27, 7, 23, 14, 9, 4]


def load_codes(loc, loc_codes="code_tables"):

    # Import activity code dictionary csv to df
    dfactcodes = pd.read_csv(os.path.join(loc, loc_codes, "activity_codes.csv"),
                             index_col=False,
                             sep=';',
                             dtype={'CODE': str, 'NAME': str})

    # Import short names and merge
    defactshrt = pd.read_csv(os.path.join(loc, loc_codes, "activity_codes_short.csv"),
                             index_col=False,
                             sep=';',
                             dtype={'CODE': str, 'SHORTNAME': str})
    
    dfactcodes = dfactcodes.merge(defactshrt, how='outer', on='CODE')

    # Add codepoint level (1, 2 or 3) and sort
    dfactcodes['LEVEL'] = dfactcodes.CODE.str.len() / 2
    dfactcodes = dfactcodes.sort_values('CODE').reset_index(drop=True)

    # Import education level code dictionary csv to df
    dfeducodes = pd.read_csv(os.path.join(loc, loc_codes, "edu_codes.csv"),
                             index_col=False,
                             sep=';',
                             dtype={'CODE': str, 'NAME': str})

    # Import income level code dictionary csv to df
    dfinccodes = pd.read_csv(os.path.join(loc, loc_codes, "inc_codes.csv"),
                             index_col=False,
                             sep=';',
                             dtype={'CODE': str, 'NAME': str})

    # Import age code dictionary csv to df
    dfagecodes = pd.read_csv(os.path.join(loc, loc_codes, "age_codes.csv"),
                             index_col=False,
                             sep=';',
                             dtype={'CODE': str, 'NAME': str})

    # Import employment status code dictionary csv to df
    dfempcodes = pd.read_csv(os.path.join(loc, loc_codes, "employ_codes.csv"),
                             index_col=False,
                             sep=';',
                             dtype={'CODE': str, 'NAME': str})

    # Import industry and occupation code dictionary csv to df
    dfindcodes = pd.read_csv(os.path.join(loc, loc_codes, "indocc_codes.csv"),
                             index_col=False,
                             sep=';',
                             dtype={'FLAG': str, 'CODE': str, 'NAME': str})

    # Import race code dictionary csv to df
    dfraccodes = pd.read_csv(os.path.join(loc, loc_codes, "race_codes.csv"),
                             index_col=False,
                             sep=';',
                             dtype={'CODE': str, 'NAME': str, 'NAME2012': str})

    # Import location (state) code dictionary csv to df
    dfloccodes = pd.read_csv(os.path.join(loc, loc_codes, "state_codes.csv"),
                             index_col=False,
                             sep=';',
                             dtype={'CODE': str, 'NAME': str})

    # Import "who activity is performed with" code dictionary csv to df
    dfwhocodes = pd.read_csv(os.path.join(loc, loc_codes, "who_codes.csv"),
                             index_col=False,
                             sep=';',
                             dtype={'CODE': str, 'NAME': str})

    # Import input codes
    dfdemocodes = pd.read_csv(os.path.join(loc, loc_codes, "demographic_codes.csv"),
                              index_col=False,
                              sep=';',
                              dtype={'CODE': str, 'NAME': str})

    return [dfactcodes, dfeducodes, dfinccodes, dfagecodes, dfempcodes,
            dfindcodes, dfraccodes, dfloccodes, dfwhocodes, dfdemocodes]


# Create code dictionaries
dfactcodes, dfeducodes, dfinccodes, dfagecodes, dfempcodes, \
    dfindcodes, dfraccodes, dfloccodes, dfwhocodes, dfdemocodes = load_codes("app/static/data")

CODEDICTS = {}
CODEDICTS['ptdtrace'] = [{'name': n, 'value': v} for n, v in zip(dfraccodes.NAME.tolist()[:-5], dfraccodes.CODE.tolist()[:-5])]
CODEDICTS['gestfips'] = [{'name': n, 'value': v} for n, v in zip(dfloccodes.NAME.tolist(), dfloccodes.CODE.tolist())]
CODEDICTS['telfs'] =    [{'name': n, 'value': v} for n, v in zip(dfempcodes.NAME.tolist(), dfempcodes.CODE.tolist())]
CODEDICTS['trdtocc1'] = [{'name': n, 'value': v} for n, v in zip(dfindcodes[dfindcodes.FLAG == 'TRDTOCC1'].NAME.tolist(),
                                                                 dfindcodes[dfindcodes.FLAG == 'TRDTOCC1'].CODE.tolist())]
CODEDICTS['teio1cow'] = [{'name': n, 'value': v} for n, v in zip(dfindcodes[dfindcodes.FLAG == 'TEIO1COW'].NAME.tolist(),
                                                                 dfindcodes[dfindcodes.FLAG == 'TEIO1COW'].CODE.tolist())]
CODEDICTS['peeduca'] = [ {'name': n, 'value': v} for n, v in zip(dfeducodes.NAME.tolist(), dfeducodes.CODE.tolist())]
