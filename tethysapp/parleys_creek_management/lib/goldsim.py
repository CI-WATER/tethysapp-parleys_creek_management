"""
Created on Oct 9, 2013

@author: sdc50
"""
import requests


def runLittleDellGoldSim(arguments, resultsFile):
    """
    Runs the Parleys Creek Goldsim model via an OWS web service
    """
    inputs = {"sc_number": arguments["sc_number"],
              "init_lit": arguments["init_lit"],
              "capacity_lit": arguments["capacity_lit"],
              "deadpool_lit": arguments["deadpool_lit"],
              "init_mt": arguments["init_mt"],
              "capacity_mt": arguments["capacity_mt"],
              "deadpool_mt": arguments["deadpool_mt"],
              "dc_jan": arguments["dc_jan"],
              "dc_feb": arguments["dc_feb"],
              "dc_mar": arguments["dc_mar"],
              "dc_apr": arguments["dc_apr"],
              "dc_may": arguments["dc_may"],
              "dc_jun": arguments["dc_jun"],
              "dc_jul": arguments["dc_jul"],
              "dc_aug": arguments["dc_aug"],
              "dc_sep": arguments["dc_sep"],
              "dc_oct": arguments["dc_oct"],
              "dc_nov": arguments["dc_nov"],
              "dc_dec": arguments["dc_dec"],
              "lc_jan": arguments["lc_jan"],
              "lc_feb": arguments["lc_feb"],
              "lc_mar": arguments["lc_mar"],
              "lc_apr": arguments["lc_apr"],
              "lc_may": arguments["lc_may"],
              "lc_jun": arguments["lc_jun"],
              "lc_jul": arguments["lc_jul"],
              "lc_aug": arguments["lc_aug"],
              "lc_sep": arguments["lc_sep"],
              "lc_oct": arguments["lc_oct"],
              "lc_nov": arguments["lc_nov"],
              "lc_dec": arguments["lc_dec"],
              "mks_jan": arguments["mks_jan"],
              "mks_feb": arguments["mks_feb"],
              "mks_mar": arguments["mks_mar"],
              "mks_apr": arguments["mks_apr"],
              "mks_may": arguments["mks_may"],
              "mks_jun": arguments["mks_jun"],
              "mks_jul": arguments["mks_jul"],
              "mks_aug": arguments["mks_aug"],
              "mks_sep": arguments["mks_sep"],
              "mks_oct": arguments["mks_oct"],
              "mks_nov": arguments["mks_nov"],
              "mks_dec": arguments["mks_dec"],
              "dem_jan": arguments["dem_jan"],
              "dem_feb": arguments["dem_feb"],
              "dem_mar": arguments["dem_mar"],
              "dem_apr": arguments["dem_apr"],
              "dem_may": arguments["dem_may"],
              "dem_jun": arguments["dem_jun"],
              "dem_jul": arguments["dem_jul"],
              "dem_aug": arguments["dem_aug"],
              "dem_sep": arguments["dem_sep"],
              "dem_oct": arguments["dem_oct"],
              "dem_nov": arguments["dem_nov"],
              "dem_dec": arguments["dem_dec"]}

    ##http: // ci - water.byu.edu:81 / little - dell?sc_number = 1 & init_lit = 5700 & capacity_lit = 20000 & deadpool_lit = 0 & init_mt = 2000 & capacity_mt = 3200 & deadpool_mt = 800 & dc_jan = 1 & dc_feb = 1 & dc_mar = 1 & dc_apr = 1 & dc_may = 1 & dc_jun = 1 & dc_jul = 1 & dc_aug = 1 & dc_sep = 1 & dc_oct = 1 & dc_nov = 1 & dc_dec = 1 & lc_jan = 1 & lc_feb = 1 & lc_mar = 1 & lc_apr = 1 & lc_may = 1 & lc_jun = 1 & lc_jul = 1 & lc_aug = 1 & lc_sep = 1 & lc_oct = 1 & lc_nov = 1 & lc_dec = 1 & mks_jan = 1 & mks_feb = 1 & mks_mar = 1 & mks_apr = 1 & mks_may = 1 & mks_jun = 1 & mks_jul = 1 & mks_aug = 1 & mks_sep = 1 & mks_oct = 1 & mks_nov = 1 & mks_dec = 1 & dem_jan = 1 & dem_feb = 1 & dem_mar = 1 & dem_apr = 1 & dem_may = 1 & dem_jun = 1 & dem_jul = 1 & dem_aug = 1 & dem_sep = 1 & dem_oct = 1 & dem_nov = 1 & dem_dec = 1

    response = requests.get('http://ci-water.byu.edu:81/little-dell',
                            params=inputs,
                            stream=True)

    with open(resultsFile, 'wb') as f:
        f.write(response.content)

    return response.status_code


if __name__ == '__main__':
    arguments = {"sc_number": "1",
                 "init_lit": "5700",
                 "capacity_lit": "20000",
                 "deadpool_lit": "0",
                 "init_mt": "2000",
                 "capacity_mt": "3200",
                 "deadpool_mt": "800",
                 "dc_jan": "1",
                 "dc_feb": "1",
                 "dc_mar": "1",
                 "dc_apr": "1",
                 "dc_may": "1",
                 "dc_jun": "1",
                 "dc_jul": "1",
                 "dc_aug": "1",
                 "dc_sep": "1",
                 "dc_oct": "1",
                 "dc_nov": "1",
                 "dc_dec": "1",
                 "lc_jan": "1",
                 "lc_feb": "1",
                 "lc_mar": "1",
                 "lc_apr": "1",
                 "lc_may": "1",
                 "lc_jun": "1",
                 "lc_jul": "1",
                 "lc_aug": "1",
                 "lc_sep": "1",
                 "lc_oct": "1",
                 "lc_nov": "1",
                 "lc_dec": "1",
                 "mks_jan": "1",
                 "mks_feb": "1",
                 "mks_mar": "1",
                 "mks_apr": "1",
                 "mks_may": "1",
                 "mks_jun": "1",
                 "mks_jul": "1",
                 "mks_aug": "1",
                 "mks_sep": "1",
                 "mks_oct": "1",
                 "mks_nov": "1",
                 "mks_dec": "1",
                 "dem_jan": "1",
                 "dem_feb": "1",
                 "dem_mar": "1",
                 "dem_apr": "1",
                 "dem_may": "1",
                 "dem_jun": "1",
                 "dem_jul": "1",
                 "dem_aug": "1",
                 "dem_sep": "1",
                 "dem_oct": "1",
                 "dem_nov": "1",
                 "dem_dec": "1"}

    resultsFile = 'results.xls'
    runLittleDellGoldSim(arguments, resultsFile)


# print wps.identification.type
#    
#    print wps.identification.title
#    
#    print wps.identification.abstract
#    
#    for operation in wps.operations:
#        print operation.name
#    
#    for process in wps.processes:
#        print process.identifier, process.title
#        
#    from owslib.wps import printInputOutput
#    
#    process = wps.describeprocess('goldsim.littledell')
#    
#    print process.title, process.abstract
#    
#    #for input in process.dataInputs:
#    #        print printInputOutput(input)
