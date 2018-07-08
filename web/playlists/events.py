import asyncio

from nats.aio.client import Client as NATS

loop = asyncio.get_event_loop()


def publish_playlist_event(youtube_url):

    def _publish_event(args):
        nc = NATS()
        options = {
            "servers": ["nats://nats:4222"],
            "io_loop": loop,
        }

        yield from nc.connect(**options)

        payload = args['payload'].encode()
        yield from nc.publish(args['subject'], payload)

        yield from nc.close()

    args = {
        "subject": "pipeline.playlist",
        "payload": youtube_url,
    }
    futures = [
        _publish_event(args),
    ]
    loop.run_until_complete(asyncio.wait(futures))
