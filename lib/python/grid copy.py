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
        self.nns = {}
        self.nns_coords = {}


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

    def val(self, tup, raise_error=True):
        if self.is_ongrid(tup):
            retval = self.grid[tup[0],tup[1]]
        else:
            if raise_error:
                raise IndexError(f"{tup} is off grid shape {self.shape}")
            else:
                retval = None
        return retval

    def is_offgrid(self, rc):
        return (rc[0]<0) or (rc[0]>=self.grid.shape[0]) or (rc[1]<0) or (rc[1]>=self.grid.shape[1])

    def is_ongrid(self, rc):
        return not self.is_offgrid(rc)

    def reset(self):
        self.grid = self.backup.copy()

    def set_nearest_neighbors(self, diag=False):
        for r in range(self.nrows):
            for c in range(self.ncols):
                self.nns[(r,c)] = self.get_nearest_neighbors( (r,c), diag=diag )
                #self.nns_coords[(r,c)] = self.get_nearest_neighbors_coords( (r,c), diag=diag)

    def get_nearest_neighbors(self, rc_tup, diag=False):
        nns = {}
        r,c = rc_tup
        for dr,dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            val = self.val( (r+dr, c+dc), raise_error=False )
            if val is not None:
                if val not in nns:
                    nns[val] = []
                nns[val].append( (r+dr, c+dc) )
        if diag:
            for dr,dc in [(1,1),(1,-1),(-1,-1),(-1,1)]:
                val = self.val( (r+dr, c+dc), raise_error=False) 
                if val is not None:
                    if val not in nns:
                        nns[val] = []                    
                    nns[val].append( (r+dr, c+dc) )
        return nns        
   
    # def get_nearest_neighbors_coords(self, rc_tup, diag=False):
    #     nns = []
    #     r,c = rc_tup
    #     for dr,dc in [(0,1),(0,-1),(1,0),(-1,0)]:
    #         val = (r+dr, c+dc)
    #         if self.is_ongrid(val):
    #             nns.append(val)
    
    #     if diag:
    #         for dr,dc in [(1,1),(1,-1),(-1,-1),(-1,1)]:
    #             val = (r+dr, c+dc)
    #             if self.is_ongrid(val):
    #                 nns.append(val)
    #     return nns 
           
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
        