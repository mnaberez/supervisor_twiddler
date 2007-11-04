supervisor_twiddler:
  This package is an RPC extension for the supervisor2 package that
  facilitates manipulation of supervisor's configuration and state in ways	
  that are not normally accessible at runtime.

History
 
  Not yet released.

Installation

  After installing the package with the usual `python setup.py install`, you
  need to modify your supervisord.conf file to register the twiddler interface:
  
  [rpcinterface:twiddler]
  supervisor.rpcinterface_factory = supervisor_twiddler.rpcinterface:make_twiddler_rpcinterface  

  After modifying the supervisord.conf file, your supervisor instance must be
  restarted for the cache interface to be loaded.  

Usage

  Normally, supervisord's configuration (specified in supervisord.conf) cannot
  be changed after supervisord has been started.  For changes in supervisord.conf
  to take effect, supervisord must be restarted.
  
  There are times when it is useful to be able to dynamically add and remove
  process configurations on a supervisord instance. This is the functionality
  that supervisor_twiddler provides. After restarting supervisord, the changes
  made by supervisor_twiddler will not persist.

  This Python interpreter session demonstrates the usage:
  
  >>> from xmlrpclib import Server
  >>> s = Server('http://localhost:9001')
  >>> s.twiddler.getAPIVersion()
  '1.0'
  >>> s.twiddler.addGroup('dynamic_procs', 999)
  True
  >>> s.twiddler.addProcessToGroup('dynamic_procs', 'ls', {'command':'ls -l', 
  ... 'autostart':'false', 'autorestart':'false', 'startsecs':'0'})
  True
  >>> s.supervisor.startProcess('dynamic_procs:ls')
  True
  >>> s.supervisor.readProcessLog('dynamic_procs:ls', 0, 50)
  'total 0\ndrwxr-xr-x   9 mnaberez  mnaberez  306 Nov'

  In the session above, a new process group called "dynamic_procs" was created
  and a process called "ls" was added to it.  
  
  The process was configured to not start automatically ("autostart"), not
  restart automatically ("autorestart"), and "startsecs" was set to zero so
  Supervisor would not think its quick termination was an error.
  
  The process was then started and its output read using the normal API commands 
  provided by Supervisor.

API

  Testing the API Version
  
    All supervisord RPC extensions follow a convention where a method called
    getAPIVersion() is available.  supervisor_twiddler provides this:
    
    twiddler.getAPIVersion()
    
    It is highly recommended that when you develop software that uses 
    supervisor_twiddler, you test the API version before making method calls.
    Since this is alpha-quality software, it's very likely that the API will 
    change.  Testing it will help keep you out of trouble.

  Listing Process Groups
    
    Process groups are defined in supervisord.conf as "group" sections.
    Assume supervisord.conf contained sections [group:foo] and [group:bar]:
    
    twiddler.getGroupNames()
    
    The return value would then return an array: ["foo", "bar"].  It is possible
    to use supervisor_twiddler to add new process groups at runtime, and these
    will also be included in the results returned by twiddler.getGroupNames().

  Adding Process Groups
  
    It is possible to add empty process groups by specifying empty [group:foo]
    sections in supervisord.conf with no "programs=" entries under them.
    However, it is not possible to add new empty process groups after
    supervisord has been started.

    The twiddler.addGroup() method adds an empty process group.  It takes two
    parameters: the name of the new group as a string, and its priority as an
    integer:
    
    twiddler.addGroup("foos", 999)

    The first parameter ("foos") is the name of the new process group.  The
    second parameter (999) is the group's priority, like in supervisord.conf.

    The method call above will create a new, empty process group named "foos".
    You can then populate this group with processes using
    twidder.addProcessToGroup().

    It is not yet possible to remove a process group, but this is planned
    for a future release of supervisor_twiddler.

  Adding a New Process to a Group
  
    It is possible to add new processes to a group and then control those
    processes as if they had existed originally in supervisord.conf.
    
    twiddler.addProcessToGroup("group_name", "foo", {"command": "/usr/bin/foo"})

    The first parameter ("group_name") is the group name where the new process
    will belong. While there is no restriction on what groups can be used, it
    is recommended that you keep your supervisord.conf groups static.  You can 
    add new process groups just for your dynamic processes, and this will help 
    you track them easier.

    The second parameter ("foo") is the name of the new process to add to the
    group.  The name must not already be present in the group.
    
    The final parameter is a dict (XML-RPC "struct") containing the program
    options.  These are the same options as in the supervisor.conf program
    section and follow the same rules.  The only required key is "command".
    
    When you add a process in this way and do not specify the "autostart"
    option, the process will start on the next transition of Supervisor's
    state machine (almost immediately).  You might want to set "autostart"
    to "false" and then start the process with supervisor.startProcess().
    
    Similarly, you might want to set "autorestart" to "false" if you don't
    want Supervisor to restart it immediately after it exits.

    If the process you are adding exits quickly, make sure that you set
    "startsecs" to 0.  Otherwise, Supervisor will think the process failed
    to start and will give an abnormal termination error.
  
  Removing a Process from a Group

    When processes are no longer needed in the supervisord runtime configuration,
    the twiddler.removeProcessFromGroup() method can be used:

    twiddler.removeProcessFromGroup("group_name", "process_name")

    To be removed, the process must not be running.  It must have terminated
    on its own or have been stopped with supervisor.stopProcess().

Warning

  Any changes to the supervisord runtime configuration will not be persisted
  after Supervisor is shut down.

  Your Supervisor instance should never be exposed to the outside world.  With
  supervisor_twiddler, anyone with access to the API has the ability to run
  arbitrary commands on the server.
  
Author Information

  Mike Naberezny (mike@maintainable.com)
  "Maintainable Software":http://www.maintainable.com
