# ------------------------------------------------------------------------------
# Converts a .vtk from the microstructure-solver into a .mat fwormat for MATLAB
# reading
# ------------------------------------------------------------------------------
import numpy
from vtk import vtkUnstructuredGridReader
from vtk.util import numpy_support as VN
from scipy.io import savemat


## User specification ==========================================================
filename = 'output/000/Microstructure_YZ.vtk'
outputname = 'auto'
# ==============================================================================
# Read in the file
reader = vtkUnstructuredGridReader()
reader.SetFileName(filename)
reader.ReadAllScalarsOn()
reader.Update()
data = reader.GetOutput()

# Save point data arrays into a dictionary
pointData = data.GetPointData()
nArrays = pointData.GetNumberOfArrays()
names   = [pointData.GetArrayName(i) for i in range(nArrays)]
coords  = data.GetPoints().GetData()
dict    = {'coords':VN.vtk_to_numpy(coords)}
for (i, name) in enumerate(names):
    dict[name] = VN.vtk_to_numpy(pointData.GetArray(name))

print(dir(coords))
# Convert dictionary to .mat file
if outputname == 'auto':
    tokens = filename.split('/')
    tokens = tokens[-1].split('.')
    outputname = tokens[0] + '.mat'

savemat(outputname, dict)
