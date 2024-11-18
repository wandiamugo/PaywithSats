# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from peersrpc import peers_pb2 as peersrpc_dot_peers__pb2

GRPC_GENERATED_VERSION = '1.67.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in peersrpc/peers_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class PeersStub(object):
    """Peers is a service that can be used to get information and interact
    with the other nodes of the network.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.UpdateNodeAnnouncement = channel.unary_unary(
                '/peersrpc.Peers/UpdateNodeAnnouncement',
                request_serializer=peersrpc_dot_peers__pb2.NodeAnnouncementUpdateRequest.SerializeToString,
                response_deserializer=peersrpc_dot_peers__pb2.NodeAnnouncementUpdateResponse.FromString,
                _registered_method=True)


class PeersServicer(object):
    """Peers is a service that can be used to get information and interact
    with the other nodes of the network.
    """

    def UpdateNodeAnnouncement(self, request, context):
        """lncli: peers updatenodeannouncement
        UpdateNodeAnnouncement allows the caller to update the node parameters
        and broadcasts a new version of the node announcement to its peers.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PeersServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'UpdateNodeAnnouncement': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateNodeAnnouncement,
                    request_deserializer=peersrpc_dot_peers__pb2.NodeAnnouncementUpdateRequest.FromString,
                    response_serializer=peersrpc_dot_peers__pb2.NodeAnnouncementUpdateResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'peersrpc.Peers', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('peersrpc.Peers', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class Peers(object):
    """Peers is a service that can be used to get information and interact
    with the other nodes of the network.
    """

    @staticmethod
    def UpdateNodeAnnouncement(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/peersrpc.Peers/UpdateNodeAnnouncement',
            peersrpc_dot_peers__pb2.NodeAnnouncementUpdateRequest.SerializeToString,
            peersrpc_dot_peers__pb2.NodeAnnouncementUpdateResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)