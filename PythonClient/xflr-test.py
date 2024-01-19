from xflrpy import xflrClient, enumApp, enumLineStipple, Plane, WingSection, WPolar, enumPolarType, AnalysisSettings3D, enumWPolarResult, enumAnalysisMethod

# from xflrpy import *
# ======== PROJECT MANAGEMENT ========= 

# Change these values accordingly
# Using a valid path is your responsibility
project_name = "test1.xfl"
project_path = "/home/shrike/rakshak-1/xflrpy/projects/"

xp = xflrClient(connect_timeout=100)

# load an existing project without saving the current one
# returns the current application: Xfoil/ Airfoil-design/ plane-design/ inverse-design 
app = xp.loadProject(files = project_path + project_name, save_current = False)

# set the relevant application on the gui
xp.setApp(enumApp.DIRECTDESIGN)

# Gives useful information about the mainframe class in xflr5
print(xp.state)


# =========== AIRFOIL MORPHING =============

# get a useable object for the current class
afoil = xp.getApp(enumApp.DIRECTDESIGN)

# get a specific airfoil from a dictionary of all airfoils
foilDict = afoil.foilDict["MH 60  10.08%"] 

# you can also get the airfoil through a straight function. This is faster
foil = afoil.getFoil("MH 60  10.08%")

# show some airfoil properties
print(foil) 

# Get airfoil coordinates and play with them (what?)
coords = foil.coords
print(foil.coords)
coords[10] = [0.1, 0.01]  # change the 11th coordinate to something
foil.coords = coords

# Modify foil geometry
foil.setGeom(camber = 0.03)
foil.setGeom(thickness = 0.15, camber_x = 0.27)

# change styles
ls = afoil.getLineStyle(foil.name)
ls.color = [255,0,0,255] # r,g,b,a  make it completely red
ls.stipple = enumLineStipple.DASHDOT
afoil.setLineStyle(foil.name, ls)   # set the style finally

# delete foil. why not. what's the point of all this. why are we here.
# foil.delete()


# =========== PLANE MORPHING =============

xp.setApp(enumApp.MIAREX) # set to plane design application

# Load multiple airfoils; return the design application
xp.loadProject(project_path + project_name)

miarex = xp.getApp() # Get the current application


# Create a new custom plane
plane3 = Plane(name="custom_plane")


# let's add sections to the primary wing
sec0 = WingSection(chord=0.2, right_foil_name="fuselage center", left_foil_name="fuselage center") # you might need to change airfoils accordingly
sec1 = WingSection(y_position = 1, chord=0.1, offset=0.2, twist=5, dihedral=5, right_foil_name="MH 60  10.08%", left_foil_name="MH 60  10.08%")
plane3.wing.sections.append(sec0)
plane3.wing.sections.append(sec1)


### You can also add elevators and fins, but i'll leave that for now 
# # create the elevator
# plane3.elevator.sections.append(())

# # create the fin
# plane3.fin.sections.append(())

# adds the plane to the list and tree view
miarex.plane_mgr.addPlane(plane3)

# get and print useful plane data
plane_data = miarex.plane_mgr.getPlaneData("custom_plane")
print(plane_data)


# =========== 3D ANALYSIS =============

# create a Wing Polar object
wpolar = WPolar(name="my_cute_polar", plane_name="custom_plane")
# set it's specfications
wpolar.spec.polar_type = enumPolarType.FIXEDSPEEDPOLAR
wpolar.spec.free_stream_speed = 12
wpolar.spec.analysis_method = enumAnalysisMethod.VLMMETHOD

# creates the analysis
miarex.define_analysis(wpolar=wpolar)

# these settings are on the right pane in the GUI
analysis_settings = AnalysisSettings3D(is_sequence=True, sequence=(0,10,1))

# get custom results from the analysis
results = miarex.analyze("my_cute_polar", "custom_plane2", analysis_settings, result_list=[enumWPolarResult.ALPHA, enumWPolarResult.CLCD])

print(results)
