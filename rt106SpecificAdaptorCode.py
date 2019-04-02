# Copyright (c) General Electric Company, 2017.  All rights reserved.

# Rt 106

# Simple Heterogeneity Metrics

import os, glob, uuid, time, logging, subprocess

# function: run_algorithm() -- Python function for marshalling your data and running your algorithm.
# parameters:
#   datastore: object tobe used when interacting with the Object Store
#   context:  A JSON structure that should contain all the inputs and parameters your algorithm needs.
def run_algorithm(datastore,context):

    logging.info('run_algorithm: %r' % context)

    # cleanup the input and output directories
    for f in glob.glob('/rt106/input/*') + glob.glob('/rt106/output/*'):
        os.remove(f)

    # 1.    Code for marshalling inputs.
    cell_quant_path = datastore.get_pathology_result_image_path(context['slide'], context['region'], context['branch'],  'Quant')
    if (type(cell_quant_path) == "int" and cell_quant_path > 200):
        status = "ERROR_QUANT_FILE_NOT_FOUND"
        return { 'result' : {}, 'status' : cell_quant_path }

    quan_csv = 'quan_%s.csv' % context['region']
    het_csv = 'quan_%s_diversity.csv' % context['region']
    instance_status = datastore.get_instance(cell_quant_path, '/rt106/input', quan_csv, 'csv')
    if (instance_status != 200):
        status = "ERROR_QUANT_FILE_NOT_FOUND"
        return { 'result' : {}, 'status' : status }

    output_path = datastore.get_pathology_result_path(context['slide'], context['region'], context['branch'], 'Heterogeneity')
    output_file = '/rt106/input/%s' % het_csv

    # 2.    Code for calling algorithm.
    all_markers_var = context['all_markers']
    all_metrics_var = context['all_metrics']
    biomarker_var = context['biomarker']
    log_flag_var = context['log_flag']
    maxRange_var = context['maxRange']
    numberSpecies_var = context['numberSpecies']
    identity_matrix_var = context['identity_matrix']
    metric_var = context['metric']
    if metric_var != "QE" and metric_var != 'Shannon' and metric_var != 'Simpson':
        status = "ERROR_BAD_METRIC_TYPE"
        return { 'result' : {}, 'status' : status}
    try:
        run_algorithm = '/usr/bin/python main.py /rt106/input/%s %s %s %s %s %s %s %s %s' % (quan_csv, biomarker_var, log_flag_var, maxRange_var, numberSpecies_var, identity_matrix_var, metric_var, all_markers_var, all_metrics_var)
        logging.info('run Algorithm: %r' % run_algorithm)
        subprocess.check_call(run_algorithm,shell=True)
    except subprocess.CalledProcessError, e:
        logging.error('%d - %s' % (e.returncode, e.cmd))
        status = "EXECUTION_FINISHED_ERROR"
        result_context = {}
        return { 'result' : result_context, 'status' : status }

    # 3.    Set status.
    status = "EXECUTION_FINISHED_SUCCESS"

    # 4.    Store results in datastore.
    # Note that algorithm puts its output back in the /rt106/input directory.
    response_upload = datastore.post_instance(output_path, '/rt106/input', het_csv, 'csv', context['force'])

    if response_upload == 403:
        status = "EXECUTION_ERROR"

    # 5.    Create JSON structure containing results.
    nuclear_image_path = datastore.get_pathology_primary_path(context['slide'], context['region'], 'DAPI')
    result_context = {
        "nuclearImage" : nuclear_image_path,
        "cellMetrics" : output_path
    }

    return { 'result' : result_context, 'status' : status }
