
from datetime import datetime
import os
from pathlib import Path
import subprocess
import sys

from airflow.sdk import dag, task


PROJECT_DIR = Path(
    os.getenv("TELESCOPE_PROJECT_DIR", "/opt/airflow/telescope_project")
)


@dag(
    dag_id="telecom_offers_transformation",
    start_date=datetime(2026, 11, 24),
    schedule=None,
    catchup=False,
    tags=["telecom", "transformation"],
)
def telecom_offers_transformation():

    @task
    def run_transformation():

        subprocess.run(
            [
                sys.executable,
                "-m",
                "src.data_transformation.offers_transformation",
            ],
            cwd=PROJECT_DIR,
            check=True,
        )

    run_transformation()


telecom_offers_transformation()
