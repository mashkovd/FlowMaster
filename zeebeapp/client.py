import asyncio

from pyzeebe import ZeebeClient, create_insecure_channel

from settings import settings

# Create a zeebe client
channel = create_insecure_channel(
    hostname=settings.ZEEBE_ADDRESS,
    port=settings.ZEEBE_PORT,
)
zeebe_client = ZeebeClient(channel)


# Run a Zeebe process instance
async def run_process(bpmn_process_id: str, variables: dict = None):
    await zeebe_client.run_process(bpmn_process_id=bpmn_process_id, variables=variables)


# Publish message
async def publish_message(
    name: str, correlation_key: str = None, message_id: str = "", variables: dict = None
):
    await zeebe_client.publish_message(
        name=name,
        correlation_key=correlation_key,
        message_id=message_id,
        variables=variables,
    )


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(
        run_process(bpmn_process_id="Process_max_value", variables={"source": "121"})
    )
