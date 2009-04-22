# supervisor_cache

This package is an RPC extension for [Supervisor](http://supervisord.org) 
that allows Supervisor's configuration and state to be manipulated in ways 
that are not normally possible at runtime.

## Installation

[Download](http://github.com/mnaberez/supervisor_twiddler/downloads) and
extract, then install to Python's `site-packages`:

    $ python setup.py install
    
After installing the package, you must modify your `supervisord.conf` file 
to register the twiddler interface:

    [rpcinterface:twiddler]
    supervisor.rpcinterface_factory = supervisor_twiddler.rpcinterface:make_twiddler_rpcinterface

After modifying the `supervisord.conf` file, your Supervisor instance must be
restarted for the twiddler interface to be loaded.

## Usage

Normally, supervisord's configuration (specified in `supervisord.conf`) cannot
be changed after supervisord has been started. For changes in `supervisord.conf`
to take effect, supervisord must be restarted.

There are times when it is useful to be able to dynamically add and remove
process configurations on a supervisord instance. This is the functionality
that supervisor_twiddler provides. After restarting supervisord, the changes
made by supervisor_twiddler will not persist.

The following Python interpreter session demonstrates the usage.

First, a `ServerProxy` object must be configured. If supervisord is listening on
an inet socket, `ServerProxy` configuration is simple:

    >>> import xmlrpclib
    >>> s = xmlrpclib.ServerProxy('http://localhost:9001')

If supervisord is listening on a domain socket, `ServerProxy` can be configured
with `SupervisorTransport`. The URL must still be supplied and be a valid HTTP
URL to appease ServerProxy, but it is superfluous.

    >>> import xmlrpclib
    >>> from supervisor.xmlrpc import SupervisorTransport
    >>> s = xmlrpclib.ServerProxy('http://127.0.0.1/whatever', 
    ... SupervisorTransport('', '', 'unix:///path/to/supervisor.sock'))

Once `ServerProxy` has been configured appropriately, we can now exercise
supervisor_twiddler:

    >>> s.twiddler.getAPIVersion()
    '0.1'
    >>> s.twiddler.addGroup('dynamic_procs', 999)
    True
    >>> s.twiddler.addProgramToGroup('dynamic_procs', 'ls', {'command':'ls -l', 
    ... 'autostart':'false', 'autorestart':'false', 'startsecs':'0'})
    True
    >>> s.supervisor.startProcess('dynamic_procs:ls')
    True
    >>> s.supervisor.readProcessLog('dynamic_procs:ls', 0, 50)
    'total 0
    drwxr-xr-x   9 mnaberez  mnaberez  306 Nov'

In the session above, a new process group called `dynamic_procs` was created and
a process called `ls` was added to it.

The process was configured to not start automatically (`autostart`), not restart
automatically (`autorestart`), and `startsecs` was set to zero so Supervisor would
not think its quick termination was an error.

The process was then started and its output read using the normal API commands
provided by Supervisor.

## Warnings

Any changes to the supervisord runtime configuration will not be persisted
after Supervisor is shut down.

Your Supervisor instance should never be exposed to the outside world. With
supervisor_twiddler, anyone with access to the API has the ability to run
arbitrary commands on the server.

### Author

[Mike Naberezny](http://github.com/mnaberez)
