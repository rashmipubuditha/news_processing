import logging
import os
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, split
import pyarrow as pa
import pyarrow.parquet as pq

# Configure logging
logging.basicConfig(level=logging.INFO)
logging.info("Pipeline execution started: process_data_all.py")

def create_spark_session() -> SparkSession:
    """Creates and returns a Spark session."""
    return SparkSession.builder.appName("NewsProcessorAll").getOrCreate()

def process_data_all(output_dir: str) -> None:
    """
    Process the AG News dataset using PySpark and count all unique words.
    """
    # Create Spark session
    spark = create_spark_session()

    # Load dataset from JSONL file
    df = spark.read.json("dataset/test.jsonl")
    # df.show(5, truncate=False) 

    # Extract words from "description"
    df_words = df.select("description").withColumn("word", explode(split(col("description"), r"\s+")))

    # Count all unique words
    df_all_count = df_words.groupBy("word").count()

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save the Output files

    today = datetime.today().strftime("%Y%m%d")

    if df_all_count.count() > 0:
        df_all_count_pd = df_all_count.toPandas()
        table = pa.Table.from_pandas(df_all_count_pd)
        pq.write_table(table, f"{output_dir}/word_count_all_{today}.parq")
        print(f"Parquet file saved at {output_dir}")
    else:
        print("No data to write!")

    # Testing

    # Read the Parquet file into an Arrow Table
    table = pq.read_table(f"{output_dir}/word_count_all_{today}.parq")

    # Convert the Arrow Table to a Pandas DataFrame
    df_output = table.to_pandas()
    print(f"Print process all data by reading the word_count_all_{today}.parq file: ")
    print(df_output)

    logging.info("Processing complete.")
