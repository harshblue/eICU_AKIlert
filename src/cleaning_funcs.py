def lab_process(df):
    df.columns = ['patientunitstayid', 'labname', 'min_result', 'max_result', 'delta_result']
    df.set_index(['patientunitstayid', 'labname'], inplace=True)
    df = df.unstack(level=1)
    df.columns = df.columns.map('_'.join)
    return df

def vital_process(df, day):
    df.columns = ['patientunitstayid','min_sao2', 'max_sao2', 'mean_sao2', 'min_heartrate', 'max_heartrate', \
                       'mean_heartrate', 'min_respiration', 'max_respiration', 'mean_respiration']
    df['days_of_data'] = day
    df.set_index('patientunitstayid', inplace=True)
    return df

def fluid_process(df, day, label):
    df.columns = ['patientunitstayid', 'ave_hourly_intake', 'ave_hourly_output', 'ave_hourly_dialysis', 'ave_hourly_nettotal']
    df['days_of_data'] = day
    df.set_index('patientunitstayid', inplace=True)
    if label == 'negative':
        df = df[df['ave_hourly_dialysis']==0]
    return df

def merge_filter(lab_df, vital_df):
    combined_df = vital_df.merge(lab_df, left_index=True, right_index=True)
    #combined_df = combined_df.merge(fluid_df, left_index=True, right_index=True)
    return combined_df, combined_df.index.tolist()

def filter_nextday_patients(lab_df, vital_df, index):
    lab_df = lab_df.reset_index()
    lab_df = lab_df[~(lab_df['patientunitstayid'].isin(index))]
    lab_df.set_index('patientunitstayid', inplace=True)
    vital_df = vital_df.reset_index()
    vital_df = vital_df[~(vital_df['patientunitstayid'].isin(index))]
    vital_df.set_index('patientunitstayid', inplace=True)
    #fluid_df = fluid_df.reset_index()
    #fluid_df = fluid_df[~(fluid_df['patientunitstayid'].isin(index))]
    #fluid_df.set_index('patientunitstayid', inplace=True)
    return lab_df, vital_df