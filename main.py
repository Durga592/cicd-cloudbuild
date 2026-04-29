from google.cloud import bigquery
from flask import Flask
import os

app = Flask(__name__)
client = bigquery.Client()


@app.route("/")
def main(big_query_client=client):
    """
    Docstring for main
    
    :param big_query_client: Description
    """
    table_id = "mlops-1-494812.test_schema.us_states"
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
    )
    uri = "gs://sidd-ml-ops-new/us-states.csv"
    load_job = big_query_client.load_table_from_uri(
        uri, table_id, job_config=job_config
    )

    load_job.result()

    destination_table = big_query_client.get_table(table_id)
    return {"data": destination_table.num_rows}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5052)))
