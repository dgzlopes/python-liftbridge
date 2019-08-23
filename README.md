# python-liftbridge
[![PyPI](https://img.shields.io/pypi/v/python-liftbridge.svg)](https://pypi.org/project/python-liftbridge/)
[![GitHub](https://img.shields.io/github/license/dgzlopes/python-liftbridge)](https://github.com/dgzlopes/python-liftbridge/blob/master/LICENSE.md)

Python client for [Liftbridge](https://github.com/liftbridge-io/liftbridge), a system that provides lightweight, fault-tolerant message streams for [NATS](https://nats.io).

Liftbridge provides the following high-level features:

- Log-based API for NATS
- Replicated for fault-tolerance
- Horizontally scalable
- Wildcard subscription support
- At-least-once delivery support and message replay
- Message key-value support
- Log compaction by key

## Installation

```
$ pip install python-liftbridge
```

## Basic Usage

```python
from python_liftbridge import Lift, Message, Stream, ErrStreamExists

# Create a Liftbridge client.
client = Lift(ip_address='localhost:9292', timeout=5)

# Create a stream attached to the NATS subject "foo".
try:
    client.create_stream(Stream(subject='foo', name='foo-stream'))
except ErrStreamExists:
    print('This stream already exists!')

# Publish a message to "foo".
client.publish(Message(value='hello', subject='foo'))

# Subscribe to the stream starting from the beginning.
for message in client.subscribe(
    Stream(
        subject='foo',
        name='foo-stream',
    ).start_at_earliest_received(),
):
    print("Received: '{}'".format(message.value))

```

### Create Stream

[Streams](https://github.com/liftbridge-io/liftbridge/blob/master/documentation/concepts.md#stream) are a durable message log attached to a NATS subject. They record messages published to the subject for consumption.

Streams have a few key properties: a subject, which is the corresponding NATS subject, a name, which is a human-readable identifier for the stream, and a replication factor, which is the number of nodes the stream should be replicated to for redundancy.  Optionally, there is a group which is the name of a load-balance group for the stream to join. When there are multiple streams in the same group, messages will be balanced among them.

```python
"""
    Create a stream attached to the NATS subject "foo.*" that is replicated to
    all the brokers in the cluster. ErrStreamExists is returned if a stream with
    the given name already exists for the subject.
"""
client.create_stream(Stream(subject='foo.*', name='my-stream', max_replication=True))
```

### Subscription Start/Replay Options

[Subscriptions](https://github.com/liftbridge-io/liftbridge/blob/master/documentation/concepts.md#subscription) are how Liftbridge streams are consumed. Clients can choose where to start consuming messages from in a stream. This is controlled using options passed to Subscribe.

```python
# Subscribe starting with new messages only.
client.subscribe(
    Stream(subject='foo', name='foo-stream')
)
# Subscribe starting with the most recently published value.
client.subscribe(
    Stream(subject='foo', name='foo-stream').start_at_earliest_received()
)
# Subscribe starting with the oldest published value.
client.subscribe(
    Stream(subject='foo', name='foo-stream').start_at_latest_received()
)
# Subscribe starting at a specific offset.
client.subscribe(
    Stream(subject='foo', name='foo-stream').start_at_offset(4)
)
# Subscribe starting at a specific time.
client.subscribe(
    Stream(subject='foo', name='foo-stream').start_at_time(datetime.now())
)
# Subscribe starting at a specific amount of time in the past.
client.subscribe(
    Stream(subject='foo', name='foo-stream').start_at_time_delta(timedelta(days=1))
)
```

### Publishing

A publish API is provided to make it easy to write messages to streams. This includes a number of options for decorating messages with metadata like a message key.

Keys are used by Liftbridge's log compaction. When enabled, Liftbridge streams will retain only the last message for a given key.

```python
# Publish a message with a key
client.publish(Message(subject='foo', value='Hello', key='key'))
```

#### Publishing Directly with NATS

Since Liftbridge is an extension of [NATS](https://github.com/nats-io/gnatsd), a [NATS client](https://github.com/nats-io/nats.py) can also be used to publish messages. This means existing NATS publishers do not need any changes for messages to be consumed in Liftbridge.

## How to contribute
1. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
2. Fork [the repository](https://github.com/dgzlopes/python-liftbridge) on GitHub to start making your changes to the master branch (or branch off of it).
3. Write a test which shows that the bug was fixed or that the feature works as expected.
4. Send a [pull request](https://help.github.com/en/articles/creating-a-pull-request-from-a-fork) and bug [me](https://github.com/dgzlopes) until it gets merged and published.

Some things on the backlog:

- [ ] Add documentation (Sphynx)
- [ ] Add CI (CircleCI)
- [ ] Add tests
- [ ] Add code coverage
- [ ] Add TLS support for gRPC
- [ ] Add message headers support
- [ ] Add message ACK support (scaffolding is already done)
- [x] Add method to close connection
- [ ] Add async client
- [ ] Add gRPC connection pool
- [ ] Add logging
- [ ] Improve fetch metadata
- [ ] Better instrumentation/observability (OpenCensus support?)
