import pandas as pd

class Data:

    def __init__(self):
        
        # import excel file
        df = pd.read_excel('CleanData.xlsx', header=None, sheet_name="Customer classes and routing")

        # set black entries to 0
        df = df.replace('black', 0).fillna(0)

        # import routing matrices and turn into arrays
        self.routing_matrices =[]

        flam_pap_cloth = df.iloc[5:11,2:8].values
        self.routing_matrices.append(flam_pap_cloth)

        flam_wood_metal = df.iloc[16:22,2:8].values
        self.routing_matrices.append(flam_wood_metal)

        flam = df.iloc[27:33,2:8].values
        self.routing_matrices.append(flam)

        flam_pap = df.iloc[38:44,2:8].values
        self.routing_matrices.append(flam_pap)

        flam_chem_pap_electr = df.iloc[49:55,2:8].values
        self.routing_matrices.append(flam_chem_pap_electr)

        green = df.iloc[60:66,2:8].values
        self.routing_matrices.append(green)

        flam_wood_chem_pap = df.iloc[71:77,2:8].values
        self.routing_matrices.append(flam_wood_chem_pap)

        wood = df.iloc[82:88,2:8].values
        self.routing_matrices.append(wood)

        wood_carpet = df.iloc[93:99,2:8].values
        self.routing_matrices.append(wood_carpet)

        debris = df.iloc[104:110,2:8].values
        self.routing_matrices.append(debris)

        flam_wood_metal_matt_pap_electr = df.iloc[115:121,2:8].values
        self.routing_matrices.append(flam_wood_metal_matt_pap_electr)
        
        self.loc = {'Gate': 1, 'FWPM': 2, 'DcDdGpCh': 3, 'GrWcTEGs': 4, 'Rest': 5}

    def getMatrix(self,n):
        return self.routing_matrices[n]
    
    def getLocation(self, location):
        
        return self.loc[location]
    
data = Data()
data.getLocation('DcDdGpCh')
