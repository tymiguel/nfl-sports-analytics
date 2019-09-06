import pandas as pd

def filter_df(data_frame, cols_to_keep):
    return data_frame[cols_to_keep].copy()

def update_cols(data_frame, new_col_names):
    data_frame.columns = new_col_names
    return data_frame

def assign_home(data_frame, apply_col, new_col, dct):
    apply_func = lambda x: dct['x'][1] if x == dct['x'][0] else dct['x'][2]
    data_frame[new_col] = data_frame[apply_col].apply(apply_func)
    return data_frame

def create_dummies(data_frame, columns):
    df = pd.DataFrame()

    for col in columns:
        dummies = pd.get_dummies(data_frame[col])
        dummies.columns = [name + col[-2:] for name in dummies.columns]
        df = pd.concat([df, dummies], axis=1)

    combined_df = pd.concat([data_frame, df], axis=1)
    
    return combined_df