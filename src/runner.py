import time
import sys
import os
import pandas
import pandas as pd
from pathlib import Path

def read_csv(file_path: str ):
    df  = pd.read_csv(file_path)
    return df

def process_data(df: pandas.DataFrame):
    count_df = df.groupby(["personal_training"]).size()
    return count_df

def write_status_data(df:pd.DataFrame) -> bool:
    try:
        df.to_csv('output.csv', index=True)
        return True
    except Exception as e:
        print(e)
        return False


def get_file_path(env: str, file_name: str ) -> str :
    root_file_path = ""
    if "local" in env.lower() :
        # if we are running from the Src Folder
        root_file_path = Path.cwd().parent
    if "dev" in env.lower() :
        print(Path.cwd())
        # if we are running from the Src Folder
        root_file_path = "/app"
    if "qa" in env.lower():
        root_file_path = "bucket_Name"

    file_path = f"{root_file_path}/data/input/{file_name}"

    return file_path
def main():
    if len(sys.argv) > 1:
        print("parsing the Input Arguments")
        env = os.getenv("ENV" , "dev")
        file_name = sys.argv[1]
    else:
        print("No Arguments were provided")
        sys.exit(1)
    print(" Hellow World ........")
    print(" Hellow World ........")

    file_path = get_file_path(env, file_name)

    source_df = read_csv(file_path)
    count_df = process_data(source_df)
    print(count_df)
    status = write_status_data(count_df)
    if status:
        print("Status Written")
    else:
        sys.exit(2)





if __name__ == "__main__":
    main()

