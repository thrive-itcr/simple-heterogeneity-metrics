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

def metricsForCSV(path, feat_ind, log_flag_bool, maxRange, nSpecies, simMat_bool, metric, all_markers_str, all_metrics_str):
    # Default parameters for the first prototoype:
    # CSV column that contains X data.  Y data is assumed to come npath_ext.
    xy_ind = 1
    # CSV column to use as the heterogeneity feature.
    #feat_ind = 3
    # Whether to perform a log transform.
    #log_flag='1'
    if log_flag_bool == True:
        log_flag='1'
    else:
        log_flag='0'
    # Distance from each cell to examine for diversity.
    #maxRange = 200
    # Number of different species / clusters / categories of cells.
    #nSpecies = 4
    # Similarity matrix:  How similar the species are to each other.
    #simMat = 'default'
    if simMat_bool == True:
        simMat = 'identity'
    else:
        simMat = 'default'
    # Which diversity metric. Allowed values are: QE, Shannon, Simpson
    #metric = 'QE'
    all_markers = string2bool(all_markers_str)
    #print('all_markers:')
    #print(all_markers)
    #print(type(all_markers))

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
                #print('inpath: ' + inpath)
                #print('outpath: ' + outpath)
                #print('xy_ind: ' + str(xy_ind))
                #print('feat_ind: ' + str(feat_ind))
                #print('log_flag: ' + log_flag)
                xy, feat = structureData(inpath, xy_ind, i, log_flag)
                #print('xy:')
                #print(xy)
                #print('feat:')
                #print(feat)
                #print('maxRange: ' + str(maxRange))
                #print('nSpecies: ' + str(nSpecies))
                #print('simMat: ' + simMat)
                #print('metric: ' + metric)
                try:
                    heat, colors = diversityHeatmap(xy, feat, maxRange, nSpecies, simMat, metric)
                    #print('main.py, heat:')
                    #print(heat)
                    #print(type(heat))
                    #print(heat.shape)
                    #print('colors:')
                    #print(colors)
                    #print(type(colors))
                    #print(colors.shape)
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
        #print('path: ' + path)
        #print('xy_ind: ' + str(xy_ind))
        #print('feat_ind: ' + str(feat_ind))
        #print('log_flag: ' + log_flag)
        xy, feat = structureData(path, xy_ind, feat_ind, log_flag)
        #print('xy:')
        #print(xy)
        #print('feat:')
        #print(feat)
        #print('maxRange: ' + str(maxRange))
        #print('nSpecies: ' + str(nSpecies))
        #print('simMat: ' + simMat)
        #print('metric: ' + metric)
        heat, colors = diversityHeatmap(xy, feat, maxRange, nSpecies, simMat, metric)
        prefix = headers[feat_ind] + '-' + metric
        diversity2csv(prefix, inpath, outpath_final, heat, colors)




if __name__ == '__main__':
    if len(sys.argv) < 9:
        print("Not enough arguments.")
        sys.exit()
    # The only argument initially is the path to the input file.
    print sys.argv[1]
    metricsForCSV(sys.argv[1], int(sys.argv[2]), bool(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), bool(sys.argv[6]), sys.argv[7], sys.argv[8], sys.argv[9])

