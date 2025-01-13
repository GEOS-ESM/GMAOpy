import subprocess
import re
from semperpy.archive.archive import Archive

class DMF(Archive):

    path_ = '/usr/bin'

    @classmethod
    def setCommandPath(self,path):
        DMF.path_ = path

    def do_stage(self,stagelist,output=subprocess.PIPE):
        self.execute_command('dmget','-v','\n'.join(stagelist),output)

    def do_copy(self,filename,destination):
        pass

    def offline(self,filelist):
        out = self.execute_command('dmattr','-a state','\n'.join(filelist))
        output = self.split_output(filelist,out)
        result = []
        for i in range(len(filelist)):
            file = output[i]
            if not file == '':
                if not (re.search('DUL',file) or re.search('not available',file)):
                    result.append(filelist[i])
        return result

    def filesize(self,filelist):
        if len(filelist) == 0:
            return [0]
        out = self.execute_command('dmattr','-a size','\n'.join(filelist))
        output = self.split_output(filelist,out)
        result = [0] * len(output)
        for i in range(len(output)):
            file = output[i]
            value = re.search('(\d+)',file)
            if value is None or len(value.groups()) > 1:
                raise SystemError('Calling "dmattr -a size %s" returned an invalid result' % filename)
            else:
                result[i] = int(value.groups()[0])
        return result

    def split_output(self,filelist,output):
        # get rid of the last newline
        output = output[0:-1]
        all = output.split('\n')
        if len(all) != len(filelist):
            raise SystemError('The DMF command returned a result which is inconsistent with what is expected, perhap one of the files specified in not handled by the DMF')
        return all

    def execute_command(self,cmd,options,argument,output=subprocess.PIPE):
        args = ('',options)
        if len(options) == 0:
            args = ('')
        child = subprocess.Popen((self.path_ + '/' + cmd,options),stdin=subprocess.PIPE,stdout=output,stderr=output,text=True)
        out,err = child.communicate(input = argument + '\n')
        error = child.returncode
        if (error != 0):
            raise ValueError("The command %s failed with error: %s" % (cmd,str(error)))
        return out

Archive.register('dmf',DMF)
