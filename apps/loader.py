from distributed import Client, LocalCluster
from app import app,cache
import os

@cache.memoize()
def data():
    import modin.pandas as pd
    # Dask Local Cluster 
    print("ssssssssssssssssssssssssssssssssss  ",os.getcwd())
    cluster = LocalCluster()
    client = Client(cluster)
    df = pd.read_csv("./dynamic/displaydata.csv",index_col=[0])
    return df

# def main():
#      df =  data()

# if __name__ == '__data__':
#      #import multiprocessing.popen_spawn_win32
#      data()
