import sys
import unittest
import supervisor_twiddler
import supervisor_twiddler.resulthandler
from supervisor_twiddler.compat import _b, _u
from supervisor.tests.base import DummyEvent, DummyOptions, DummyPConfig, DummyProcess
from supervisor.dispatchers import RejectEvent

class TestStdinWriteHandler(unittest.TestCase):
    def test_handler_does_nothing_when_response_is_OK(self):
        event = DummyEvent()
        response = 'OK'
        supervisor_twiddler.resulthandler.stdin_write_handler(event, response)

    def test_handler_rejects_event_when_response_is_unexpected(self):
        event = DummyEvent()
        response = 'unexpected'
        self.assertRaises(RejectEvent,
                          supervisor_twiddler.resulthandler.stdin_write_handler,
                          event, response)

    def test_handler_writes_chars_when_response_is_STDIN(self):
        options = DummyOptions()
        config = DummyPConfig(options, 'cat', 'bin/cat')

        process = DummyProcess(config)
        process.pid = 42
        process.killing = False

        event = DummyEvent()
        event.process = process

        response = 'STDIN:foobar'
        supervisor_twiddler.resulthandler.stdin_write_handler(event, response)
        self.assertEqual(process.stdin_buffer, 'foobar')

    def test_write_encodes_unicode_as_utf8(self):
        options = DummyOptions()
        config = DummyPConfig(options, 'cat', 'bin/cat')

        process = DummyProcess(config)
        process.pid = 42
        process.killing = False

        event = DummyEvent()
        event.process = process

        response = _u(_b('STDIN:foobar'))
        supervisor_twiddler.resulthandler.stdin_write_handler(event, response)
        self.assertEqual(process.stdin_buffer, 'foobar')

    def test_write_fails_silently_if_process_has_no_pid(self):
        options = DummyOptions()
        config = DummyPConfig(options, 'cat', 'bin/cat')

        process = DummyProcess(config)
        process.pid = None
        process.killing = False

        event = DummyEvent()
        event.process = process

        response = 'STDIN:foobar'
        supervisor_twiddler.resulthandler.stdin_write_handler(event, response)
        self.assertEqual(process.stdin_buffer, '')

    def test_write_fails_silently_if_process_is_killing(self):
        options = DummyOptions()
        config = DummyPConfig(options, 'cat', 'bin/cat')

        process = DummyProcess(config)
        process.pid = 42
        process.killing = True

        event = DummyEvent()
        event.process = process

        response = 'STDIN:foobar'
        supervisor_twiddler.resulthandler.stdin_write_handler(event, response)
        self.assertEqual(process.stdin_buffer, '')

    def test_write_fails_silently_if_oserror_during_write(self):
        options = DummyOptions()
        config = DummyPConfig(options, 'cat', 'bin/cat')

        process = DummyProcess(config)
        process.pid = 42
        process.killing = False
        process.write_error = True

        event = DummyEvent()
        event.process = process

        response = 'STDIN:foobar'
        supervisor_twiddler.resulthandler.stdin_write_handler(event, response)
        self.assertEqual(process.stdin_buffer, '')

def test_suite():
    return unittest.findTestCases(sys.modules[__name__])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
