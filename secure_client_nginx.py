import grpc

import service_pb2
import service_pb2_grpc


def main():
    host = 'example.domain.com'
    port = '1443'

    with open('server.crt', 'rb') as f:
        trusted_certs = f.read()

    credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
    channel = grpc.secure_channel('{}:{}'.format(host, port), credentials)

    stub_prod = service_pb2_grpc.ProdServerStub(channel)
    data_prod = service_pb2.ProdRootData(message='hi prod!')
    response_prod = stub_prod.ProdRoot(data_prod)
    print(response_prod.message)

    stub_stage = service_pb2_grpc.StageServerStub(channel)
    data_stage = service_pb2.ProdRootData(message='hi stage!')
    response_stage = stub_stage.StageRoot(data_stage)
    print(response_stage.message)

if __name__ == '__main__':
    main()
