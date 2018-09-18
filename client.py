import grpc, sys, os, json

import service_pb2
import service_pb2_grpc

def main():
    json_config = os.environ.get('GRPC_RG_JSON_CONFIG', '.')
    with open('{}/rggrpc.service.json'.format(json_config), 'r') as f:
        envs = json.loads(f.read())

    port = envs['server']['GRPC_RG_SERVER_NGINX_PORT']
    host = envs['server']['GRPC_RG_SERVER_NGINX_DOMAIN']
    ssl_crt_file_path = envs['client']['GRPC_RG_SERVER_SSL_CRT_LOCAL_PATH']

    with open('{}'.format(ssl_crt_file_path), 'rb') as f:
        trusted_certs = f.read()

    credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
    channel = grpc.secure_channel('{}:{}'.format(host, port), credentials)

    stub_stage = service_pb2_grpc.StageServerStub(channel)
    data_stage = service_pb2.ProdRootData(message=' '.join(sys.argv[1:]))
    response_stage = stub_stage.StageRoot(data_stage)
    print(response_stage.message)

if __name__ == '__main__':
    main()
