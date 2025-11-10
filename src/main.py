from typing import Annotated
from prefect import flow, task
from dependency_injector.wiring import inject, Provide
from src.container import AppContainer
from src.config import Config


@inject
@task
def extract(
    config: Annotated[Config, Provide[AppContainer.config]] = Provide[
        AppContainer.config
    ],
):
    print(f"Extracting data from {config}")
    data = [
        {"product": "apple", "quantity": 3, "price": 0.5},
        {"product": "banana", "quantity": 5, "price": 0.25},
    ]
    print("Data extracted:", data)
    return data


@task
def transform(data):
    print("Transforming data...")
    transformed = []
    for row in data:
        total = row["quantity"] * row["price"]
        transformed.append({**row, "total": total})
    print("Data transformed:", transformed)
    return transformed


@task
def load(data):
    print("Loading data...")
    for row in data:
        print(f"Loaded: {row}")
    print("Data loaded successfully!")


@flow
def simple_etl_flow():
    print("Starting ETL flow...")
    data = extract()
    transformed = transform(data)
    load(transformed)
    print("ETL flow completed!")


if __name__ == "__main__":
    container = AppContainer()
    container.wire(modules=[__name__])
    simple_etl_flow()
