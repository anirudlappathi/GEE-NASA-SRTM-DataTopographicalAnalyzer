from ast import And
import enum
from re import T
import ee
import numpy

def createPointMap(xMin, xMax, yMin, yMax, image, subdiv):
    
    #ee.Authenticate()
    ee.Initialize()
    
    # CONSTRUCTOR
    XMIN = xMin
    XMAX = xMax
    YMIN = yMin
    YMAX = yMax

    XDIF = XMAX-XMIN
    YDIF = YMAX-YMIN
    
    def createNodeMap(subdiv):
        nodeMap = numpy.zeros(((subdiv, subdiv, 2)), dtype=float)
        for i in range(subdiv):
            for j in range(subdiv):
                nodeMap[i][j][0] = XMIN + (i * (XDIF / (subdiv-1))) 
                nodeMap[i][j][1] = YMIN + (j * (YDIF / (subdiv-1))) 
        return nodeMap

    #def createReadableElevationMap(subdiv, feat):
    #    elevationMap = numpy.zeros(((subdiv, subdiv, 1)), dtype=float)
    

    elevationMap = ee.Image(image)
    nodeMap = createNodeMap(subdiv)

    feats = []

    def colored(r, g, b, text):
        return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

    # make points from nodes
    nullEven = 1
    for row in nodeMap:
        for column in row:
            for val in column:
                if(nullEven % 2 == 1):
                    points = [ee.Geometry.Point(column[0], column[1]) for coord in column]
                    feats += [ee.Feature(p, {'name': 'node{}'.format(i)}) for i, p in enumerate(points)]
                    fc = ee.FeatureCollection(feats)
                    reducer = ee.Reducer.first()
                    data = elevationMap.reduceRegions(fc, reducer.setOutputs(['elevation']), 30)
                nullEven += 1
    viewableEMap = ''
    #iterCounter = 0
    i = 1
    j = 1
    for feat in data.getInfo()['features']:
        if i % 2 == 0:
            try:
                elevation = feat['properties']['elevation']
                print(colored(round((elevation - 500)/1200*255), 50, 50, feat['properties']['elevation']), end='')
                print(' '*(4-(len(str(elevation)))), end='')
            except:
                print('N/A', end='   ')
            if j%subdiv == 0:
                print('\n')
            j += 1
        i += 1

    
    print('\nfeat time: {}'.format(i))
    i += 1
    print(viewableEMap)
                #if iterCounter%subdiv == 0:
                #    viewableEMap += '\n'
                #iterCounter += 1 
                        #viewableEMap[i][j] = feat['properties']
            #print(viewableEMap)
            #except:
                #print('{}: Invalid GeoJSON Geometry'.format(points))
                #feats = [ee.Feature(p) for p in enumerate(points)]

            # make a featurecollection from points
    #fc = ee.FeatureCollection(feats)

            # extract points from elevationMap
            #reducer = ee.Reducer.first()
            #data = elevationMap.reduceRegions(fc, reducer.setOutputs(['elevation']), 30)

            # see data
            #for feat in data.getInfo()['features']:
            #    print(feat['properties'])

    # export as CSV
    #task = ee.batch.Export.table.toDrive(data, 'pointsDataExtract', 'sunsetData.csv')
    #task.start()

createPointMap(9, 10, 9, 10, "USGS/SRTMGL1_003", 50)

#createPointMap(0, 10, 0, 10, "USGS/3DEP/10m", 3)

#var dataset = ee.Image('USGS/3DEP/10m')
#var elevation = dataset.select('elevation');
#var slope = ee.Terrain.slope(elevation);
#Map.setCenter(-112.8598, 36.2841, 10);
#Map.addLayer(elevation, {min: 0, max: 3000,   palette: [
#    '3ae237', 'b5e22e', 'd6e21f', 'fff705', 'ffd611', 'ffb613', 'ff8b13',
#    'ff6e08', 'ff500d', 'ff0000', 'de0101', 'c21301', '0602ff', '235cb1',
#    '307ef3', '269db1', '30c8e2', '32d3ef', '3be285', '3ff38f', '86e26f'
#  ],
#}, 'elevation');
#Map.addLayer(slope, {min: 0, max: 60}, 'slope');