# %% [markdown]
# ## Hurricane Tracking Workflow
# This notebook selects trackpoints from a features class of trackpoints for a selected storm (season & name), creates a track line, and extracts US counties that intersect that trackline. 
# 
# Fall 202X  
# John.Fay@duke.edu

# %%
#Import package
import arcpy
from pathlib import Path

#Set paths
raw_folder_path = Path.cwd().parent / 'data' / 'raw'
processed_folder_path = Path.cwd().parent / 'data' / 'processed'

#Arcpy environment settings
arcpy.env.workspace = str(raw_folder_path)
arcpy.env.overwriteOutput = True

# %%
#Set storm variable
storm_season = 2000
storm_name = "HELENE"
affected_counties = processed_folder_path / 'affected_counties.shp'

#Set model layers
ibtracs_NA_points = str(raw_folder_path /'IBTrACS_NA.shp')
usa_counties = 'https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/USA_Counties_Generalized_Boundaries/FeatureServer/0'
storm_track_points =  "memory\\track_points"
storm_track_line = "memory\\Tracklines"

#%%
#create dictionary of storm names in seasons
#initialize dictionary
storm_dict = {}


#initialize storm name list
storm_names = []
#iterate through years
for storm_season in range(2000,2004):
    #create list of storms
    cursor = arcpy.da.SearchCursor(
        in_table = ibtracs_NA_points, 
        where_clause = f'SEASON = {storm_season}',
        field_names = ['NAME']
    )

    #with arcpy.da.SearchCursor(
    # in_table = ibtracs_NA_points, 
    # where_clause = f'SEASON = {storm_season}',
    # field_names = ['NAME']
    #) as cursor: 
        ###code chunk and then cursor auto-deletes

    for row in cursor:
        storm_name = row[0]
        #append to list 
        if not storm_name in storm_names and storm_name != 'UNNAMED':
            storm_names.append(storm_name)

    storm_dict[storm_season] = storm_names

    #delete cursor
    del cursor

# %% [markdown]
# #### Select point features corresponding to a specific storm (season & name)

# %%

#iterate through keys in the dictionary
for storm_season in storm_dict.keys:
    #get list of storms
    storm_names = storm_dict[storm_season]

    storm_count = 0

#iterate through storms
    for storm_name in storm_names:
#Select points for a given storm
        arcpy.analysis.Select(
            in_features=ibtracs_NA_points, 
            out_feature_class=storm_track_points, 
            where_clause=f"SEASON = {storm_season} And NAME = '{storm_name}'"
        )

        #Connect point to a track line
        arcpy.management.PointsToLine(
            Input_Features=storm_track_points,
            Output_Feature_Class=storm_track_line,
            Sort_Field='ISO_TIME'
        )

        select_output = arcpy.management.SelectLayerByLocation(
            in_layer=usa_counties, 
            overlap_type="INTERSECT", 
            select_features=storm_track_line, 
            )
        select_result = select_output.getOutput(0)

        county_count = int(arcpy.GetCount_management(select_result).getOutput(0))

        storm_count += county_count
        print(storm_name, storm_season, county_count, storm_count)


# %% [markdown]
# #### Count the Counties

#%%
#count the counties




# %%

