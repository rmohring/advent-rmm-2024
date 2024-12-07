import numpy as np

class Gridder:
    def __init__(self, data=None, T=False, flip=None):
        if data is None:
            self.grid = []
        else:
            if isinstance(data, np.ndarray):
                self.grid = data.copy()        
            elif isinstance(data, (list, tuple)):
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
            

    def addrow(self, row, strip=False):
        self.columnar_build = False
        if strip:
            r = row.strip("\n")
        else:
            r = row
        self.grid.append(list(r))

    def addcol(self, row, strip=False):
        self.columnar_build = True
        self.addrow(row, strip=strip)
            
    def done_building(self):
        self.grid = np.array(self.grid)
        if self.columnar_build:
            self.grid = self.grid.T
    
    def integerize(self):
        self.grid = self.grid.astype(int)

    def tolist(self):
        return self.grid.tolist()
    
    def val(self, tup):
        return self.grid[tup[0],tup[1]]
    
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
    
    def __str__(self):
        return ("\n".join(("".join(x) for x in self.grid.tolist())))
        