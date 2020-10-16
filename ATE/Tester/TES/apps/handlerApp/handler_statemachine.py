from transitions import Machine
from enum import Enum


class States(Enum):
    startup = 'startup'
    connecting = 'connecting'
    initialized = 'initialized'
    loading = 'loading'
    ready = 'ready'
    testing = 'testing'
    unloading = 'unloading'
    error = 'error'

    @classmethod
    def list(cls):
        return [x.value for x in list(cls)]

    def __call__(self):
        return self.value


class HandlerStateMachine(Machine):
    transistions = [{'source': States.startup,        'dest': States.connecting,      'trigger': 'startup_done'},          # noqa: E241
                    {'source': States.connecting,     'dest': States.initialized,     'trigger': 'master_connected'},      # noqa: E241
                    {'source': States.initialized,    'dest': States.loading,         'trigger': 'master_loading'},        # noqa: E241
                    {'source': States.loading,        'dest': States.ready,           'trigger': 'master_load_done'},      # noqa: E241
                    {'source': States.ready,          'dest': States.testing,         'trigger': 'master_testing'},        # noqa: E241
                    {'source': States.testing,        'dest': States.ready,           'trigger': 'master_testing_done'},   # noqa: E241
                    {'source': States.ready,          'dest': States.unloading,       'trigger': 'master_unload'},         # noqa: E241
                    {'source': States.unloading,      'dest': States.initialized,     'trigger': 'master_initialized'},    # noqa: E241

                    {'source': States.startup,        'dest': States.error,           'trigger': 'on_error'},              # noqa: E241
                    {'source': States.connecting,    'dest': States.error,           'trigger': 'on_error'},               # noqa: E241
                    {'source': States.initialized,   'dest': States.error,           'trigger': 'on_error'},               # noqa: E241
                    {'source': States.ready,         'dest': States.error,           'trigger': 'on_error'},               # noqa: E241
                    {'source': States.testing,       'dest': States.error,           'trigger': 'on_error'},               # noqa: E241
                    {'source': States.unloading,     'dest': States.error,           'trigger': 'on_error'}]               # noqa: E241

    def __init__(self):
        self._machine = Machine(model=self,
                                states=States.list(),
                                transitions=self.transistions,
                                initial=States.startup())

    @property
    def model(self):
        return self._machine.model

    def after_state_change(self, call_back):
        self._machine.after_state_change = call_back
