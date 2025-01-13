from gmaopy.hooks.datahook import DataHook

class InfoHook(DataHook):

    @classmethod
    def usage(self):
        return ['infohook does not take any arguments']

    def __call__(self,main_variable,data):
        print(data[0])

infohook = InfoHook

DataHook.registerHook('infohook',InfoHook)
