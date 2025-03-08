import logging
import os
from datetime import datetime
from typing import List
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, split
import pyarrow as pa
import pyarrow.parquet as pq

# Configure logging
logging.basicConfig(level=logging.INFO)

def create_spark_session() -> SparkSession:
    """Creates and returns a Spark session."""
    return SparkSession.builder.appName("NewsProcessor").getOrCreate()

def process_data(target_words: List[str], output_dir: str) -> None:
    """
    Process AG News dataset using PySpark.

    :param target_words: List of words to filter and count.
    :param output_dir: Directory to save processed data.
    """
    # Create Spark session
    spark = create_spark_session()

    # Load dataset from JSONL file
    df = spark.read.json("dataset/test.jsonl")
    # df.show(5, truncate=False)

    # Extract words from "description"
    df_words = df.select("description").withColumn("word", explode(split(col("description"), r"\s+")))

    # Filter and count target words
    df_filtered = df_words.filter(col("word").isin(target_words))
    df_count = df_filtered.groupBy("word").count()

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    today = datetime.today().strftime("%Y%m%d")

    if df_count.count() > 0:
        df_count_pd = df_count.toPandas()
        table = pa.Table.from_pandas(df_count_pd)
        pq.write_table(table, f"{output_dir}/word_count_{today}.parq")
        print(f"Parquet file saved at {output_dir}")
    else:
        print("No data to write!")

    # Read the Parquet file into an Arrow Table
    table = pq.read_table( f"{output_dir}/word_count_{today}.parq")

    # Convert the Arrow Table to a Pandas DataFrame
    df_output = table.to_pandas()

    print("Process Data: ",df_output)

    logging.info("Processing complete.")

