
import pandas as pd
import numpy as np


# ### Recency FUNCTION INSIDE SOME FUNCTION
def heuristics(dtf, cutoff, sfassetr, blocks):

    list_df = np.array_split(dtf, blocks)
    for i in range(0, blocks):
        list_df[i].dropna(inplace=True)
        list_df[i].reset_index(drop=True, inplace=True)
        for j in list_df[i]['eq_capgain']:
            if j > cutoff:
                cr = list_df[i]['eq_capgain'][list_df[i]
                                              ['eq_capgain'] == j].index.values
                # print(cr[0])
                fwd = cr + 1
                # print(fwd[0])
                ivalue = list_df[i].iloc[cr[0], 3]
                # print(ivalue)
                rr = list_df[i].iloc[fwd[0], 2]
                # print(rr)
                g = (ivalue) * (1 + rr)
                # print(g)
                list_df[i].iloc[fwd[0], 3] = g
                if fwd[0] == len(list_df[i]) - 1:
                    break
            if j < cutoff:
                cr = list_df[i]['eq_capgain'][list_df[i]
                                              ['eq_capgain'] == j].index.values
                # print(cr[0])
                fwd = cr + 1
                # print(fwd[0])
                ivalue = list_df[i].iloc[cr[0], 3]
                # print(ivalue)
                z = (ivalue) * (1 + sfassetr)
                # print(z)
                list_df[i].iloc[fwd[0], 3] = z
                if fwd[0] == len(list_df[i]) - 1:
                    break
    # # check
    # list_df[0]
    # list_df[12]
    # list_df[3]

    # ### 60/40 Part of the FUNCTION INSIDE SOME FUNCTION
    for i in range(0, blocks):
        for j in list_df[i]['eq_capgain']:
            cr = list_df[i]['eq_capgain'][list_df[i]
                                          ['eq_capgain'] == j].index.values
            # print(cr[0])
            fwd = cr + 1
            # print(fwd[0])
            ivalue = list_df[i].iloc[cr[0], 4]
            # print(ivalue)
            rr = list_df[i].iloc[fwd[0], 2]
            # print(rr)
            sixty = (0.60 * ivalue) * (1 + rr)
            # print(sixty)
            forty = (0.40 * ivalue) * (1 + sfassetr)
            # print(forty)
            res = sixty + forty
            list_df[i].iloc[fwd[0], 4] = res
            if fwd[0] == len(list_df[i]) - 1:
                break
    # # check
    # list_df[0]
    # list_df[3]
    # list_df[12]

    # ### 100% Stocks Part of the FUNCTION INSIDE SOME FUNCTION
    for i in range(0, blocks):
        for j in list_df[i]['eq_capgain']:
            cr = list_df[i]['eq_capgain'][list_df[i]
                                          ['eq_capgain'] == j].index.values
            # print(cr[0])
            fwd = cr + 1
            # print(fwd[0])
            ivalue = list_df[i].iloc[cr[0], 5]
            # print(ivalue)
            res = ivalue * (1 + j)
            list_df[i].iloc[fwd[0], 5] = res
            if fwd[0] == len(list_df[i]) - 1:
                break
    # # check
    # list_df[0]
    # list_df[3]
    # list_df[12]

    # ### 2 down out Part of the FUNCTION INSIDE SOME FUNCTION
    list_of_js = {elem: [] for elem in range(0, blocks)}
    for i in range(0, blocks):
        for j in list_df[i]['eq_capgain']:
            list_of_js[i].append(j)

    for i in range(0, blocks):
        res = list(zip(list_of_js[i], list_of_js[i][1:]))
        for x, y in res:
            if x < cutoff and y < cutoff:
                cx = list_df[i]['eq_capgain'][list_df[i]
                                              ['eq_capgain'] == x].index.values
                # print(cj[0])
                fwd = cx + 1
                # print(fwd[0])
                ivalue = list_df[i].iloc[cx[0], 6]
                res = ivalue * (1 + sfassetr)
                list_df[i].iloc[fwd[0], 6] = res

                if fwd[0] == len(list_df[i]) - 1:
                    break
            else:
                cx = list_df[i]['eq_capgain'][list_df[i]
                                              ['eq_capgain'] == x].index.values
                # print(cj[0])
                fwd = cx + 1
                # print(fwd[0])
                ivalue = list_df[i].iloc[cx[0], 6]
                ave = (x + y) / 2
                res = ivalue * (1 + ave)
                list_df[i].iloc[fwd[0], 6] = res
                if fwd[0] == len(list_df[i]) - 1:
                    break

    # # check
    # list_df[0]
    # list_df[3]
    # list_df[12]

    # ### Naive Part of the FUNCTION INSIDE SOME FUNCTION
    for i in range(0, blocks):
        for j in list_df[i]['eq_capgain']:
            if j < cutoff:
                cr = list_df[i]['eq_capgain'][list_df[i]
                                              ['eq_capgain'] == j].index.values
                # print(cr[0])
                fwd = cr + 1
                # print(fwd[0])
                ivalue = list_df[i].iloc[cr[0], 7]
                # print(ivalue)
                rr = list_df[i].iloc[fwd[0], 2]
                # print(rr)
                g = (ivalue) * (1 + rr)
                # print(g)
                list_df[i].iloc[fwd[0], 7] = g
                if fwd[0] == len(list_df[i]) - 1:
                    break
            if j > cutoff:
                cr = list_df[i]['eq_capgain'][list_df[i]
                                              ['eq_capgain'] == j].index.values
                # print(cr[0])
                fwd = cr + 1
                # print(fwd[0])
                ivalue = list_df[i].iloc[cr[0], 7]
                # print(ivalue)
                z = (ivalue) * (1 + sfassetr)
                # print(z)
                list_df[i].iloc[fwd[0], 7] = z
                if fwd[0] == len(list_df[i]) - 1:
                    break
    # check
    # list_df[0]
    # list_df[3]
    # list_df[12]

    # ### Recency 2 of the FUNCTION INSIDE SOME FUNCTION
    for i in range(0, blocks):
        for j in list_df[i]['eq_capgain']:
            if j < sfassetr:
                # print('below')
                pos = list_df[i]['eq_capgain'][list_df[i]
                                               ['eq_capgain'] == j].index.values
                # print(pos[0])
                fwd = pos + 1
                # print(fwd[0])
                ivalue = list_df[i].iloc[pos[0], 8]
                # print(ivalue)
                z = (ivalue) * (1 + 0.025)
                # print(z)
                list_df[i].iloc[fwd[0], 8] = z
                if fwd[0] == len(list_df[i]) - 1:
                    break
            if j >= sfassetr:
                # print('above')
                cr = list_df[i]['eq_capgain'][list_df[i]
                                              ['eq_capgain'] == j].index.values
                # print(cr[0])
                fwd = cr + 1
                # print(fwd[0])
                ivalue = list_df[i].iloc[cr[0], 8]
                # print(ivalue)
                rr = list_df[i].iloc[fwd[0], 2]
                # print(rr)
                g = (ivalue) * (1 + rr)
                # print(g)
                list_df[i].iloc[fwd[0], 8] = g
                if fwd[0] == len(list_df[i]) - 1:
                    break

    finaldf = pd.concat(list_df)
    return finaldf
