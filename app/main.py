import asyncio
import os
import sys

import mlflow
import mlflow.pyfunc
import numpy as np
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from mlflow import MlflowClient
from mlflow.exceptions import MlflowException
from pydantic import BaseModel


class PredictRequest(BaseModel):
    features: list[float]


class PredictResponse(BaseModel):
    prediction: list[float]
    model_name: str
    model_version: str
    alias: str


class HealthResponse(BaseModel):
    status: str
    tracking_uri: str
    model_name: str
    model_version: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: load @champion model
    tracking_uri = os.environ.get("MLFLOW_TRACKING_URI")
    model_name = os.environ.get("MODEL_NAME")

    if not tracking_uri:
        print("ERROR: MLFLOW_TRACKING_URI environment variable is not set.", file=sys.stderr)
        print("Set it with: export MLFLOW_TRACKING_URI=http://localhost:5000", file=sys.stderr)
        sys.exit(1)

    if not model_name:
        print("ERROR: MODEL_NAME environment variable is not set.", file=sys.stderr)
        print("Set it with: export MODEL_NAME=IrisClassifier", file=sys.stderr)
        sys.exit(1)

    mlflow.set_tracking_uri(tracking_uri)
    client = MlflowClient()

    try:
        mv = client.get_model_version_by_alias(model_name, "champion")
    except MlflowException as e:
        print(f"ERROR: Failed to get @champion alias for model '{model_name}': {e}", file=sys.stderr)
        print("Make sure the MLflow server is running and the model has a @champion alias.", file=sys.stderr)
        sys.exit(1)

    try:
        app.state.model = mlflow.pyfunc.load_model(f"models:/{model_name}@champion")
        app.state.model_version = mv.version
        app.state.model_name = model_name
        app.state.tracking_uri = tracking_uri
        print(f"Loaded model '{model_name}' version {mv.version} (@champion)")
    except Exception as e:
        print(f"ERROR: Failed to load model: {e}", file=sys.stderr)
        sys.exit(1)

    yield
    # Shutdown: cleanup (if needed)


app = FastAPI(
    title="MLflow Champion Model API",
    description="Serves the @champion model from MLflow Model Registry",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Check service health and loaded model info."""
    return HealthResponse(
        status="ok",
        tracking_uri=app.state.tracking_uri,
        model_name=app.state.model_name,
        model_version=app.state.model_version,
    )


@app.post("/predict", response_model=PredictResponse)
async def predict(req: PredictRequest) -> PredictResponse:
    """Run inference using the loaded @champion model."""
    model = app.state.model
    features = np.array(req.features).reshape(1, -1)
    # Use asyncio.to_thread to avoid blocking the event loop with sync model.predict
    prediction = await asyncio.to_thread(model.predict, features)
    return PredictResponse(
        prediction=prediction.tolist(),
        model_name=app.state.model_name,
        model_version=app.state.model_version,
        alias="champion",
    )
