# SFTP to AWS S3
SFTP server with S3 support as backend. As simple as that

## Getting started
You may want to check the existing docker image for this software from DockerHub.

### Usage
```
./run.py -c <config_file.yml> [--host='0.0.0.0'] [-p 21] [-l INFO] [-b mybucket] [-k ssh_private_key_file]
```

### Creating the config file
Just create a YAML file with the following structure:
```yaml
bucket: 'mybucket'
keys:
  - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDt2m6agh6+IniAGXATi4LGb30zUDhWdROCTIk77KDYHLqLf5Cht3WtcK6aMjad9GHPshjs7DA0TlN0tWzA4D9C9RhKOY+VXvVhLU/g0L/DFgAM3uQ18CIpedoI+CGtsrHFD5GmZmggaMQtCBkOHhTGqTu6tpyjs6DnZ/vp6YWYpPMlPGMcwxKeFW43XkJKFcG12ChpQFi9/blM26yxCmC64oCJwyhJ+L3OST6gBdjnfdguwMthBFZPaQKzWFd0hEwjlH91KV+EhBMzBhDuoSvDoYnszkixnPOcpo3cIBIcxp6OWSqo1iU4orH8PVUaRe+XNBp7hW6GqzrmpLkVRPb+fL62j8/8Oa8OLVH+iYug7bpGNZPJKS3O76T/UB3K7HpGkue8nyHEi5s5gBcVUOUorJDB8GpnN+2LTAmMnRAmivRSC74ZT+hI2IgkscQoNMgm8eDnsupGhC4l6/tJP82/hEdDY0hpY8FZI9ME8PJ2IKSu/gpzbsRptZVGbVG4+aM= # Sample key 1
  - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDt2m6agh6+IniAGXATi4LGb30zUDhWdROCTIk77KDYHLqLf5Cht3WtcK6aMjad9GHPshjs7DA0TlN0tWzA4D9C9RhKOY+VXvVhLU/g0L/DFgAM3uQ18CIpedoI+CGtsrHFD5GmZmggaMQtCBkOHhTGqTu6tpyjs6DnZ/vp6YWYpPMlPGMcwxKeFW43XkJKFcG12ChpQFi9/blM26yxCmC64oCJwyhJ+L3OST6gBdjnfdguwMthBFZPaQKzWFd0hEwjlH91KV+EhBMzBhDuoSvDoYnszkixnPOcpo3cIBIcxp6OWSqo1iU4orH8PVUaRe+XNBp7hW6GqzrmpLkVRPb+fL62j8/8Oa8OLVH+iYug7bpGNZPJKS3O76T/UB3K7HpGkue8nyHEi5s5gBcVUOUorJDB8GpnN+2LTAmMnRAmivRSC74ZT+hI2IgkscQoNMgm8eDnsupGhC4l6/tJP82/hEdDY0hpY8FZI9ME8PJ2IKSu/gpzbsRptZVGbVG4+aM= # Sample key 2
private_key: |
  -----BEGIN RSA PRIVATE KEY-----
  MIIEogIBAAKCAQEAvq0vfXTkphx7T+0qXNjcr8uE6qBUjdcXECucRdEEIi5R4xp2
  dr2BRhi3GrJK3wV9FkkeNOl0r+z5FAYIzF5lt4zmPN/NlhwAt7RZahnWMc7T2cmb
  sXNMYvmgpRVrG0wFvUoI+Y1l+9rjjwAzuKFtV7xy4p92bY+ARI+d1CQ80pZkwVtu
  95upGjOMCtXUA8/d3C1sscM4JjANKVlrcDSgb7T8NojYiBex8z7a7NoMn9cab+tp
  lSIbIt41NpQhbIxJCtLtKAU00mObnUnf5mSgOkL7MOMUnhX1n/2VpIZG6U7B1yT8
  TEApigq0MkfQLJkoMoJqN3mdpQwqwD3Db5s5ZQIDAQABAoIBADG77nUktjb1mtxg
  GfqZvgZEaWjhZOySO7vGBD7Zo+BegJFh56BVEZD9BVV7R7ggMF5NuAlJE1yHzPgC
  Eu1redCEedFK9s6+gxlneyMHlizrq6pUwb1pO3Vdcx9cFNHL5HtZAjpFPWKR12UH
  QnZX9LM7viOKQFOXaHd5lkstIIg0qmXC7Z7FkAgPIvO18yASlCYwISPBgQpdEVu8
  P2R+9Z7lHu8skqLC8KFfMwiZ3P/bTZeloCabpAOeeLoExR/7tMZxGL8QdS2HuAeF
  nyJ39T911Te6nl67T4UDh+Q/YE2mvCs7ecQL1Eih6FvRcN8l7/kcqmwS1exN3UET
  za7P5okCgYEA8Qjl5rsnpmvXE98Ajqj0VvMEL5oMrsGyDg+W/757pCTxSuuvDlPB
  Ombbk3+UgmwUo9uOezmzmrnuXq7rmrtOcM+ji68De9WN7ne5v4Vk9wbzS3Y8fH/B
  MOuEcdALb6jcrs36deks/rJZpWyANEbiDiIDlQ9uZWIuUwGpu5/0OwMCgYEAyoPf
  mgCPtD4NtdwWWBrDveQnqUf0w9xjdpE2zCDt4QmykALiJjof9qFTqv2Jgco0Qlvi
  nCpQPaDCmvKvN+CVUruXYuhwsPXuqbavkPecbyHVQyjYwytVyHGxxARLVCLluMpz
  rsypbob30ctaksDNXoyMFBMWqVfOZOTuUxJFmXcCgYB06Uf5/lVhF3WfIc93YuQB
  OKaTIDl+mlzvDQjEy3PVTkXrfR3P6TgUR8fBZ2R1Tk9Emz4k7vv61KyWKGoHB0so
  1M4S9rTN3+uT+2aRSvaKC0j/FT6JdL4UKGh5e9vQMSu5bhdKEevNLlzlLBeTQ75p
  9H2gU3fMnS6y/F+DrjYcWQKBgC3oBt/aELlC98ipw0blikmZVoRBE3LymnleIZXU
  QRgqIpgSj0ErG+PEXjr8jhclxwLj4VKVJOtTbcnCCYYZGsBOVdrN5f23QgqmptWt
  y4BFoxo+QCS9xgxR+YH9lzXTU0+4VNDjA+VSIwsjlbx+iA9OvNIwIYrxpI+qdXvP
  QIexAoGAfo4OMInOxCRaTnYOlNWCRwzkxjvZRIHXwAQ2ek0c6nqd7jAu30MsuEGq
  boKuTDIH1O3vfNZf0DEq3yg5Aj7Bu4DtszNoJAIlR7RKer+mckDzgvyBD2gyuT5q
  NHxSh107PvDlBsiL2aI185DAU8O4wq4fLJD9WexTQksK6Z3Ac+I=
  -----END RSA PRIVATE KEY-----
listen_addr: '0.0.0.0'
listen_port: 3373
```

### Docker image
Running this image is as simple as
```
docker run -v ./sample_config.yml:/app/sample_config.yml sftp2s3 sftp2s3 -c /app/sample_config.yml
```

## Configuration
The configuration order is, from less to more:
- Defaults
- Environment variables
- Configuration file
- Command line arguments

It is mandatory to have a configuration file 

### Defaults
The default values are
- listen_addr: `localhost`
- listen_port: `3373`
- bucket: `None`
- private_key: `None`
- public_keys: `None`

### Environment variables
- `CONFIG_FILE`: Path of the configuration file
- `SSH_PUBLIC_KEY`: Single SSH public key allowed
- `S3_BUCKET`: Name of the linked S3 bucket
- `LISTEN_ADDR`: Listen address
- `LISTEN_PORT`: Listen port

### Configuration file
You can create a YAML file for storing the application settings using the following keys:
- `log_level`: Log level.
- `keys`: List of public keys allowed to use this service.
- `private_key`: Content of the SSH private key used by the server.
- `bucket`: Name of the linked S3 bucket.
- `listen_addr`: Listen address.
- `listen_port`: Listen port.
