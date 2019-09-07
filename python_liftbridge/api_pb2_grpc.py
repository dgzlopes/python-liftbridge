# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import python_liftbridge.api_pb2 as protos_dot_api__pb2


class APIStub(object):
  """API is the main Liftbridge server interface clients interact with.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.CreateStream = channel.unary_unary(
        '/proto.API/CreateStream',
        request_serializer=protos_dot_api__pb2.CreateStreamRequest.SerializeToString,
        response_deserializer=protos_dot_api__pb2.CreateStreamResponse.FromString,
        )
    self.Subscribe = channel.unary_stream(
        '/proto.API/Subscribe',
        request_serializer=protos_dot_api__pb2.SubscribeRequest.SerializeToString,
        response_deserializer=protos_dot_api__pb2.Message.FromString,
        )
    self.FetchMetadata = channel.unary_unary(
        '/proto.API/FetchMetadata',
        request_serializer=protos_dot_api__pb2.FetchMetadataRequest.SerializeToString,
        response_deserializer=protos_dot_api__pb2.FetchMetadataResponse.FromString,
        )
    self.Publish = channel.unary_unary(
        '/proto.API/Publish',
        request_serializer=protos_dot_api__pb2.PublishRequest.SerializeToString,
        response_deserializer=protos_dot_api__pb2.PublishResponse.FromString,
        )


class APIServicer(object):
  """API is the main Liftbridge server interface clients interact with.
  """

  def CreateStream(self, request, context):
    """CreateStream creates a new stream attached to a NATS subject. It returns
    an AlreadyExists status code if a stream with the given subject and name
    already exists.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Subscribe(self, request, context):
    """Subscribe creates an ephemeral subscription for the given stream. It
    begins to receive messages starting at the given offset and waits for
    new messages when it reaches the end of the stream. Use the request
    context to close the subscription.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def FetchMetadata(self, request, context):
    """FetchMetadata retrieves the latest cluster metadata, including stream
    broker information.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Publish(self, request, context):
    """Publish a new message to a subject. If the AckPolicy is not NONE and a
    deadline is provided, this will synchronously block until the ack is
    received. If the ack is not received in time, a DeadlineExceeded status
    code is returned.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_APIServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'CreateStream': grpc.unary_unary_rpc_method_handler(
          servicer.CreateStream,
          request_deserializer=protos_dot_api__pb2.CreateStreamRequest.FromString,
          response_serializer=protos_dot_api__pb2.CreateStreamResponse.SerializeToString,
      ),
      'Subscribe': grpc.unary_stream_rpc_method_handler(
          servicer.Subscribe,
          request_deserializer=protos_dot_api__pb2.SubscribeRequest.FromString,
          response_serializer=protos_dot_api__pb2.Message.SerializeToString,
      ),
      'FetchMetadata': grpc.unary_unary_rpc_method_handler(
          servicer.FetchMetadata,
          request_deserializer=protos_dot_api__pb2.FetchMetadataRequest.FromString,
          response_serializer=protos_dot_api__pb2.FetchMetadataResponse.SerializeToString,
      ),
      'Publish': grpc.unary_unary_rpc_method_handler(
          servicer.Publish,
          request_deserializer=protos_dot_api__pb2.PublishRequest.FromString,
          response_serializer=protos_dot_api__pb2.PublishResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'proto.API', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
