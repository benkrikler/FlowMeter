class BaseProduct(object):
    def __init__(self):
        pass
    def ProcessData(self,flowData):
        raise NotImplementedError( 
                "ProcessData() is not implemented for " +self.__class__.__name__)

class BaseOutput(object):
    def __init__(self,product_dependencies):
        self.product_dependencies=[]
        self.product_dependencies+=product_dependencies
    def CompileOutput(self,flows,config, products):
        raise NotImplementedError( 
                "CompileOutput() is not implemented for " +self.__class__.__name__)
