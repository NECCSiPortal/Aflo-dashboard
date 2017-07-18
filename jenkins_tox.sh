#!/bin/bash

##
## This file is for running tox, coverage test
##
## Jenkins tox or coverage test job will use this file on Jenkins slave server.
## The job name is "Aflo-dashboard_xxx_Tox" or "Aflo-dashboard_xxx_Coverage"
##
## Aflo-dashboard is depeding on
##  - NECCSPortal-dashboard
##  - python-Afloclient
## and this is not a plugin of Horizon.
## The way of running tox test is a little bit special.
## So we write the code that way in this file.
##

##
## Variables determined by Jenkins
if [ "${WORKSPACE}" = "" ]; then
  echo "You need to export WORKSPACE env"
  exit 1
fi
if [ "${BUILD_NUMBER}" = "" ]; then
  echo "You need to export BUILD_NUMBER env"
  exit 1
fi
if [ "${GITHUB_BK_DIR}" = "" ]; then
  echo "You need to export GITHUB_BK_DIR env"
  exit 1
fi
if [ "${TARGET_HORIZON_BR}" = "" ]; then
  echo "You need to export TARGET_HORIZON_BR env"
  exit 1
fi
TARGET_HORIZON_BR_NM=${TARGET_HORIZON_BR//\//_}
if [ "${TARGET_NECCSPORTAL_BR}" = "" ]; then
  echo "You need to export TARGET_NECCSPORTAL_BR env"
  exit 1
fi
if [ "${NECCSPORTAL_GIT}" = "" ]; then
  echo "You need to export NECCSPORTAL_GIT env"
  exit 1
fi

##
## RPMs
yum install -y gcc libffi-devel openssl-devel

##
## Git clone Openstack/horizon
cd ${GITHUB_BK_DIR}

if ls ${GITHUB_BK_DIR}/horizon.${TARGET_HORIZON_BR_NM} > /dev/null 2>&1
then
  echo "Already github source is cloned"
else
  git clone -b ${TARGET_HORIZON_BR} --single-branch https://github.com/openstack/horizon.git
  mv horizon horizon.${TARGET_HORIZON_BR_NM}
fi
cd horizon.${TARGET_HORIZON_BR_NM}
git pull
git log -n 1 --format=%H

##
## Create temporary directory
rm -rf ${WORKSPACE}/.horizon
mkdir ${WORKSPACE}/.horizon
cp -prf ${GITHUB_BK_DIR}/horizon.${TARGET_HORIZON_BR_NM} ${WORKSPACE}/.horizon/horizon
##
## Git clone NECCSPortal-dashboard from GitLab
cd ${WORKSPACE}/.horizon
git clone -b ${TARGET_NECCSPORTAL_BR} --single-branch ${NECCSPORTAL_GIT}

##
## Put NECCSPortal-dashboard to horizon
\cp -prf ./NECCSPortal-dashboard/* ./horizon/

##
## Put Aflo-dashboard to horizon
cd ${WORKSPACE}/../
rsync -a ${WORKSPACE}/* ${WORKSPACE}/.horizon/horizon/ --exclude .horizon  --exclude nec_portal/local/nec_portal_settings.py
cat ${WORKSPACE}/nec_portal/local/nec_portal_settings.py >> ${WORKSPACE}/.horizon/horizon/nec_portal/local/nec_portal_settings.py

##
## Edit test-requirements.txt to be able to install python-Afloclient
#cat <<EOF >> ${WORKSPACE}/.horizon/horizon/test-requirements.txt
#-e git+${AFLOCLIENT_GIT}@${TARGET_NECCSPORTAL_BR}#egg=python-Afloclient
#EOF
## Git clone python-Afloclient from GitLab
cd ${WORKSPACE}/.horizon
git clone -b ${TARGET_NECCSPORTAL_BR} --single-branch ${AFLOCLIENT_GIT}

##
## Edit test-requirements.txt to be able to install python-Afloclient
cat <<EOF >> ${WORKSPACE}/.horizon/horizon/test-requirements.txt
-e git+${AFLOCLIENT_GIT}@${TARGET_NECCSPORTAL_BR}#egg=python-Afloclient
EOF

##
## Run tox/coverage
cd ${WORKSPACE}/.horizon/horizon/
./run_tests.sh -V -n $@

echo "bye"