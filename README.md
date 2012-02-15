# supervisor_twiddler

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

## API Description

### Testing the API Version

All RPC extensions for Supervisor follow a convention where a method called
`getAPIVersion()` is available. supervisor_twiddler provides this:

    twiddler.getAPIVersion()

It is highly recommended that when you develop software that uses
supervisor_twiddler, you test the API version before making method calls.

### Listing Process Groups

Process groups are defined in supervisord.conf as group sections. Assume
`supervisord.conf` contained sections `[group:foo]` and `[group:bar]`:

    twiddler.getGroupNames()

The return value would then return an array: `["foo", "bar"]`. It is possible
to use supervisor_twiddler to add new process groups at runtime, and these
will also be included in the results returned by `twiddler.getGroupNames()`.

### Adding a New Program to a Group

In supervisord.conf, a `[program:x]` section will result one or more processes,
depending on `numprocs` and named by `process_name`.

The `twiddler.addProgramToGroup()` method makes it possible to add a new program
to a group (resulting in one or more processes) and then control these
processes as if they had existed originally in `supervisord.conf`.

    twiddler.addProgramToGroup("group_name", "foo", 
      {"command": "/usr/bin/foo"})

The first parameter (`group_name`) is the group name where the new process will
belong. While there is no restriction on what groups can be used, it is
recommended that you keep your `supervisord.conf` groups static. You can add new
process groups just for your dynamic processes, and this will help you track
them easier.

The second parameter (`foo`) is the name of the new program to add to the group,
as it would have been written in the `[program:foo]` section `supervisord.conf`.

The final parameter is a dict (XML-RPC "struct") containing the program
options. These are the same options as in the `supervisor.conf` program section
and follow the same rules. The only required key is `command`.

When you add a program in this way and do not specify the autostart option,
the process will start on the next transition of Supervisor's state machine
(almost immediately). You might want to set autostart to `false` and then
start the process with `supervisor.startProcess()`.

Similarly, you might want to set autorestart to `false` if you don't want
Supervisor to restart it immediately after it exits.

If the process you are adding exits quickly, make sure that you set `startsecs`
to `0`. Otherwise, Supervisor will think the process failed to start and will
give an abnormal termination error.

### Removing a Process from a Group

When processes are no longer needed in the supervisord runtime configuration,
the `twiddler.removeProcessFromGroup()` method can be used:

    twiddler.removeProcessFromGroup("group_name", "process_name")

To be removed, the process must not be running. It must have terminated on its
own or have been stopped with `supervisor.stopProcess()`.

### Logging a Message

The `twiddler.log()` method allows you to write arbitrary messages to
Supervisor's main log. When you twiddle with Supervisor's configuration, this
method is useful for logging messages about what was done.

    twiddler.log("This is an informational message", "INFO")

The first argument is a string message to write to the log. The second
argument is the log level and is optional (defaults to `INFO`). The log level
may be a string or an integer.
                                                             
Log levels are defined in the supervisor.loggers module and at the time of
writing are: `CRIT` (50), `ERRO` (40), `WARN` (30), `INFO` (20), `DEBG` (10), 
`TRAC` (5), and `BLAT` (3).

## Warnings

Any changes to the supervisord runtime configuration will not be persisted
after Supervisor is shut down.

Your Supervisor instance should never be exposed to the outside world. With
supervisor_twiddler, anyone with access to the API has the ability to run
arbitrary commands on the server.

### Author

[Mike Naberezny](http://github.com/mnaberez)
