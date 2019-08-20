import sys

import grpc

import python_liftbridge.api_pb2_grpc


class BaseClient(object):

    """
        Connect creates a Client connection for the given Liftbridge cluster.
        Multiple addresses can be provided. Connect will use whichever it connects
        successfully to first in random order. The Client will use the pool of
        addresses for failover purposes. Note that only one seed address needs to be
        provided as the Client will discover the other brokers when fetching
        metadata for the cluster.
    """

    def __init__(self, ip_address='127.0.0.1:9292', timeout=5, tls_cert=None):
        self.ip_address = ip_address
        self.timeout = timeout
        if tls_cert:
            self.stub = self._secure_connect(tls_cert)
        else:
            self.stub = self._insecure_connect()

    def _insecure_connect(self):
        channel = grpc.insecure_channel(self.ip_address)
        try:
            grpc.channel_ready_future(channel).result(timeout=self.timeout)
        except grpc.FutureTimeoutError:
            sys.exit('Error connecting to server')
        else:
            return python_liftbridge.api_pb2_grpc.APIStub(channel)

    def _secure_connect(self, secure_file):
        pass

    def close(self):
        pass
