import asyncio
from temporalio.worker import Worker
from temporalio.client import Client
from .workflows import ImageRequestWorkflow
from .activities import update_request_status

async def main():
    
    # connect to temporal server
    client = await Client.connect("temporal:7233")  # default server address of temporal

    worker = Worker(
        client,
        task_queue="image-request-task-queue",
        workflows=[ImageRequestWorkflow],
        activities=[update_request_status]
    )

    print("worker is running")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())