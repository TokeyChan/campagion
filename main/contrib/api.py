
def calc_statistics(dict_):
    ecpm = calc_ecpm(dict_)
    ctr = calc_ctr(dict_)
    ecpc = calc_ecpc(dict_)
    dict_['ecpm'] = float(round(ecpm, 4)) if ecpm is not None else None
    dict_['ctr'] = float(round(ctr, 4)) if ctr is not None else None
    dict_['ecpc'] = float(round(ecpc, 4)) if ecpc is not None else None
    return dict_

def calc_ecpm(dict_):
    try:
        return (dict_['revenue'] / dict_['impressions']) * 1000
    except:
        return None

def calc_ctr(dict_):
    try:
        return (dict_['clicks'] / dict_['impressions']) * 100
    except:
        return None

def calc_ecpc(dict_):
    try:
        return dict_['revenue'] / dict_['clicks']
    except TypeError:
        return None