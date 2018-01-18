#!/bin/bash
# Copyright (c) General Electric Company, 2017.  All rights reserved.

echo ""
echo "Removing algorithm image."
docker rmi thriveitcr/simple-heterogeneity-metrics

echo ""
echo "Building algorithm image."
docker build -t thriveitcr/simple-heterogeneity-metrics --build-arg http_proxy=$http_proxy --build-arg https_proxy=$https_proxy --build-arg no_proxy=$no_proxy .
echo ""
docker images
