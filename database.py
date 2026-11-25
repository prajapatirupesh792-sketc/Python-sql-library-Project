import os
import pandas as pd
from sqlalchemy import  create_engine , text
import urllib


#-- configure you mysql workbench credentials---

DB_USER = "root"
DB_PASSWORD = "Rupesh@7045"
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "campus_db"
CSV_PATH = r"C:\Users\rupes\OneDrive\Desktop\Python And Sql Projects\indian_engineering_placement_2026.csv"


DEFAULT_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{urllib.parse.quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}"
DATABASE_URL = f"{DEFAULT_DATABASE_URL}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

def ensure_database() -> None:
    """ Create the traget database if it does not exist ."""
    default_engine = create_engine(DEFAULT_DATABASE_URL)
    with default_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`"))
    default_engine.dispose()

    global engine
    engine = create_engine(DATABASE_URL)


def init_db(csv_path: str = CSV_PATH):
    """
    Cleans raw CSV data, imputes nulls , and streams into MYSQL .
    """

    #if not os.__path__.exists(csv_path):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"source file ' {csv_path} ' was not found.")

    ensure_database()

    df = pd.read_csv(csv_path)

    # Imputes missing values with medians

    if "Open_Source_Contributions" in df.columns:
        df["Open_Source_Contributions"] = df["Open_Source_Contributions"].fillna(
            df["Open_Source_Contributions"].median()
        )
    if "LinkedIn_Activity_Score" in df.columns:
        df["LinkedIn_Activity_Score"] = df["LinkedIn_Activity_Score"].fillna(
            df["LinkedIn_Activity_Score"].median()
        )

    # Stream into Mysql

    df.to_sql("Students", con=engine, if_exists="replace", index=False)

    # Create indexes in mysql using a safe prefix length string columns.

    with engine.connect() as conn:
        conn.execute(text("ALTER TABLE Students ADD INDEX idx_college_tier (College_Tier(50));"))
        conn.execute(text("ALTER TABLE Students ADD INDEX idx_branch (Branch(50));"))
        conn.execute(text("ALTER TABLE Students ADD INDEX idx_placement_status (Placement_Status(50));"))
        conn.execute(text("ALTER TABLE Students ADD INDEX idx_cgpa (CGPA);"))
        conn.execute(text("ALTER TABLE Students ADD INDEX idx_dsa (DSA_Problems_Solved);"))
        conn.commit()

    print("Data Successfully loaded and indexed in  mysql workbenach!")

def run_query (query: str, params: tuple = ()) -> pd.DataFrame:
    """ 
     
Runs Queries against Mysql using SQLALCHEMY ."""

    with engine.connect() as conn:
        return pd.read_sql_query(text(query), conn, params=params)

if __name__=="__main__":
    init_db()


