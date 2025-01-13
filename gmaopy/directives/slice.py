from gmaopy.directives.retrieve import Retrieve

class Slice(Retrieve):

    def return_fieldset(self):
        return False

    def use_intervals(self):
        return True

    def name(self):
        return 'retrieve'

slice = Slice
