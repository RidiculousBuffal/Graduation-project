import io
import os
from typing import Dict

import requests


class IPFSClient:
    """
    A comprehensive Python client for the IPFS API.

    This client implements all endpoints available in the Kubo IPFS API v0.34.1.
    """

    def __init__(self, host="127.0.0.1", port=5001, base_path="/api/v0", session=None):
        """
        Initialize the IPFS client.

        Args:
            host: The host where the IPFS daemon is running
            port: The port of the IPFS API
            base_path: The base path of the API
            session: A custom requests session (if needed)
        """
        self.api_url = f"{host}:{port}{base_path}"
        self.session = session or requests.Session()

    def _make_request(self, command: str, files=None, params=None, data=None, method='post') -> Dict:
        """
        Make a request to the IPFS API.

        Args:
            command: The API command to execute
            files: Files to upload (if any)
            params: Query parameters
            data: Request body data
            method: HTTP method to use

        Returns:
            The API response as a dictionary or text
        """
        url = f"{self.api_url}/{command}"

        if method.lower() == 'post':
            response = self.session.post(url, files=files, params=params, data=data)
        else:
            response = self.session.get(url, params=params)

        if response.status_code >= 400:
            try:
                error_message = response.json().get('Message', response.text)
            except ValueError:
                error_message = response.text
            raise Exception(f"IPFS API error ({response.status_code}): {error_message}")

        # Check if the response is JSON
        content_type = response.headers.get('Content-Type', '')
        if 'json' in content_type:
            return response.json()
        else:
            # For some endpoints, return raw content instead of wrapping in dict
            if 'octet-stream' in content_type or 'text/plain' in content_type:
                return response.content
            return {"Text": response.text}

    def _prepare_files(self, file_param, file_obj):
        """
        Prepare files for upload to IPFS.

        Args:
            file_param: The parameter name to use
            file_obj: File object or path

        Returns:
            Prepared files dictionary
        """
        if isinstance(file_obj, str) and os.path.isfile(file_obj):
            return {file_param: open(file_obj, 'rb')}
        elif isinstance(file_obj, (bytes, bytearray)):
            return {file_param: io.BytesIO(file_obj)}
        elif hasattr(file_obj, 'read'):  # File-like object
            return {file_param: file_obj}
        else:
            return {file_param: file_obj}

    # Basic IPFS operations

    def add(self, file_path_or_obj, **kwargs):
        """
        Add a file or directory to IPFS.

        Args:
            file_path_or_obj: Path to file or file object
            **kwargs: Optional arguments as documented in the API
                quiet: bool - Write minimal output
                quieter: bool - Write only final hash
                silent: bool - Write no output
                progress: bool - Stream progress data
                trickle: bool - Use trickle-dag format for dag generation
                only-hash: bool - Only chunk and hash - do not write to disk
                wrap-with-directory: bool - Wrap files with a directory object
                chunker: str - Chunking algorithm
                pin: bool - Pin this object when adding
                raw-leaves: bool - Use raw blocks for leaf nodes
                nocopy: bool - Add the file using filestore
                And more...

        Returns:
            Dict with information about the added file
        """
        files = self._prepare_files('file', file_path_or_obj)
        return self._make_request('add', files=files, params=kwargs)

    def cat(self, ipfs_path, **kwargs):
        """
        Show IPFS object data.

        Args:
            ipfs_path: The path to the IPFS object to be outputted
            **kwargs: Optional arguments:
                offset: int - Byte offset to begin reading from
                length: int - Maximum number of bytes to read
                progress: bool - Stream progress data

        Returns:
            The content of the IPFS object
        """
        params = {"arg": ipfs_path, **kwargs}
        return self._make_request('cat', params=params)

    def get(self, ipfs_path, output=None, **kwargs):
        """
        Download IPFS objects.

        Args:
            ipfs_path: The path to the IPFS object to be retrieved
            output: The path where the output should be stored
            **kwargs: Optional arguments:
                archive: bool - Output a TAR archive
                compress: bool - Compress the output with GZIP compression
                compression-level: int - The level of compression (1-9)
                progress: bool - Stream progress data

        Returns:
            The downloaded content
        """
        params = {"arg": ipfs_path}
        if output:
            params["output"] = output
        params.update(kwargs)

        return self._make_request('get', params=params)

    def ls(self, ipfs_path, **kwargs):
        """
        List directory contents for Unix filesystem objects.

        Args:
            ipfs_path: The path to the IPFS object to list links from
            **kwargs: Optional arguments:
                headers: bool - Print table headers
                resolve-type: bool - Resolve linked objects to find their types
                size: bool - Resolve linked objects to find out their file size
                stream: bool - Stream directory entries

        Returns:
            Dict with listing information
        """
        params = {"arg": ipfs_path, **kwargs}
        return self._make_request('ls', params=params)

    # Block API

    def block_put(self, data, **kwargs):
        """
        Store input as an IPFS block.

        Args:
            data: The data to store as a block
            **kwargs: Optional arguments:
                format: str - Format that the block will be a given in
                mhtype: str - Multihash hash function
                mhlen: int - Multihash hash length
                pin: bool - Pin added blocks recursively

        Returns:
            Dict with block information (Key and Size)
        """
        files = self._prepare_files('file', data)
        return self._make_request('block/put', files=files, params=kwargs)

    def block_get(self, cid):
        """
        Get a raw IPFS block.

        Args:
            cid: The CID of an existing block to get

        Returns:
            The raw block data
        """
        params = {"arg": cid}
        return self._make_request('block/get', params=params)

    def block_stat(self, cid):
        """
        Print information of a raw IPFS block.

        Args:
            cid: The CID of an existing block to stat

        Returns:
            Dict with block information (Key and Size)
        """
        params = {"arg": cid}
        return self._make_request('block/stat', params=params)

    def block_rm(self, cid, **kwargs):
        """
        Remove IPFS block(s) from the local datastore.

        Args:
            cid: CID of block to remove
            **kwargs: Optional arguments:
                force: bool - Ignore nonexistent blocks
                quiet: bool - Write minimal output

        Returns:
            Dict with removal information
        """
        params = {"arg": cid, **kwargs}
        return self._make_request('block/rm', params=params)

    # BitSwap API

    def bitswap_stat(self, **kwargs):
        """
        Show diagnostic information on the bitswap agent.

        Args:
            **kwargs: Optional arguments:
                verbose: bool - Print extra information
                human: bool - Print sizes in human-readable format

        Returns:
            Dict with bitswap statistics
        """
        return self._make_request('bitswap/stat', params=kwargs)

    def bitswap_wantlist(self, **kwargs):
        """
        Show blocks currently on the wantlist.

        Args:
            **kwargs: Optional arguments:
                peer: str - Specify which peer to show wantlist for

        Returns:
            Dict with wanted blocks
        """
        return self._make_request('bitswap/wantlist', params=kwargs)

    def bitswap_ledger(self, peer):
        """
        Show the current ledger for a peer.

        Args:
            peer: The PeerID (B58) of the ledger to inspect

        Returns:
            Dict with ledger information
        """
        params = {"arg": peer}
        return self._make_request('bitswap/ledger', params=params)

    # Bootstrap API

    def bootstrap(self):
        """
        Show or edit the list of bootstrap peers.

        Returns:
            Dict with bootstrap peers
        """
        return self._make_request('bootstrap')

    def bootstrap_add(self, peer=None, **kwargs):
        """
        Add peers to the bootstrap list.

        Args:
            peer: A peer to add to the bootstrap list
            **kwargs: Optional arguments:
                default: bool - Add default bootstrap nodes

        Returns:
            Dict with added peers
        """
        params = kwargs
        if peer:
            params["arg"] = peer
        return self._make_request('bootstrap/add', params=params)

    def bootstrap_add_default(self):
        """
        Add default peers to the bootstrap list.

        Returns:
            Dict with added peers
        """
        return self._make_request('bootstrap/add/default')

    def bootstrap_list(self):
        """
        Show peers in the bootstrap list.

        Returns:
            Dict with bootstrap peers
        """
        return self._make_request('bootstrap/list')

    def bootstrap_rm(self, peer=None, **kwargs):
        """
        Remove peers from the bootstrap list.

        Args:
            peer: A peer to remove from the bootstrap list
            **kwargs: Optional arguments:
                all: bool - Remove all bootstrap peers

        Returns:
            Dict with removed peers
        """
        params = kwargs
        if peer:
            params["arg"] = peer
        return self._make_request('bootstrap/rm', params=params)

    def bootstrap_rm_all(self):
        """
        Remove all peers from the bootstrap list.

        Returns:
            Dict with removed peers
        """
        return self._make_request('bootstrap/rm/all')

    # DAG API

    def dag_export(self, root, **kwargs):
        """
        Streams the selected DAG as a .car stream.

        Args:
            root: CID of a root to recursively export
            **kwargs: Optional arguments:
                progress: bool - Display progress on CLI

        Returns:
            The exported CAR data
        """
        params = {"arg": root, **kwargs}
        return self._make_request('dag/export', params=params)

    def dag_get(self, ref, **kwargs):
        """
        Get a DAG node from IPFS.

        Args:
            ref: The object to get
            **kwargs: Optional arguments:
                output-codec: str - Format that the object will be encoded as

        Returns:
            The DAG node data
        """
        params = {"arg": ref, **kwargs}
        return self._make_request('dag/get', params=params)

    def dag_import(self, car_file, **kwargs):
        """
        Import the contents of .car files.

        Args:
            car_file: The CAR file to import
            **kwargs: Optional arguments:
                pin-roots: bool - Pin optional roots
                silent: bool - No output
                stats: bool - Output stats

        Returns:
            Dict with import information
        """
        files = self._prepare_files('path', car_file)
        return self._make_request('dag/import', files=files, params=kwargs)

    def dag_put(self, data, **kwargs):
        """
        Add a DAG node to IPFS.

        Args:
            data: The DAG node data to add
            **kwargs: Optional arguments:
                store-codec: str - Codec that the stored object will be encoded with
                input-codec: str - Codec that the input object is encoded in
                pin: bool - Pin this object when adding
                hash: str - Hash function to use

        Returns:
            Dict with CID information
        """
        files = self._prepare_files('object data', data)
        return self._make_request('dag/put', files=files, params=kwargs)

    def dag_resolve(self, ref):
        """
        Resolve IPLD block.

        Args:
            ref: The path to resolve

        Returns:
            Dict with resolve information
        """
        params = {"arg": ref}
        return self._make_request('dag/resolve', params=params)

    def dag_stat(self, root, **kwargs):
        """
        Get stats for a DAG.

        Args:
            root: CID of a DAG root to get statistics for
            **kwargs: Optional arguments:
                progress: bool - Return progressive data while reading

        Returns:
            Dict with DAG statistics
        """
        params = {"arg": root, **kwargs}
        return self._make_request('dag/stat', params=params)

    # Diagnostic API

    def diag_cmds(self, **kwargs):
        """
        List commands run on this IPFS node.

        Args:
            **kwargs: Optional arguments:
                verbose: bool - Print extra information

        Returns:
            List of commands
        """
        return self._make_request('diag/cmds', params=kwargs)

    def diag_cmds_clear(self):
        """
        Clear inactive requests from the log.

        Returns:
            Operation result
        """
        return self._make_request('diag/cmds/clear')

    def diag_cmds_set_time(self, time):
        """
        Set how long to keep inactive requests in the log.

        Args:
            time: Time to keep inactive requests in log

        Returns:
            Operation result
        """
        params = {"arg": time}
        return self._make_request('diag/cmds/set-time', params=params)

    def diag_profile(self, **kwargs):
        """
        Collect a performance profile for debugging.

        Args:
            **kwargs: Optional arguments:
                output: str - The path where output .zip should be stored
                collectors: list - The list of collectors to use
                profile-time: str - The amount of time spent profiling

        Returns:
            Profile data
        """
        return self._make_request('diag/profile', params=kwargs)

    def diag_sys(self):
        """
        Print system diagnostic information.

        Returns:
            System diagnostic information
        """
        return self._make_request('diag/sys')

    # Files API (MFS)

    def files_chcid(self, path="/", **kwargs):
        """
        Change the CID version or hash function of the root node of a given path.

        Args:
            path: Path to change (default '/')
            **kwargs: Optional arguments:
                cid-version: int - CID version to use
                hash: str - Hash function to use

        Returns:
            Operation result
        """
        params = {"arg": path, **kwargs}
        return self._make_request('files/chcid', params=params)

    def files_cp(self, source, dest, **kwargs):
        """
        Add references to IPFS files and directories in MFS (or copy within MFS).

        Args:
            source: Source IPFS or MFS path to copy
            dest: Destination within MFS
            **kwargs: Optional arguments:
                parents: bool - Make parent directories as needed

        Returns:
            Operation result
        """
        params = {"arg": [source, dest], **kwargs}
        return self._make_request('files/cp', params=params)

    def files_flush(self, path="/"):
        """
        Flush a given path's data to disk.

        Args:
            path: Path to flush (default '/')

        Returns:
            Dict with CID
        """
        params = {"arg": path}
        return self._make_request('files/flush', params=params)

    def files_ls(self, path="/", **kwargs):
        """
        List directories in the local mutable namespace.

        Args:
            path: Path to show listing for (default '/')
            **kwargs: Optional arguments:
                long: bool - Use long listing format
                U: bool - Do not sort; list entries in directory order

        Returns:
            Dict with directory entries
        """
        params = {"arg": path, **kwargs}
        return self._make_request('files/ls', params=params)

    def files_mkdir(self, path, **kwargs):
        """
        Make directories in MFS.

        Args:
            path: Path to dir to make
            **kwargs: Optional arguments:
                parents: bool - Make parent directories as needed
                cid-version: int - CID version to use
                hash: str - Hash function to use

        Returns:
            Operation result
        """
        params = {"arg": path, **kwargs}
        return self._make_request('files/mkdir', params=params)

    def files_mv(self, source, dest):
        """
        Move files in MFS.

        Args:
            source: Source file to move
            dest: Destination path for file to be moved to

        Returns:
            Operation result
        """
        params = {"arg": [source, dest]}
        return self._make_request('files/mv', params=params)

    def files_read(self, path, **kwargs):
        """
        Read a file from MFS.

        Args:
            path: Path to file to be read
            **kwargs: Optional arguments:
                offset: int - Byte offset to begin reading from
                count: int - Maximum number of bytes to read

        Returns:
            File contents
        """
        params = {"arg": path, **kwargs}
        return self._make_request('files/read', params=params)

    def files_rm(self, path, **kwargs):
        """
        Remove a file from MFS.

        Args:
            path: File to remove
            **kwargs: Optional arguments:
                recursive: bool - Recursively remove directories
                force: bool - Forcibly remove target at path

        Returns:
            Operation result
        """
        params = {"arg": path, **kwargs}
        return self._make_request('files/rm', params=params)

    def files_stat(self, path, **kwargs):
        """
        Display file status.

        Args:
            path: Path to node to stat
            **kwargs: Optional arguments:
                format: str - Print statistics in given format
                hash: bool - Print only hash
                size: bool - Print only size

        Returns:
            Dict with file status
        """
        params = {"arg": path, **kwargs}
        return self._make_request('files/stat', params=params)

    def files_write(self, path, data, **kwargs):
        """
        Write to a file in MFS.

        Args:
            path: Path to write to
            data: Data to write
            **kwargs: Optional arguments:
                offset: int - Byte offset to begin writing at
                create: bool - Create the file if it does not exist
                parents: bool - Make parent directories as needed
                truncate: bool - Truncate the file before writing

        Returns:
            Operation result
        """
        params = {"arg": path, **kwargs}
        files = self._prepare_files('data', data)
        return self._make_request('files/write', files=files, params=params)

    # Filestore API

    def filestore_dups(self):
        """
        List blocks that are both in the filestore and standard block storage.

        Returns:
            Dict with duplicate blocks
        """
        return self._make_request('filestore/dups')

    def filestore_ls(self, obj=None, **kwargs):
        """
        List objects in filestore.

        Args:
            obj: CID of objects to list
            **kwargs: Optional arguments:
                file-order: bool - Sort results based on backing file path

        Returns:
            Dict with filestore objects
        """
        params = kwargs
        if obj:
            params["arg"] = obj
        return self._make_request('filestore/ls', params=params)

    def filestore_verify(self, obj=None, **kwargs):
        """
        Verify objects in filestore.

        Args:
            obj: CID of objects to verify
            **kwargs: Optional arguments:
                file-order: bool - Verify objects based on backing file

        Returns:
            Dict with verification results
        """
        params = kwargs
        if obj:
            params["arg"] = obj
        return self._make_request('filestore/verify', params=params)

    # Key API

    def key_gen(self, name, **kwargs):
        """
        Create a new keypair.

        Args:
            name: Name of key to create
            **kwargs: Optional arguments:
                type: str - Type of the key (rsa, ed25519)
                size: int - Size of the key
                ipns-base: str - Encoding used for keys

        Returns:
            Dict with generated key info
        """
        params = {"arg": name, **kwargs}
        return self._make_request('key/gen', params=params)

    def key_import(self, name, key_data, **kwargs):
        """
        Import a key and print imported key ID.

        Args:
            name: Name to associate with key in keychain
            key_data: The key file data
            **kwargs: Optional arguments:
                ipns-base: str - Encoding used for keys
                format: str - Format of the key

        Returns:
            Dict with imported key info
        """
        params = {"arg": name, **kwargs}
        files = self._prepare_files('key', key_data)
        return self._make_request('key/import', files=files, params=params)

    def key_list(self, **kwargs):
        """
        List all local keypairs.

        Args:
            **kwargs: Optional arguments:
                l: bool - Show extra information about keys
                ipns-base: str - Encoding used for keys

        Returns:
            Dict with key list
        """
        return self._make_request('key/list', params=kwargs)

    def key_rename(self, old_name, new_name, **kwargs):
        """
        Rename a keypair.

        Args:
            old_name: Name of key to rename
            new_name: New name of the key
            **kwargs: Optional arguments:
                force: bool - Allow overwriting an existing key
                ipns-base: str - Encoding used for keys

        Returns:
            Dict with rename result
        """
        params = {"arg": [old_name, new_name], **kwargs}
        return self._make_request('key/rename', params=params)

    def key_rm(self, name, **kwargs):
        """
        Remove a keypair.

        Args:
            name: Names of keys to remove
            **kwargs: Optional arguments:
                l: bool - Show extra information about keys
                ipns-base: str - Encoding used for keys

        Returns:
            Dict with removal result
        """
        params = {"arg": name, **kwargs}
        return self._make_request('key/rm', params=params)

    def key_sign(self, data, **kwargs):
        """
        EXPERIMENTAL: Sign a data with a key.

        Args:
            data: Data to sign
            **kwargs: Optional arguments:
                key: str - Name of key to use
                ipns-base: str - Encoding used for keys

        Returns:
            Dict with signature information
        """
        params = kwargs
        files = self._prepare_files('data', data)
        return self._make_request('key/sign', files=files, params=params)

    def key_verify(self, data, **kwargs):
        """
        EXPERIMENTAL: Verify that the given data and signature match.

        Args:
            data: Data to verify
            **kwargs: Optional arguments:
                key: str - Name of key to use for verification
                signature: str - Signature to verify

        Returns:
            Dict with verification result
        """
        params = kwargs
        files = self._prepare_files('data', data)
        return self._make_request('key/verify', files=files, params=params)

    # Log API

    def log_level(self, subsystem, level):
        """
        Change the logging level.

        Args:
            subsystem: The subsystem logging identifier
            level: The log level

        Returns:
            Dict with operation result
        """
        params = {"arg": [subsystem, level]}
        return self._make_request('log/level', params=params)

    def log_ls(self):
        """
        List the logging subsystems.

        Returns:
            Dict with subsystem list
        """
        return self._make_request('log/ls')

    def log_tail(self):
        """
        EXPERIMENTAL: Read the event log.

        Returns:
            The event log
        """
        return self._make_request('log/tail')

    # Name API (IPNS)

    def name_publish(self, ipfs_path, **kwargs):
        """
        Publish IPNS names.

        Args:
            ipfs_path: IPFS path of object to be published
            **kwargs: Optional arguments:
                key: str - Name of the key to use
                resolve: bool - Check if name can be resolved before publishing
                lifetime: str - Time duration of the record
                ttl: str - Time duration hint for caching

        Returns:
            Dict with publish result
        """
        params = {"arg": ipfs_path, **kwargs}
        return self._make_request('name/publish', params=params)

    def name_resolve(self, name=None, **kwargs):
        """
        Resolve IPNS names.

        Args:
            name: The IPNS name to resolve
            **kwargs: Optional arguments:
                recursive: bool - Resolve until the result is not an IPNS name
                nocache: bool - Do not use cached entries

        Returns:
            Dict with resolved path
        """
        params = kwargs
        if name:
            params["arg"] = name
        return self._make_request('name/resolve', params=params)

    def name_inspect(self, record, **kwargs):
        """
        EXPERIMENTAL: Inspect an IPNS Record.

        Args:
            record: The IPNS record data
            **kwargs: Optional arguments:
                verify: str - CID of public IPNS key to validate
                dump: bool - Include a full hex dump of Protobuf record

        Returns:
            Dict with inspection results
        """
        params = kwargs
        files = self._prepare_files('record', record)
        return self._make_request('name/inspect', files=files, params=params)

    def name_pubsub_cancel(self, name):
        """
        EXPERIMENTAL: Cancel a name subscription.

        Args:
            name: Name to cancel the subscription for

        Returns:
            Dict with operation result
        """
        params = {"arg": name}
        return self._make_request('name/pubsub/cancel', params=params)

    def name_pubsub_state(self):
        """
        EXPERIMENTAL: Query the state of IPNS pubsub.

        Returns:
            Dict with pubsub state
        """
        return self._make_request('name/pubsub/state')

    def name_pubsub_subs(self, **kwargs):
        """
        EXPERIMENTAL: Show current name subscriptions.

        Args:
            **kwargs: Optional arguments:
                ipns-base: str - Encoding used for keys

        Returns:
            Dict with subscriptions
        """
        return self._make_request('name/pubsub/subs', params=kwargs)

    # Pin API

    def pin_add(self, ipfs_path, **kwargs):
        """
        Pin objects to local storage.

        Args:
            ipfs_path: Path to object to be pinned
            **kwargs: Optional arguments:
                recursive: bool - Recursively pin object links
                progress: bool - Show progress

        Returns:
            Dict with pinned objects
        """
        params = {"arg": ipfs_path, **kwargs}
        return self._make_request('pin/add', params=params)

    def pin_ls(self, ipfs_path=None, **kwargs):
        """
        List objects pinned to local storage.

        Args:
            ipfs_path: Path to object to be listed
            **kwargs: Optional arguments:
                type: str - The type of pinned keys to list
                quiet: bool - Output only CIDs

        Returns:
            Dict with pinned objects
        """
        params = kwargs
        if ipfs_path:
            params["arg"] = ipfs_path
        return self._make_request('pin/ls', params=params)

    def pin_rm(self, ipfs_path, **kwargs):
        """
        Remove object from pin-list.

        Args:
            ipfs_path: Path to object to be unpinned
            **kwargs: Optional arguments:
                recursive: bool - Recursively unpin the object

        Returns:
            Dict with unpinned objects
        """
        params = {"arg": ipfs_path, **kwargs}
        return self._make_request('pin/rm', params=params)

    def pin_update(self, from_path, to_path, **kwargs):
        """
        Update a recursive pin.

        Args:
            from_path: Path to old object
            to_path: Path to new object to be pinned
            **kwargs: Optional arguments:
                unpin: bool - Remove the old pin

        Returns:
            Dict with operation result
        """
        params = {"arg": [from_path, to_path], **kwargs}
        return self._make_request('pin/update', params=params)

    def pin_verify(self, **kwargs):
        """
        Verify that recursive pins are complete.

        Args:
            **kwargs: Optional arguments:
                verbose: bool - Write the hashes of non-broken pins
                quiet: bool - Write just hashes of broken pins

        Returns:
            Dict with verification results
        """
        return self._make_request('pin/verify', params=kwargs)

    # Pin Remote API

    def pin_remote_add(self, ipfs_path, **kwargs):
        """
        Pin object to remote pinning service.

        Args:
            ipfs_path: CID or Path to be pinned
            **kwargs: Optional arguments:
                service: str - Name of the remote pinning service to use
                name: str - An optional name for the pin
                background: bool - Add to queue on remote service and return

        Returns:
            Dict with remote pin information
        """
        params = {"arg": ipfs_path, **kwargs}
        return self._make_request('pin/remote/add', params=params)

    def pin_remote_ls(self, **kwargs):
        """
        List objects pinned to remote pinning service.

        Args:
            **kwargs: Optional arguments:
                service: str - Name of the remote pinning service
                name: str - Return pins with names containing the value
                cid: list - Return pins for specific CIDs
                status: list - Return pins with specified statuses

        Returns:
            Dict with remotely pinned objects
        """
        return self._make_request('pin/remote/ls', params=kwargs)

    def pin_remote_rm(self, **kwargs):
        """
        Remove pins from remote pinning service.

        Args:
            **kwargs: Optional arguments:
                service: str - Name of the remote pinning service
                name: str - Remove pins with names containing the value
                cid: list - Remove pins for specific CIDs
                status: list - Remove pins with specified statuses
                force: bool - Allow removal without confirmation

        Returns:
            Operation result
        """
        return self._make_request('pin/remote/rm', params=kwargs)

    def pin_remote_service_add(self, name, endpoint, key):
        """
        Add remote pinning service.

        Args:
            name: Service name
            endpoint: Service endpoint
            key: Service key

        Returns:
            Operation result
        """
        params = {"arg": [name, endpoint, key]}
        return self._make_request('pin/remote/service/add', params=params)

    def pin_remote_service_ls(self, **kwargs):
        """
        List remote pinning services.

        Args:
            **kwargs: Optional arguments:
                stat: bool - Try to fetch and display pin count

        Returns:
            Dict with remote services
        """
        return self._make_request('pin/remote/service/ls', params=kwargs)

    def pin_remote_service_rm(self, service):
        """
        Remove remote pinning service.

        Args:
            service: Name of remote pinning service to remove

        Returns:
            Operation result
        """
        params = {"arg": service}
        return self._make_request('pin/remote/service/rm', params=params)

    # CID API

    def cid_base32(self, cid):
        """
        Convert CIDs to Base32 CID version 1.

        Args:
            cid: CID to convert

        Returns:
            Dict with converted CID
        """
        params = {"arg": cid}
        return self._make_request('cid/base32', params=params)

    def cid_bases(self, **kwargs):
        """
        List available multibase encodings.

        Args:
            **kwargs: Optional arguments:
                prefix: bool - Include single letter prefixes
                numeric: bool - Also include numeric codes

        Returns:
            List of available encodings
        """
        return self._make_request('cid/bases', params=kwargs)

    def cid_codecs(self, **kwargs):
        """
        List available CID codecs.

        Args:
            **kwargs: Optional arguments:
                numeric: bool - Include numeric codes
                supported: bool - List only codecs supported by go-ipfs

        Returns:
            List of available codecs
        """
        return self._make_request('cid/codecs', params=kwargs)

    def cid_format(self, cid, **kwargs):
        """
        Format and convert a CID in various useful ways.

        Args:
            cid: CID to format
            **kwargs: Optional arguments:
                f: str - Printf style format string
                v: str - CID version to convert to
                b: str - Multibase to display CID in

        Returns:
            Dict with formatted CID
        """
        params = {"arg": cid, **kwargs}
        return self._make_request('cid/format', params=params)

    def cid_hashes(self, **kwargs):
        """
        List available multihashes.

        Args:
            **kwargs: Optional arguments:
                numeric: bool - Include numeric codes
                supported: bool - List only hashes supported by go-ipfs

        Returns:
            List of available hashes
        """
        return self._make_request('cid/hashes', params=kwargs)

    # Multibase API

    def multibase_decode(self, data):
        """
        Decode multibase string.

        Args:
            data: The data to decode

        Returns:
            Decoded data
        """
        files = self._prepare_files('encoded_file', data)
        return self._make_request('multibase/decode', files=files)

    def multibase_encode(self, data, **kwargs):
        """
        Encode data into multibase string.

        Args:
            data: The data to encode
            **kwargs: Optional arguments:
                b: str - Multibase encoding to use

        Returns:
            Encoded data
        """
        files = self._prepare_files('file', data)
        return self._make_request('multibase/encode', files=files, params=kwargs)

    def multibase_list(self, **kwargs):
        """
        List available multibase encodings.

        Args:
            **kwargs: Optional arguments:
                prefix: bool - Include single letter prefixes
                numeric: bool - Include numeric codes

        Returns:
            List of available encodings
        """
        return self._make_request('multibase/list', params=kwargs)

    def multibase_transcode(self, data, **kwargs):
        """
        Transcode multibase string between bases.

        Args:
            data: The data to transcode
            **kwargs: Optional arguments:
                b: str - Target multibase encoding

        Returns:
            Transcoded data
        """
        files = self._prepare_files('encoded_file', data)
        return self._make_request('multibase/transcode', files=files, params=kwargs)

    # Config API

    def config(self, key, value=None, **kwargs):
        """
        Get and set IPFS config values.

        Args:
            key: The key of the config entry
            value: The value to set the config entry to (if setting)
            **kwargs: Optional arguments:
                bool: bool - Set a boolean value
                json: bool - Parse stringified JSON

        Returns:
            Dict with config value
        """
        params = {"arg": [key]}
        if value is not None:
            params["arg"].append(value)
        params.update(kwargs)
        return self._make_request('config', params=params)

    def config_profile_apply(self, profile, **kwargs):
        """
        Apply profile to config.

        Args:
            profile: The profile to apply
            **kwargs: Optional arguments:
                dry-run: bool - Print difference without applying

        Returns:
            Dict with config changes
        """
        params = {"arg": profile, **kwargs}
        return self._make_request('config/profile/apply', params=params)

    def config_replace(self, config):
        """
        Replace the config with a new config.

        Args:
            config: The new config file

        Returns:
            Operation result
        """
        files = self._prepare_files('file', config)
        return self._make_request('config/replace', files=files)

    def config_show(self):
        """
        Output config file contents.

        Returns:
            Dict with config contents
        """
        return self._make_request('config/show')

    # Other APIs

    def commands(self, **kwargs):
        """
        List all available commands.

        Args:
            **kwargs: Optional arguments:
                flags: bool - Show command flags

        Returns:
            Dict with command information
        """
        return self._make_request('commands', params=kwargs)

    def id(self, peer_id=None, **kwargs):
        """
        Show IPFS node id info.

        Args:
            peer_id: Peer.ID of node to look up
            **kwargs: Optional arguments:
                format: str - Optional output format
                peerid-base: str - Encoding used for peer IDs

        Returns:
            Dict with node information
        """
        params = kwargs
        if peer_id:
            params["arg"] = peer_id
        return self._make_request('id', params=params)

    def ping(self, peer_id, **kwargs):
        """
        Send echo request packets to IPFS hosts.

        Args:
            peer_id: ID of peer to be pinged
            **kwargs: Optional arguments:
                count: int - Number of ping messages to send

        Returns:
            Dict with ping results
        """
        params = {"arg": peer_id, **kwargs}
        return self._make_request('ping', params=params)

    def refs(self, ipfs_path, **kwargs):
        """
        List links (references) from an object.

        Args:
            ipfs_path: Path to the object to list refs from
            **kwargs: Optional arguments:
                format: str - Format for edges
                edges: bool - Emit edge format
                unique: bool - Omit duplicate refs
                recursive: bool - Recursively list links

        Returns:
            Dict with references
        """
        params = {"arg": ipfs_path, **kwargs}
        return self._make_request('refs', params=params)

    def refs_local(self):
        """
        List all local references.

        Returns:
            Dict with local references
        """
        return self._make_request('refs/local')

    def repo_gc(self, **kwargs):
        """
        Perform a garbage collection sweep on the repo.

        Args:
            **kwargs: Optional arguments:
                stream-errors: bool - Stream errors
                quiet: bool - Write minimal output

        Returns:
            Dict with GC results
        """
        return self._make_request('repo/gc', params=kwargs)

    def repo_ls(self):
        """
        List all local references.

        Returns:
            Dict with local references
        """
        return self._make_request('repo/ls')

    def repo_stat(self, **kwargs):
        """
        Get stats for the currently used repo.

        Args:
            **kwargs: Optional arguments:
                size-only: bool - Only report RepoSize and StorageMax
                human: bool - Print sizes in human readable format

        Returns:
            Dict with repo stats
        """
        return self._make_request('repo/stat', params=kwargs)

    def repo_verify(self):
        """
        Verify all blocks in repo are not corrupted.

        Returns:
            Dict with verification progress
        """
        return self._make_request('repo/verify')

    def repo_version(self, **kwargs):
        """
        Show the repo version.

        Args:
            **kwargs: Optional arguments:
                quiet: bool - Write minimal output

        Returns:
            Dict with repo version
        """
        return self._make_request('repo/version', params=kwargs)

    def resolve(self, name, **kwargs):
        """
        Resolve the value of names to IPFS.

        Args:
            name: The name to resolve
            **kwargs: Optional arguments:
                recursive: bool - Resolve until the result is not an IPNS name
                dht-record-count: int - Number of records to request for DHT
                dht-timeout: str - Max time to collect values

        Returns:
            Dict with resolved path
        """
        params = {"arg": name, **kwargs}
        return self._make_request('resolve', params=params)

    def shutdown(self):
        """
        Shut down the IPFS daemon.

        Returns:
            Operation result
        """
        return self._make_request('shutdown')

    def stats_bw(self, **kwargs):
        """
        Print IPFS bandwidth information.

        Args:
            **kwargs: Optional arguments:
                peer: str - Specify a peer to print bandwidth for
                proto: str - Specify a protocol to print bandwidth for
                poll: bool - Print bandwidth at an interval
                interval: str - Time interval between updates if 'poll' is true

        Returns:
            Dict with bandwidth stats
        """
        return self._make_request('stats/bw', params=kwargs)

    def stats_bitswap(self, **kwargs):
        """
        Show diagnostic information on the bitswap agent.

        Args:
            **kwargs: Optional arguments:
                verbose: bool - Print extra information
                human: bool - Print sizes in human readable format

        Returns:
            Dict with bitswap stats
        """
        return self._make_request('stats/bitswap', params=kwargs)

    def stats_dht(self, dht=None):
        """
        Returns statistics about the node's DHT(s).

        Args:
            dht: The DHT to get stats for (wan/lan/etc)

        Returns:
            Dict with DHT stats
        """
        params = {}
        if dht:
            params["arg"] = dht
        return self._make_request('stats/dht', params=params)

    def stats_provide(self):
        """
        Returns statistics about the node's (re)provider system.

        Returns:
            Dict with provider stats
        """
        return self._make_request('stats/provide')

    def stats_repo(self, **kwargs):
        """
        Get stats for the currently used repo.

        Args:
            **kwargs: Optional arguments:
                size-only: bool - Only report RepoSize and StorageMax
                human: bool - Print sizes in human readable format

        Returns:
            Dict with repo stats
        """
        return self._make_request('stats/repo', params=kwargs)

    # Swarm API

    def swarm_addrs(self):
        """
        List known addresses.

        Returns:
            Dict with peer addresses
        """
        return self._make_request('swarm/addrs')

    def swarm_addrs_listen(self):
        """
        List interface listening addresses.

        Returns:
            Dict with listening addresses
        """
        return self._make_request('swarm/addrs/listen')

    def swarm_addrs_local(self, **kwargs):
        """
        List local addresses.

        Args:
            **kwargs: Optional arguments:
                id: bool - Show peer ID in addresses

        Returns:
            Dict with local addresses
        """
        return self._make_request('swarm/addrs/local', params=kwargs)

    def swarm_connect(self, address):
        """
        Open connection to a given peer.

        Args:
            address: Address of peer to connect to

        Returns:
            Dict with connection result
        """
        params = {"arg": address}
        return self._make_request('swarm/connect', params=params)

    def swarm_disconnect(self, address):
        """
        Close connection to a given address.

        Args:
            address: Address of peer to disconnect from

        Returns:
            Dict with disconnect result
        """
        params = {"arg": address}
        return self._make_request('swarm/disconnect', params=params)

    def swarm_filters(self):
        """
        Manipulate address filters.

        Returns:
            Dict with address filters
        """
        return self._make_request('swarm/filters')

    def swarm_filters_add(self, address):
        """
        Add an address filter.

        Args:
            address: Multiaddr to filter

        Returns:
            Dict with operation result
        """
        params = {"arg": address}
        return self._make_request('swarm/filters/add', params=params)

    def swarm_filters_rm(self, address):
        """
        Remove an address filter.

        Args:
            address: Multiaddr filter to remove

        Returns:
            Dict with operation result
        """
        params = {"arg": address}
        return self._make_request('swarm/filters/rm', params=params)

    def swarm_peers(self, **kwargs):
        """
        List peers with open connections.

        Args:
            **kwargs: Optional arguments:
                verbose: bool - Show all information
                streams: bool - Show information about open streams
                latency: bool - Show information about latency
                direction: bool - Show information about connection direction

        Returns:
            Dict with peer information
        """
        return self._make_request('swarm/peers', params=kwargs)

    def swarm_peering_add(self, address):
        """
        Add peers into the peering subsystem.

        Args:
            address: Address of peer to add to peering subsystem

        Returns:
            Dict with operation result
        """
        params = {"arg": address}
        return self._make_request('swarm/peering/add', params=params)

    def swarm_peering_ls(self):
        """
        List peers registered in the peering subsystem.

        Returns:
            Dict with peered peers
        """
        return self._make_request('swarm/peering/ls')

    def swarm_peering_rm(self, peer_id):
        """
        Remove a peer from the peering subsystem.

        Args:
            peer_id: ID of peer to remove

        Returns:
            Dict with operation result
        """
        params = {"arg": peer_id}
        return self._make_request('swarm/peering/rm', params=params)

    def swarm_resources(self):
        """
        EXPERIMENTAL: Get resource usage info.

        Returns:
            Resource manager information
        """
        return self._make_request('swarm/resources')

    # Version API

    def version(self, **kwargs):
        """
        Show IPFS version information.

        Args:
            **kwargs: Optional arguments:
                number: bool - Only show version number
                commit: bool - Show the commit hash
                repo: bool - Show repo version
                all: bool - Show all version information

        Returns:
            Dict with version information
        """
        return self._make_request('version', params=kwargs)

    def version_check(self, **kwargs):
        """
        Check Kubo version against connected peers.

        Args:
            **kwargs: Optional arguments:
                min-percent: int - Percentage of peers needed to trigger warning

        Returns:
            Dict with version check result
        """
        return self._make_request('version/check', params=kwargs)

    def version_deps(self):
        """
        Shows information about dependencies used for build.

        Returns:
            Dict with dependency information
        """
        return self._make_request('version/deps')

    # Routing API (formerly DHT API)

    def routing_findpeer(self, peer_id, **kwargs):
        """
        Find the multiaddresses associated with a Peer ID.

        Args:
            peer_id: The ID of the peer to search for
            **kwargs: Optional arguments:
                verbose: bool - Print extra information

        Returns:
            Dict with found peer information
        """
        params = {"arg": peer_id, **kwargs}
        return self._make_request('routing/findpeer', params=params)

    def routing_findprovs(self, key, **kwargs):
        """
        Find peers that can provide a specific value.

        Args:
            key: The key to find providers for
            **kwargs: Optional arguments:
                verbose: bool - Print extra information
                num-providers: int - The number of providers to find

        Returns:
            Dict with providers
        """
        params = {"arg": key, **kwargs}
        return self._make_request('routing/findprovs', params=params)

    def routing_get(self, key):
        """
        EXPERIMENTAL: Given a key, query the routing system for its best value.

        Args:
            key: The key to find a value for

        Returns:
            Dict with retrieved value
        """
        params = {"arg": key}
        return self._make_request('routing/get', params=params)

    def routing_provide(self, key, **kwargs):
        """
        EXPERIMENTAL: Announce to the network that you are providing values.

        Args:
            key: The key to announce
            **kwargs: Optional arguments:
                verbose: bool - Print extra information
                recursive: bool - Recursively provide entire graph

        Returns:
            Dict with operation result
        """
        params = {"arg": key, **kwargs}
        return self._make_request('routing/provide', params=params)

    def routing_put(self, key, value, **kwargs):
        """
        EXPERIMENTAL: Write a key/value pair to the routing system.

        Args:
            key: The key to store
            value: The value to store
            **kwargs: Optional arguments:
                allow-offline: bool - Save record to datastore without broadcasting

        Returns:
            Dict with operation result
        """
        params = {"arg": key, **kwargs}
        files = self._prepare_files('value-file', value)
        return self._make_request('routing/put', files=files, params=params)

    def routing_reprovide(self):
        """
        EXPERIMENTAL: Trigger reprovider.

        Returns:
            Operation result
        """
        return self._make_request('routing/reprovide')
