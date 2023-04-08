"""
Duncan's new multiple range test
-----------------------------------
This is a simple implementation of Duncan's new multiple range test for multiple comparison.
Author: Zell Wu
Date: 4/7/2023
"""

import pandas as pd
import numpy as np
import string


def dmrt(values, sd, rp, no_digits=2):
    """ Duncan's new multiple range test
    Input:
        values: The values from different treatments (do not need to be sorted).
        sd: The standard error of the mean difference.
        rp: The values of significant studentized ranges obtained from table.
        no_digits: The number of digits after the dot.
    Output:
        A table with MRT alphabetical notation.
    """
    # set critical values
    Rp = [round(i * sd, no_digits) for i in rp]
    # sort
    sorted_values = sorted(values, reverse=True)
    # comparison
    res = []
    done = False
    for i in range(0, len(sorted_values) - 1):
        # loop quit if we has searched all elements
        if done:
            break
        temp = [i + 1]
        # loop
        for j in range(i + 1, len(sorted_values)):
            # Calculate the difference between two values
            diff = sorted_values[i] - sorted_values[j]
            rp = Rp[j - i - 1]
            # Compare difference to critical value
            if diff <= rp:
                # j+1 is no significant different with i+1
                temp.append(j + 1)
                # there are no significant differences between i+1 and the end
                if j == len(sorted_values) - 1:
                    res.append(temp)
                    done = True
                    break
            else:
                # duplication e.g. [3,4,5] [4,5]
                if res and i != len(sorted_values) - 2 and j == res[-1][-1]:
                    break
                # comparison between the last two elements, so add the last element into the end individually
                if i == len(sorted_values) - 2 and j == len(sorted_values) - 1:
                    res.append([j + 1])
                    done = True
                    break
                # normal condition: there are significant differences between i+1 and j+1
                res.append(temp)
                break
    return res


if __name__ == "__main__":

    values = [24.33, 20.00, 20.00, 17.67, 21.67, 20.67, 20.00]
    sd = 0.665
    # You can change the p_value below by commenting and uncommenting
    rp = [4.320, 4.504, 4.622, 4.705, 4.767, 4.815]  # p_value=0.01
    # rp = [3.081, 3.225, 3.312, 3.370, 3.410, 3.439]   # p_value=0.05

    res = dmrt(values, sd, rp)
    print(res)

    show_df = pd.DataFrame(data={'Clone': ['A1', 'A5', 'A6', 'A2', 'A3', 'A7', 'A4'],
                                 'Mean': [24.33, 21.67, 20.67, 20.00, 20.00, 20.00, 17.67]})
    ordinal = 0
    for lst in res:
        show_df[ordinal] = [''] * len(values)
        for i in lst:
            show_df[ordinal][i - 1] = '|'
        ordinal += 1
    show_df['Group'] = [''] * len(values)

    for i in range(show_df.shape[0]):
        for j in range(ordinal):
            if show_df[j][i] == '|':
                show_df['Group'][i] += list(string.ascii_lowercase)[j]

    print(show_df)
