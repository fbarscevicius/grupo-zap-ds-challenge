from pandas import DataFrame
from typing import Any

def download_json(url: str, path: str, filename: str) -> None:
    '''
    Automates JSON extraction from Grupo Zap raw data zipfiles,
    saving the result inside the path provided
    
    Args:
        url (str): url to get the zip from
        path (str): directory where to save the data
        filename (str): name of the resulting JSON (will concatenate with '.json')
    '''
    
    import os
    import errno
    from urllib import request
    from zipfile import ZipFile
    
    try:
        os.makedirs(path)
        
    except OSError as err:
        if err.errno != errno.EEXIST:
            raise
    
    req  = request.urlopen(url)
    data = req.read()

    with open(path + filename + '.zip', 'wb') as f:       
        f.write(data)
        
    dir_state = os.listdir(path)
    
    with ZipFile(path + filename + '.zip', 'r') as _zip:
        _zip.extractall(path)
        
    extracted = [name for name in os.listdir(path) if name not in dir_state][0]
    
    os.rename(path + extracted, path + filename + '.json')
    os.remove(path + filename + '.zip')
    
    
def parse_json(path: str, verbose: bool = True) -> DataFrame:
    '''
    Converts a nested JSON file to a pd.DataFrame
    
    Args:
        path (str): path to json file
        verbose (bool): toogles loading percentage
        
    Returns:
        <pandas DataFrame>
    '''
    
    import json
    import pandas as pd
    from IPython.display import clear_output

    out = []
    with open(path) as f:
        document = []

        for line in f:
            document.append(line)

        ttl = len(document)
        i   = 1    
        for record in document:
            clear_output(wait=True)

            parse       = json.loads(record)
            df_unnested = pd.io.json.json_normalize(parse, sep='_')
            out.append(df_unnested)
            
            if verbose:
                print(f'Loading {path}: {round((i / ttl) * 100, 2)}%')
                i += 1

    return pd.concat(out, ignore_index=True, copy=False, sort=False)


def pkl_io(path: str, method: str='load', file: Any=None) -> Any:
    '''
    Convenient wrapper around `pickle` module to load or dump a .pkl file
    
    Args:
        path (str): path to pkl file
        method (str): operation to perform 'load' | 'dump'        
        file (any pickable): file to export when dumping
        
    Returns:
        loaded pickle file if method=='load'
    '''
    
    import os
    import errno
    import pickle as pkl
    
    if method == 'load':
        with open(path, 'rb') as f:
            data = pkl.load(f)

        return data
    
    else:
        if not file: 
            raise TypeError('`file` can not be None when method != "load"')
        
        # Extract directory from filename and assert it exists:
        dirs = os.path.split(path)[0]        
        try:
            os.makedirs(dirs)
        
        except OSError as err:
            if err.errno != errno.EEXIST:
                raise
        
        with open(path, 'wb') as f:
            pkl.dump(f, file)