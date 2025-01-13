from semperpy.core.tools import to_list, mergedicts_keep
from semperpy.fields.fieldset import FieldSet
from semperpy.fields.field import Field
from semperpy.fields.containers.slicecontainer import SliceContainer

class FieldCreator(object):

    def __call__(self,slices,metadata,**kargs):
        args = mergedicts_keep(metadata,kargs)
        shape = [ len(to_list(metadata[x])) for x in self.dimensions_ ]
        self.collection_.append(Field(SliceContainer(self.source_,slices,shape),self.dimensions_,args))

    def preProcess(self,dimensions,source,shape,slices,metadata):
        self.collection_ = FieldSet()
        self.dimensions_ = [ x.officialName() for x in dimensions ]
        self.source_ = source

    def postProcess(self,dimensions,source,shape,slices,metadata):
        pass

    def fieldSet(self,new = None):
        if new:
            self.collection_ = new
        return self.collection_
