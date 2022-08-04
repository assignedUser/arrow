# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
FROM  public.ecr.aws/lambda/python:3.9

ARG ARROW_REF=master
ARG ARROW_ORG=apache

RUN yum install -y git

RUN git clone https://github.com/$ARROW_ORG/arrow && \
    cd arrow  && \
    git checkout $ARROW_REF && \
    python3 -m pip install -e dev/archery[bot]

COPY app.py requirements.txt ${LAMBDA_TASK_ROOT}/

RUN pip install -r requirements.txt --target ${LAMBDA_TASK_ROOT}
CMD [ "app.handler"]
