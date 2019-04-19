import sys, os, csv
from structureData import *
from diversityHeatmap import *
from diversity2csv import *

# Main script written by BDS.

def string2bool(s):
    if (s.lower() == "true" or s.lower() == "t"):
        return True
    else:
        return False

def calculate_one_metric(path,inpath,outpath_final,headers,xy_ind,feat_ind,log_flag,maxRange,nSpecies,simMat,metric):
    # Just calculates metrics on a single marker.
    xy, feat = structureData(path, xy_ind, feat_ind, log_flag)
    heat, colors = diversityHeatmap(xy, feat, maxRange, nSpecies, simMat, metric)
    prefix = headers[feat_ind] + '-' + metric
    diversity2csv(prefix, inpath, outpath_final, heat, colors)

def calculate_one_metric_on_markers(path,all_markers,xy_ind,feat_ind,log_flag,maxRange,nSpecies,simMat,metric):
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
    if all_markers == True:
        # Calculate metrics on all the markers.
        # Iterate through the headers.
        i = 0
        found_one = False
        # test case for processing all markers
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
                    prefix = h + '-' + metric
                    diversity2csv(prefix, inpath, outpath, heat, colors)
                    #print('SUCCESS getting diversity metrics on ' + h)
                found_one = True
            i=i+1 # end of for loop
        # Copy file at outpath to outpath_final.
        os.system('cp ' + outpath + ' ' + outpath_final)
        #print('Done processing all columns')
    else:
        # Just calculates metrics on a single marker.
        calculate_one_metric(path,inpath, outpath_final, headers, xy_ind,feat_ind,log_flag,maxRange,nSpecies,simMat,metric)


# Parameters:
#   path - location of marker quantitation input file
#   feat_ind - csv column index for the location of the marker to be analyzed (if only one)
#   log_flag_bool - whether to perform a log transform
#   maxRange - distance from each cell to examine for diversity
#   nSpecies - number of different species / clusters / categories of cells
#   simMat_bool - how similar the species are to each other, true == identity matrix, false == default matrix
#   metric - which diversity metric, allowed values are: QE, Shannon, Simpson
#   all_markers_str
#   all_metrics_str
def metricsForCSV(path, feat_ind, log_flag_bool, maxRange, nSpecies, simMat_bool, metric, all_markers_str, all_metrics_str):
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
    all_markers = string2bool(all_markers_str)
    all_metrics = string2bool((all_metrics_str))
    calculate_one_metric_on_markers(path,all_markers,xy_ind,feat_ind,log_flag,maxRange,nSpecies,simMat,metric)
    '''
    # Not yet implemented.  Only QE is actually implemented.
    if all_metrics == False:
        calculate_one_metric_on_markers(path,all_markers,xy_ind,feat_ind,log_flag,maxRange,nSpecies,simMat,metric)
    else:
        # Iterate through QE, Shannon, Simpson
        print('Calculating all metrics: QE, Shannon, Simpson')
        metric = 'QE'
        calculate_one_metric_on_markers(path,all_markers,xy_ind,feat_ind,log_flag,maxRange,nSpecies,simMat,metric)
    '''

if __name__ == '__main__':
    if len(sys.argv) < 9:
        print("Not enough arguments.")
        sys.exit()
    # The only argument initially is the path to the input file.
    print sys.argv[1]
    metricsForCSV(sys.argv[1], int(sys.argv[2]), bool(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), bool(sys.argv[6]), sys.argv[7], sys.argv[8], sys.argv[9])

