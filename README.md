import faust
from aiokafka.helpers import create_ssl_context
from faust.types.auth import AuthProtocol, SASLMechanism

broker_credentials = faust.SASLCredentials(
    mechanism=SASLMechanism.SCRAM_SHA_256,
    ssl_context=create_ssl_context(),
    username='fufjupdj',
    password='n222dzBlEFg5675NzVUFpL2vT2NFHvt1'
)
app = faust.App(
    'fufjupdj',
    broker='glider.srvs.cloudkafka.com:9094',
    broker_credentials=broker_credentials,
    group_id='fufjupdj-consumer',

    ssl_context=create_ssl_context(),
    value_serializer="json",
)


greetings_topic = app.topic('fufjupdj-default')


@app.agent(greetings_topic)
async def greet(greetings):
    async for greeting in greetings:
        print(greeting)


if __name__ == '__main__':
    app.main()
