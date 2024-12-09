import numpy as np

class Gridder:
    def __init__(self, data=None, shape=None, T=False, flip=None, from_text=False, strip=True): #, columnar_build=False):
        if data is None:
            if shape is not None:
                self.grid = np.full(shape, ".")
            else:
                self.grid = []
        else:
            if isinstance(data, np.ndarray):
                self.grid = data.copy()        
            elif isinstance(data, (list, tuple)):
                if from_text:
                    self.grid = self.build_from_text(data, strip=strip) #, columnar_build=columnar_build)
                else:
                    self.grid = np.array(data)
            elif isinstance(data, Gridder):
                self.grid = data.grid.copy()
            
            if T:
                self.grid = self.grid.T
                
            if flip is not None:
                if flip == 'ud':
                    self.grid = np.flipud(self.grid)
                elif flip == 'lr':
                    self.grid = np.fliplr(self.grid)
                else:
                    raise ValueError("flip unknown")

        #self.columnar_build = columnar_build
        self.backup = self.grid.copy()    

    def build_from_text(self, data, strip=True): #, columnar_build=False, ):
        d = []
        for row in data:
            if strip:
                r = row.strip("\n")
            else:
                r = row
            d.append(list(r))
        
        return np.array(d)
        
    # def addrow(self, row, strip=False):
    #     self.columnar_build = False
    #     if strip:
    #         r = row.strip("\n")
    #     else:
    #         r = row
    #     self.grid.append(list(r))

    # def addcol(self, row, strip=False):
    #     self.columnar_build = True
    #     self.addrow(row, strip=strip)
            
    # def done_building(self):
    #     self.grid = np.array(self.grid)
    #     if self.columnar_build:
    #         self.grid = self.grid.T
    
    def integerize(self):
        self.grid = self.grid.astype(int)

    def tolist(self):
        return self.grid.tolist()

    def setvals(self, tuplist, val):
        for x in tuplist:
            self.setval(x, val)
        
    def setval(self, tup, val):
        self.grid[tup[0],tup[1]] = val

    def val(self, tup):
        return self.grid[tup[0],tup[1]]

    def is_offgrid(self, rc):
        return (rc[0]<0) or (rc[0]>=self.grid.shape[0]) or (rc[1]<0) or (rc[1]>=self.grid.shape[1])

    def is_ongrid(self, rc):
        return not self.is_offgrid(rc)

    def reset(self):
        self.grid = self.backup.copy()
    
    @property
    def shape(self):
        return self.grid.shape
    
    @property
    def T(self):
        return self.grid.T        

    @property
    def flipud(self):
        return np.flipud(self.grid)

    @property
    def fliplr(self):
        return np.fliplr(self.grid)

    @property
    def nrows(self):
        return self.grid.shape[0]
    
    @property
    def ncols(self):
        return self.grid.shape[1] 

    @property
    def rows(self):
        return [x.tolist() for x in self.grid]

    @property
    def cols(self):
        return [x.tolist() for x in self.grid.T]

    @property
    def erows(self):
        return enumerate(self.rows)

    @property
    def ecols(self):
        return enumerate(self.cols)
    
    def pretty(self, sep=""):
        return ("\n".join((sep.join(x) for x in self.grid.tolist())))

    def pp(self, sep=""):
        print(self.pretty(sep=sep))
        return
    
    def __str__(self):
        return ("\n".join(("".join(x) for x in self.grid.tolist())))
        