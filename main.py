import sys, os, csv
import numpy as np
import mysql.connector
from structureData import *
from diversityHeatmap import *
from diversity2csv import *

# Main script written by BDS.

'''
def string2bool(s):
    if (s.lower() == "true" or s.lower() == "t"):
        return True
    else:
        return False
'''

def calculate_one_metric_on_markers(path,xy_ind,log_flag,maxRange,nSpecies,simMat,metric,slide,region,branch):
    #print('entering calculate_one_metric_on_markers() with slide %s, region %s, branch %s' % (slide,region,branch))
    # Assemble the output file path.
    inpath = path
    path_nm, path_ext  = os.path.splitext(os.path.basename(path))
    output_nm = path_nm + '_diversity' + path_ext
    outpath_final = os.path.join(os.path.dirname(path), output_nm)
    # Get all the headers in the quantitation file.
    f = open(path, 'r')
    headers = next(csv.reader(f))
    f.close()
    #print('headers are:')
    #print(headers)
    # Calculate metrics on all the markers.
    # Iterate through the headers.
    i = 0
    found_one = False
    # Create database connection for results.
    cnx = mysql.connector.connect(user='root',password='thrivemysql',host='thrive-mysql',database='thrivedb')
    # Insert several entries into the metrics table.
    cursor = cnx.cursor()
    add_metric = "INSERT INTO heterogeneity_metric (slide_name, region_name, branch_name, metric_name, metric_value) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE metric_value=%s"
    # Processing all markers
    for h in headers:
        #print('header ' + str(i) + ': ' + h)
        # Process all the headers that include the word 'Mean'
        if h.find('Mean') > -1:
            # Assemble the intermediate output file path.
            if found_one == False:
                inpath = path
            else:
                inpath = outpath
            output_nm = path_nm + '_' + str(i) + path_ext
            outpath = os.path.join(os.path.dirname(path), output_nm)
            xy, feat = structureData(inpath, xy_ind, i, log_flag)
            try:
                heat, colors = diversityHeatmap(xy, feat, maxRange, nSpecies, simMat, metric)
            except:
                print('ERROR getting diversity metrics on ' + h)
                outpath = inpath # Revert outpath to its previous value because we did not create a new output file
            else:
                #print('heat:')
                #print(heat)
                #print('np.mean(heat):')
                #print(np.mean(heat))
                prefix = h + '-' + metric
                print('calculate_one_metric_on_markers(), h: %s, metric: %s, prefix: %s, mean: %f, median: %f, std: %f' % (h, metric, prefix, np.mean(heat), np.median(heat), np.std(heat)))
                diversity2csv(prefix, inpath, outpath, heat, colors)
                # Write metrics to database.
                if (np.isfinite(np.mean(heat))):
                    mean_data = (slide, region, branch, prefix+'-mean', str(np.mean(heat)), str(np.mean(heat)))
                    cursor.execute(add_metric, mean_data)
                if (np.isfinite(np.median(heat))):
                    median_data = (slide, region, branch, prefix+'-median', str(np.median(heat)), str(np.median(heat)))
                    cursor.execute(add_metric, median_data)
                if (np.isfinite(np.std(heat))):
                    std_data = (slide, region, branch, prefix+'-std', str(np.std(heat)), str(np.std(heat)))
                    cursor.execute(add_metric, std_data)
                cnx.commit()
                #print('SUCCESS getting diversity metrics on ' + h)
            found_one = True
        i=i+1 # end of for loop
    # Copy file at outpath to outpath_final.
    os.system('cp ' + outpath + ' ' + outpath_final)
    cnx.close()
    #print('Done processing all columns')


# Parameters:
#   path - location of marker quantitation input file
#   log_flag_bool - whether to perform a log transform
#   maxRange - distance from each cell to examine for diversity
#   nSpecies - number of different species / clusters / categories of cells
#   simMat_bool - how similar the species are to each other, true == identity matrix, false == default matrix
#   metric - which diversity metric, allowed values are: QE, Shannon, Simpson
def metricsForCSV(path, log_flag_bool, maxRange, nSpecies, simMat_bool, metric, slide, region, branch):
    # xy_ind is the csv column that contains X data.  Y data is assumed to come next.
    xy_ind = 1
    if log_flag_bool == True:
        log_flag='1'
    else:
        log_flag='0'
    if simMat_bool == True:
        simMat = 'identity'
    else:
        simMat = 'default'
    calculate_one_metric_on_markers(path,xy_ind,log_flag,maxRange,nSpecies,simMat,metric,slide,region,branch)

    '''
    '''

if __name__ == '__main__':
    if len(sys.argv) < 9:
        print("Not enough arguments.")
        sys.exit()
    # The only argument initially is the path to the input file.
    print sys.argv[1]
    metricsForCSV(sys.argv[1], bool(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), bool(sys.argv[5]), sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9])

