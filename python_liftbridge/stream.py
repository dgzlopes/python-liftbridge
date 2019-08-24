from datetime import datetime
from logging import getLogger
from logging import NullHandler

import python_liftbridge.api_pb2


class Stream():
    """
        This class represents a Stream
    """

    def __init__(
            self,
            subject,
            name,
            group=None,
            replication_factor=1,
            max_replication=False,
            start_offset=None,
            start_timestamp=None,
    ):
        self.logger = getLogger(__name__)
        self.logger.addHandler(NullHandler())
        self.subject = subject
        self.name = name
        self.group = group
        if max_replication:
            self.replication_factor = -1
        else:
            self.replication_factor = replication_factor
        self.start_position = python_liftbridge.api_pb2.StartPosition.Value(
            'NEW_ONLY',
        )
        self.start_offset = start_offset
        self.start_timestamp = start_timestamp

    def start_at_offset(self, offset):
        """Sets the desired start offset to begin consuming from in the stream."""
        self.logger.debug('Sets desired start at offset: %s' % offset)
        self.start_position = python_liftbridge.api_pb2.StartPosition.Value(
            'OFFSET',
        )
        self.start_offset = offset
        self.start_timestamp = None
        return self

    def start_at_time(self, date):
        """Sets the desired timestamp to begin consuming from in the stream."""
        self.logger.debug(
            'Sets desired start at date: %s' %
            datetime.timestamp(date) * 1000000000,
        )
        self.start_timestamp = int(datetime.timestamp(date)) * 1000000000
        self.start_position = python_liftbridge.api_pb2.StartPosition.Value(
            'TIMESTAMP',
        )
        self.start_offset = None
        return self

    def start_at_time_delta(self, time_delta):
        """
            Sets the desired timestamp to begin consuming from in the stream
            using a time delta in the past.
        """
        self.logger.debug('Sets desired start at timedelta: %s' %
                          str(time_delta))
        self.start_position = python_liftbridge.api_pb2.StartPosition.Value(
            'TIMESTAMP',
        )
        actual_time = datetime.utcnow()
        self.start_timestamp = int(datetime.timestamp(
            actual_time - time_delta,
        )) * 1000000000
        self.start_offset = None
        return self

    def start_at_latest_received(self):
        """Sets the subscription start position to the last message received in the stream."""
        self.logger.debug('Sets desired start at latest received')
        self.start_position = python_liftbridge.api_pb2.StartPosition.Value(
            'LATEST',
        )
        return self

    def start_at_earliest_received(self):
        """Sets the subscription start position to the earliest message received in the stream."""
        self.logger.debug('Sets desired start at earliest received')
        self.start_position = python_liftbridge.api_pb2.StartPosition.Value(
            'EARLIEST',
        )
        return self

    def __repr__(self):
        return str(self.__dict__)
