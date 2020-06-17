from logging import getLogger
from logging import NullHandler

import python_liftbridge.api_pb2
from python_liftbridge.base import BaseClient
from python_liftbridge.errors import handle_rpc_errors
from python_liftbridge.errors import handle_rpc_errors_in_generator
from python_liftbridge.message import Message  # noqa: F401
from python_liftbridge.stream import Stream  # noqa: F401

logger = getLogger(__name__)
logger.addHandler(NullHandler())


class Lift(BaseClient):

    def fetch_metadata(self):
        # TODO
        return self._fetch_metadata(self._fetch_metadata_request())

    def subscribe(self, stream):
        """
            Subscribe creates an ephemeral subscription for the given stream. It begins
            receiving messages starting at the configured position and waits for new
            messages when it reaches the end of the stream. The default start position
            is the end of the stream. It returns an ErrNoSuchStream if the given stream
            does not exist.
        """
        logger.debug('Creating a new subscription to: %s' % stream)
        for message in self._subscribe(self._subscribe_request(stream)):
            yield message

    def create_stream(self, stream):
        """
            CreateStream creates a new stream attached to a NATS subject. Subject is the
            NATS subject the stream is attached to, and name is the stream identifier,
            unique per subject. It returns ErrStreamExists if a stream with the given
            subject and name already exists.
        """
        logger.debug('Creating a new stream: %s' % stream)
        return self._create_stream(self._create_stream_request(stream))

    def publish(self, message):
        """
            Publish publishes a new message to the NATS subject.
        """
        logger.debug('Publishing a new message: %s' % message)
        return self._publish(
            self._create_publish_request(message._build_message()),
        )

    @handle_rpc_errors
    def _fetch_metadata(self, metadata_request):
        response = self.stub.FetchMetadata(metadata_request)
        return response

    @handle_rpc_errors_in_generator
    def _subscribe(self, subscribe_request):
        for message in self.stub.Subscribe(subscribe_request):
            yield Message(
                message.value,
                message.subject,
                offset=message.offset,
                timestamp=message.timestamp,
                key=message.key,
            )

    @handle_rpc_errors
    def _create_stream(self, stream_request):
        response = self.stub.CreateStream(stream_request)
        return response

    @handle_rpc_errors
    def _publish(self, publish_request):
        response = self.stub.PublishToSubject(publish_request)
        return response

    def _fetch_metadata_request(self):
        return python_liftbridge.api_pb2.FetchMetadataRequest()

    def _create_stream_request(self, stream):
        response = python_liftbridge.api_pb2.CreateStreamRequest(
            subject=stream.subject,
            name=stream.name,
            group=stream.group,
            replicationFactor=stream.replication_factor,
        )
        return response

    def _subscribe_request(self, stream):
        if stream.start_offset:
            return python_liftbridge.api_pb2.SubscribeRequest(
                stream=stream.name,
                startPosition=stream.start_position,
                startOffset=stream.start_offset,
            )
        elif stream.start_timestamp:
            return python_liftbridge.api_pb2.SubscribeRequest(
                stream=stream.name,
                startPosition=stream.start_position,
                startTimestamp=stream.start_timestamp,
            )
        else:
            return python_liftbridge.api_pb2.SubscribeRequest(
                stream=stream.name,
                startPosition=stream.start_position,
            )

    def _create_publish_request(self, message):
        return python_liftbridge.api_pb2.PublishToSubjectRequest(
            key=message.key, 
            value=message.value,
            subject=message.subject,
            headers=message.headers,
            ackInbox=message.ackInbox,
            correlationId=message.correlationId,
            ackPolicy=message.ackPolicy,
        )
