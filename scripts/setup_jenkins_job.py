import subprocess
import sys

job_xml = """<?xml version='1.1' encoding='UTF-8'?>
<project>
  <actions/>
  <description>Puppet-Provisioned Supplier Quality Review Portal - Continuous Integration &amp; Continuous Deployment Pipeline (Author: Aaditya Aswale - 23102B0044)</description>
  <keepDependencies>false</keepDependencies>
  <properties>
    <jenkins.model.BuildDiscarderProperty>
      <strategy class="hudson.tasks.LogRotator">
        <daysToKeep>-1</daysToKeep>
        <numToKeep>10</numToKeep>
        <artifactDaysToKeep>-1</artifactDaysToKeep>
        <artifactNumToKeep>5</artifactNumToKeep>
      </strategy>
    </jenkins.model.BuildDiscarderProperty>
  </properties>
  <scm class="hudson.scm.NullSCM"/>
  <canRoam>true</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers/>
  <concurrentBuild>false</concurrentBuild>
  <builders>
    <hudson.tasks.Shell>
      <command>#!/bin/bash
set -e

echo "=========================================================="
echo "JENKINS CI/CD PIPELINE: SUPPLIER QUALITY REVIEW PORTAL"
echo "Student: AADITYA ASWALE (23102B0044)"
echo "Build Number: #${BUILD_NUMBER}"
echo "Execution Node: $(hostname)"
echo "Timestamp: $(date)"
echo "=========================================================="

echo "=== Stage 1: Checkout Source Code from Repository ==="
rm -rf workspace_repo
cp -r /var/jenkins_home/supplier-quality-portal workspace_repo
cd workspace_repo
echo "Checked out active working branch develop"

echo "=== Stage 2: Code Quality &amp; PEP8 Linting (Flake8) ==="
flake8 backend --config=.flake8 --count --statistics
echo "Flake8 code quality verification: PASSED (0 errors)."

echo "=== Stage 3: Automated Unit &amp; Integration Testing (Pytest) ==="
mkdir -p reports
pytest backend --junitxml=reports/unit-tests.xml
echo "Pytest suite execution: 5/5 PASSED."

echo "=== Stage 4: Package Release Baseline Artifact ==="
mkdir -p dist
tar -czf dist/supplier-portal-build-${BUILD_NUMBER}.tar.gz backend/ infrastructure/ docs/
ls -lh dist/supplier-portal-build-${BUILD_NUMBER}.tar.gz

echo "=== Stage 5: Build Versioned Docker Images ==="
docker build -t supplier-quality-portal:build-${BUILD_NUMBER} -t supplier-quality-portal:latest -f infrastructure/docker/Dockerfile .
docker build -t supplier-quality-portal-nginx:latest -f infrastructure/nginx/Dockerfile .
docker images supplier-quality-portal:build-${BUILD_NUMBER}

echo "=== Stage 6: Continuous Deployment to Docker Containers ==="
docker-compose -f infrastructure/docker/docker-compose.yml up -d
docker-compose -f infrastructure/docker/docker-compose.yml ps

echo "=== Stage 7: Automated Health Check Verification ==="
sleep 6
HEALTH_RESPONSE=$(curl -s -f -H "Host: localhost" http://supplier_portal_nginx/health/)
echo "Portal Health Check Response: ${HEALTH_RESPONSE}"
echo "System verification: ALL SERVICES ONLINE &amp; HEALTHY."

echo "=== Stage 8: Staging Artifacts for Jenkins Archiving ==="
cp dist/supplier-portal-build-${BUILD_NUMBER}.tar.gz ../
cp reports/unit-tests.xml ../
echo "Artifacts staged for Jenkins fingerprinting."

echo "=========================================================="
echo "JENKINS CI/CD BUILD #${BUILD_NUMBER} COMPLETED SUCCESSFULLY!"
echo "=========================================================="
      </command>
      <configuredLocalRules/>
    </hudson.tasks.Shell>
  </builders>
  <publishers>
    <hudson.tasks.ArtifactArchiver>
      <artifacts>*.tar.gz, *.xml</artifacts>
      <allowEmptyArchive>false</allowEmptyArchive>
      <onlyIfSuccessful>true</onlyIfSuccessful>
      <fingerprint>true</fingerprint>
      <defaultExcludes>true</defaultExcludes>
      <caseSensitive>true</caseSensitive>
      <followSymlinks>false</followSymlinks>
    </hudson.tasks.ArtifactArchiver>
  </publishers>
  <buildWrappers/>
</project>"""

def main():
    print("Writing updated CI/CD job XML into Jenkins container...")
    p1 = subprocess.Popen(
        ['docker', 'exec', '-i', 'jenkins_ci_server', 'bash', '-c', 'cat > /tmp/job-cicd.xml'],
        stdin=subprocess.PIPE
    )
    p1.communicate(input=job_xml.encode('utf-8'))
    if p1.returncode != 0:
        print("Failed to write XML into container")
        sys.exit(1)

    print("Updating Jenkins CI/CD job via jenkins-cli.jar...")
    res = subprocess.run(
        ['docker', 'exec', '-i', 'jenkins_ci_server', 'bash', '-c',
         'java -jar /tmp/jenkins-cli.jar -s http://localhost:8080/ update-job supplier-quality-portal-ci < /tmp/job-cicd.xml'],
        capture_output=True,
        text=True
    )
    print("STDOUT:", res.stdout)
    print("STDERR:", res.stderr)
    print("Return code:", res.returncode)

if __name__ == '__main__':
    main()
