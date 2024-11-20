from fastapi import APIRouter, HTTPException, Depends, Query
from google.cloud import bigquery
from ..utils.validate_user import verify_firebase_token


import logging


client = bigquery.Client()


# Replace with your BigQuery project ID, dataset ID, and table ID
PROJECT_ID = "augusta-edge-project"
DATASET_ID = "test"
TABLE_ID = "tabla_test"


router = APIRouter(
  #prefix="/load-image",
  #ags=["Load Image"]
)

@router.post("/query")
async def post_query(limit: int = Query(100, le=1000), offset: int = 0, where_clause: str = Query(None, description="Optional WHERE clause (parameterized)"), user: dict = Depends(verify_firebase_token)):
    try:
        query = f"SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`"
        if where_clause:
            query = f"{query} WHERE {where_clause}" # Vulnerable, needs parameterization

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                # ... other parameters
                bigquery.ScalarQueryParameter("limit", "INT64", limit),
                bigquery.ScalarQueryParameter("offset", "INT64", offset)
            ]
        )

        query_job = client.query(query, job_config=job_config)
        data_results = query_job.result()
        data_return = [dict(row) for row in data_results]
        return(data_return)
    except ValueError as e:
        logging.exception("Input data validation failed: %s", e)
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logging.exception("An unexpected error occurred: %s", e)
        raise HTTPException(status_code=500, detail="Internal Server Error") from e
