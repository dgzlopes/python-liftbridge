import python_liftbridge.api_pb2


class Message():
    """
        This class represents a Message
    """

    def __init__(
            self,
            value,
            subject,
            key=None,
            ack_inbox=None,
            correlation_id=None,
            offset=None,
            timestamp=None,
    ):
        self.key = key
        self.value = value
        self.subject = subject
        self.ack_inbox = ack_inbox
        self.correlation_id = correlation_id
        self.ack_policy = python_liftbridge.api_pb2.AckPolicy.Value('NONE')
        self.offset = offset
        self.timestamp = timestamp

    def ack_policy_all(self):
        """Sets the ack policy to wait for all stream replicas to get the message."""
        self.ack_policy = python_liftbridge.api_pb2.AckPolicy.Value('ALL')
        return self

    def ack_policy_leader(self):
        """Sets the ack policy to wait for just the stream leader to get the message."""
        self.ack_policy = python_liftbridge.api_pb2.AckPolicy.Value('LEADER')
        return self

    def ack_policy_none(self):
        """Don't send an ack."""
        self.ack_policy = python_liftbridge.api_pb2.AckPolicy.Value('NONE')
        return self

    def _build_message(self):
        message = self._create_message()
        message.value = str.encode(self.value)
        message.subject = self.subject
        message.ackPolicy = self.ack_policy
        if self.key:
            message.key = str.encode(self.key)
        if self.ack_inbox:
            message.ackInbox = self.ack_inbox
        if self.correlation_id:
            message.correlationId = self.correlation_id
        return message

    def _create_message(self):
        return python_liftbridge.api_pb2.Message()
