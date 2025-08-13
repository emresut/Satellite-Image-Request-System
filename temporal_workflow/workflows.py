from temporalio import workflow
from .activities import update_request_status
from datetime import timedelta

@workflow.defn
class ImageRequestWorkflow:
    @workflow.run
    async def run(self, request_code: str) -> None:

        print(timedelta)
        await workflow.sleep(timedelta(seconds=20)) # 20 seconds

        await workflow.execute_activity(
            update_request_status,
            request_code,
            schedule_to_close_timeout=timedelta(seconds=60)  # 60 seconds, Activity timeout is required
        )