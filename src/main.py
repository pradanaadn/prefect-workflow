from typing import Annotated
import asyncio
import json

from prefect import flow, task
from dependency_injector.wiring import inject, Provide
from src.container import AppContainer
from src.config import Config
from prefect.blocks.webhook import Webhook

webhook_block = Webhook.load("test-webhook")


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


@task
async def send_webhook(data):
    print("Sending webhook...")
    payload = {
        "content": "This is a test message from a webhook!",
        "username": "My Webhook Bot",
        "avatar_url": "https://avatars.githubusercontent.com/u/96559846?v=4",
        "embeds": [
            {
                "title": "Important Update",
                "description": "Here's some detailed information.",
                "color": 16711680,
                "fields": [
                    {"name": "Status", "value": "Operational", "inline": True},
                    {"name": "Version", "value": "1.0.0", "inline": True},
                    {
                        "name": "Data",
                        "value": json.dumps(data, indent=4),
                        "inline": False,
                    },
                ],
                "footer": {"text": "Powered by ExampleApp"},
            }
        ],
    }
    await webhook_block.call(payload)


@flow
async def simple_etl_flow():
    print("Starting ETL flow...")
    data = extract()
    transformed = transform(data)
    load(transformed)
    await send_webhook(transformed)
    print("ETL flow completed!")


if __name__ == "__main__":
    container = AppContainer()
    container.wire(modules=[__name__])
    asyncio.run(simple_etl_flow())
