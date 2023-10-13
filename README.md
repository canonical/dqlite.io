# dqlite.io

[![Code coverage](https://codecov.io/gh/canonical-web-and-design/dqlite.io/branch/master/graph/badge.svg)](https://codecov.io/gh/canonical-web-and-design/dqlite.io)

This is the repo for the [dqlite.io website](https://dqlite.io).

## Usage

After [installing Docker](https://docs.docker.com/install/):

``` bash
./run
```

And browse to http://127.0.0.1:8037.

## Building and running a Rockcraft image

First install and configure dependencies:

```bash
pip install dotrun
sudo snap install docker
sudo snap install snapcraft --classic
sudo snap install lxd
lxd init --auto
lxc network set lxdbr0 ipv6.address none
```

Build Rockcraft with support for the `flask-framework` extension:

```bash
git clone --branch feature/12f https://github.com/canonical/rockcraft.git
cd rockcraft
snapcraft --use-lxd
sudo snap install rockcraft*.snap --classic --dangerous
```

Build the dqlite.io image using Rockcraft:

```bash
cd ../dqlite.io
dotrun build
export ROCKCRAFT_ENABLE_EXPERIMENTAL_EXTENSIONS=true && rockcraft pack
```

Import the image into Docker and run it:

```bash
sudo /snap/rockcraft/current/bin/skopeo --insecure-policy copy oci-archive:dqlite-io_0.1_amd64.rock docker-daemon:dqlite-io:0.1
docker run -it --env FLASK_SECRET_KEY=testkey dqlite-io:0.1
```

Finally, use `docker inspect` to determine the container's IP address and browse to http://<ip-address>:8000.

## Deploy
You can find the deployment config in the deploy folder.
