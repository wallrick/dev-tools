# This is a devspace config that does the following

    - Spins up a ubuntu pod
    - Reverse port forwards
    - Sets http proxy environment variables to forward traffic to the reverse port

To have web traffic redirected from within the container to an external web proxy do the following.

    - If you use the reverse_proxy.sh script it will start a web proxy in a docker container.  
    - If you then run the `socat-proxy.sh <remote ip>` it will forward traffic from the local port to the remote server.  

