AirDroppy
=========

AirDroppy or AirDropPy is a tool for transferring files from one user to another by simply sharing a link.

The sender uploads a file to the server wich will only accept a few hundred kilobytes before pausing the transfer. Before uploading the file, the sender is being shown an URL that has to be sent to the recipient.

Using this URL, the recipient can now download the file. The file is being uploaded at the same time as it is being downloaded, there are never more than a few hundred kilobytes of data on the server.


Installation
------------

Clone this repository and install its dependencies

    git clone https://github.com/nils-werner/airdroppy.git
    cd airdroppy
    pip install -r requirements.txt

Launch the service

    python airdroppy.py

Then navigate to <http://localhost:8888/>
