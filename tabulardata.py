def get_col(rows, idx=0, debug=False):
    """Returns a list of values from the column with index idx"""
    col_vals = []
    for row in rows:
        col_vals.append(row[idx])
        if debug:
            print col_vals
    return col_vals

def avg(nums):
    """Returns a single number value that is the average of all
    values in sequence nums."""
    return sum(nums) / len(nums)
