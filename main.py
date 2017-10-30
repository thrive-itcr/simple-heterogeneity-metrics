import sys
from structureData import *
from diversityHeatmap import *
from diversity2csv import *

# Main script written by BDS.

def metricsForCSV(path, feat_ind):
    # Default parameters for the first prototoype:
    # CSV column that contains X data.  Y data is assumed to come next.
    xy_ind = 1
    # CSV column to use as the heterogeneity feature.
    #feat_ind = 3
    # Whether to perform a log transform.
    log_flag='1'
    # Distance from each cell to examine for diversity.
    maxRange = 200
    # Number of different species / clusters / categories of cells.
    nSpecies = 4
    # Similarity matrix:  How similar the species are to each other.
    simMat = 'default'
    # Which diversity metric. Allowed values are: QE, Shannon, Simpson
    metric = 'QE'

    xy, feat = structureData(path, xy_ind, feat_ind, log_flag)
    # BDS - modified the call below not to return colors.
    heat = diversityHeatmap(xy, feat, maxRange, nSpecies, simMat, metric)
    diversity2csv(path, heat)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Need to supply a path name and feature index.")
        sys.exit()
    # The only argument initially is the path to the input file.
    print sys.argv[1]
    metricsForCSV(sys.argv[1], int(sys.argv[2]))

