from supervisor.dispatchers import RejectEvent
from supervisor_twiddler.compat import unicode, basestring

def stdin_write_handler(event, response):
    """ A supervisor eventlistener result handler that accepts a
    special 'STDIN:' result and writes what follows to the STDIN
    of the process associated with the event. """
    if response.startswith("STDIN:"):
        _stdin_write(event.process, response[6:])
    elif response != 'OK':
        raise RejectEvent(response)

def _stdin_write(process, chars):
    """ Write chars to the stdin of process.  If the process is
    not running or another error occurs, there is not anything we
    can do so just return False. """
    if isinstance(chars, unicode):
        chars = chars.encode('utf-8')

    if not isinstance(chars, basestring):
        return False

    if not process.pid or process.killing:
        return False

    try:
        process.write(chars)
    except OSError:
        return False

    return True
