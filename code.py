import vtk

# path to the stored images
path = r'CT'

# Read data
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName(path)
reader.Update()

# Create colour transfer function
colorFunc = vtk.vtkColorTransferFunction()
colorFunc.AddRGBPoint(-1024, 0.0, 0.0, 0.0)
colorFunc.AddRGBPoint(-77, 0.5, 0.2, 0.1)
colorFunc.AddRGBPoint(100, 0.9, 0.6, 0.3)
colorFunc.AddRGBPoint(180, 1, 0.8, 0.9)
colorFunc.AddRGBPoint(260, 0.6, 0.1, 0)
colorFunc.AddRGBPoint(3071, 0.7, 0.8, 1)

# Create opacity transfer function
alphaChannelFunc = vtk.vtkPiecewiseFunction()
alphaChannelFunc.AddPoint(-1024, 0.0)
alphaChannelFunc.AddPoint(-77, 0.0)
alphaChannelFunc.AddPoint(179, 0.1)
alphaChannelFunc.AddPoint(260, 0.4)
alphaChannelFunc.AddPoint(3071, 0.7)

# View 1 for volume
volume1 = vtk.vtkVolume()
ren1 = vtk.vtkRenderer()
txt1 = vtk.vtkTextActor()
txt1.SetInput("Volume rendering!")
txtprop=txt1.GetTextProperty()
txtprop.SetFontFamilyToArial()
txtprop.SetFontSize(18)
txtprop.SetColor(1,1,1)

# Define volume mapper
volumeMapper1 = vtk.vtkSmartVolumeMapper()  
volumeMapper1.SetInputConnection(reader.GetOutputPort())

# Define volume properties
volumeProperty1 = vtk.vtkVolumeProperty()
volumeProperty1.SetScalarOpacity(alphaChannelFunc)
volumeProperty1.SetColor(colorFunc)
volumeProperty1.ShadeOn()

# Set the mapper and volume properties
volume1.SetMapper(volumeMapper1)
volume1.SetProperty(volumeProperty1)

# create volume renderer
ren1.AddVolume(volume1)
ren1.AddActor(txt1) 


###############################################################################
# View 2 for ISO mapper
ren2 = vtk.vtkRenderer()
txt2 = vtk.vtkTextActor()
txt2.SetInput("ISO rendering!")
txtprop=txt2.GetTextProperty()
txtprop.SetFontFamilyToArial()
txtprop.SetFontSize(18)
txtprop.SetColor(1,1,1)

# Apply Marching Cubes algorithm
march_cubes = vtk.vtkMarchingCubes()
march_cubes.SetInputConnection(reader.GetOutputPort())
march_cubes.ComputeNormalsOn()
march_cubes.ComputeGradientsOn()
march_cubes.SetValue(0,260)
march_cubes.Update()

# Polydata mapper for the iso-surface
isoMapper = vtk.vtkPolyDataMapper()
isoMapper.SetInputConnection(march_cubes.GetOutputPort())
isoMapper.ScalarVisibilityOff()

# Actor for the iso surface
isoActor = vtk.vtkActor()
isoActor.SetMapper(isoMapper)
isoActor.GetProperty().SetColor(1.0,1.0,1.0)

# create iso metric renderer
ren2.AddActor(isoActor)
ren2.AddActor(txt2)


###############################################################################
# View 3 for Volume+Iso mapping
ren3 = vtk.vtkRenderer()
txt3 = vtk.vtkTextActor()
txt3.SetInput("ISO & Volume rendering!")
txtprop=txt3.GetTextProperty()
txtprop.SetFontFamilyToArial()
txtprop.SetFontSize(18)
txtprop.SetColor(1,1,1)

# create a renderer for both volume as well as iso mapper
ren3.AddVolume(volume1)
ren3.AddActor(isoActor)
ren3.AddActor(txt3)


###############################################################################

# Render the scenes into 3 different viewports
ren1.SetViewport(0, 0, 0.33, 1)    # viewport 1   
ren2.SetViewport(0.33, 0, 0.66, 1) # viewport 2
ren3.SetViewport(0.66, 0, 1, 1)    # viewport 3

# Rendering
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren1) # renders the volume mapper
renWin.AddRenderer(ren2) # renders the iso mapper
renWin.AddRenderer(ren3) # renders both volume and iso mapper

# the render window size for 16:9 display
renWin.SetSize(1920,1080)
renWin.Render()
 
# The window interactor
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# syncing the viewports to first renderer
camera = ren1.GetActiveCamera()
ren1.ResetCamera()
ren2.SetActiveCamera(camera)
ren3.SetActiveCamera(camera)

# pixel intensities
maximum_minimum = reader.GetOutput().GetScalarRange()
print('the intensities are: ', maximum_minimum)
# Dimension and voxel resolution
dimension_voxel = reader.GetOutput(0)
print(dimension_voxel)

iren.Initialize() 
iren.Start()
