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

Author Information

  Mike Naberezny (mike@maintainable.com)
  "Maintainable Software":http://www.maintainable.com
