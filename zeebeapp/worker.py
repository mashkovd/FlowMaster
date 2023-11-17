from logging import getLogger

from pyzeebe import Job, ZeebeWorker, create_insecure_channel

from settings import settings

grpc_channel = create_insecure_channel(
    hostname=settings.ZEEBE_ADDRESS,
    port=settings.ZEEBE_PORT,
)
worker = ZeebeWorker(grpc_channel)
logger = getLogger(__name__)


async def on_error(exception: Exception, job: Job):
    """
    on_error will be called when the task fails
    """
    logger.warning("ZEEBE worker is stopping")
    await job.set_error_status(f"Failed to handle job {job}. Error: {str(exception)}")


@worker.task(task_type="example", exception_handler=on_error)
def example_task(source: str) -> dict:
    n = int(source)
    n_pow = n**2
    logger.info({"output": f"Hello world, {n_pow}!"})
    return {"value": f"Hello world, {n_pow}!"}
