from semperpy.archive.archive import Archive

class FileSystem(Archive):

    def do_stage(self,stagelist):
        pass

    def do_copy(self,filename,destination):
        pass

    def offline(self,filelist):
        return []

    def filesize(self,filelist):
        pass

    def do_copy(self,filelist,destination):
        pass

Archive.register('filesystem',FileSystem)
