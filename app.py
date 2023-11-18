import logging

# from logging.handlers import RotatingFileHandler

import faust
from aiokafka.helpers import create_ssl_context

# from faust.app.base import BootStrategy
from faust.types.auth import SASLMechanism
from mode import Service

from settings import settings
from zeebeapp.client import run_process

# logging.basicConfig(
#     handlers=[
#         RotatingFileHandler(
#             filename="logs.txt", mode="w", maxBytes=512000, backupCount=4
#         )
#     ],
#     level=logging.INFO,
#     format="%(levelname)s %(asctime)s %(message)s",
#     datefmt="%m/%d/%Y%I:%M:%S %p",
# )

logger = logging.getLogger(__name__)

broker_credentials = faust.SASLCredentials(
    mechanism=SASLMechanism.SCRAM_SHA_256,
    ssl_context=create_ssl_context(),
    username=settings.CLOUDKAFKA_USERNAME,
    password=settings.CLOUDKAFKA_PASSWORD,
)


class App(faust.App):
    # producer_only = True
    autodiscover = True


app = App(
    settings.KAFKA_APP_NAME,
    broker=settings.CLOUDKAFKA_BROKERS,
    broker_credentials=broker_credentials,
    group_id=settings.KAFKA_GROUP_ID,
    value_serializer=settings.KAFKA_VALUE_SERIALIZER,
)


topic = app.topic(settings.KAFKA_DEFAULT_TOPIC)


@app.agent(topic)
async def process(messages):
    logger.info(f'Processing messages from topic "{settings.KAFKA_DEFAULT_TOPIC}"')
    async for message in messages:
        logger.info(f"Message: {message}")
        await run_process(
            bpmn_process_id=message["bpmn_process_id"], variables=message["variables"]
        )


@app.service
class ZeebeWorker(Service):
    async def on_start(self):
        logger.info(
            f"ZEEBE worker is starting {settings.ZEEBE_ADDRESS}:{settings.ZEEBE_PORT}"
        )

    async def on_stop(self):
        logger.info("ZEEBE worker is stopping")

    @Service.task
    async def _background_task(self):
        while not self.should_stop:
            try:
                logger.info(
                    f"ZEEBE worker is starting {settings.ZEEBE_ADDRESS}:{settings.ZEEBE_PORT}"
                )
                from zeebeapp.worker import worker

                await worker.work()
            except Exception as e:
                logger.info("ZEEBE is not available.", e, exc_info=e)
                await self.sleep(60.0)
                logger.info("ZEEBE worker waking up")
                raise


if __name__ == "__main__":
    logger.info("starting app")
    app.main()
