# ==============================================================================
# Puppet Module: supplier_portal
# Declarative resource management for prerequisites, users, directories,
# Nginx web server, and application daemon.
# Author: AADITYA ASWALE (23102B0044)
# ==============================================================================

class supplier_portal (
  String $app_dir    = '/opt/supplier-quality-portal',
  String $app_user   = 'deployer',
  String $app_group  = 'deployer',
  Integer $port      = 80,
) {

  # 1. Prerequisite Packages
  $prereq_packages = ['nginx', 'curl', 'git', 'python3', 'python3-pip', 'docker.io']

  package { $prereq_packages:
    ensure => installed,
  }

  # 2. System Deployer User
  user { $app_user:
    ensure     => present,
    managehome => true,
    shell      => '/bin/bash',
    groups     => ['docker', 'sudo'],
    require    => Package['docker.io'],
  }

  # 3. Application Directory Structure
  file { [$app_dir, "${app_dir}/data", "${app_dir}/data/static", "${app_dir}/data/media"]:
    ensure  => directory,
    owner   => $app_user,
    group   => $app_group,
    mode    => '0755',
    require => User[$app_user],
  }

  # 4. Nginx Reverse Proxy Configuration
  file { '/etc/nginx/sites-available/supplier_portal.conf':
    ensure  => file,
    owner   => 'root',
    group   => 'root',
    mode    => '0644',
    content => "# Puppet-managed Nginx configuration\nserver {\n    listen 80;\n    server_name localhost 127.0.0.1;\n    location /health/ {\n        proxy_pass http://127.0.0.1:8000/health/;\n    }\n    location / {\n        proxy_pass http://127.0.0.1:8000;\n    }\n}\n",
    require => Package['nginx'],
    notify  => Service['nginx'],
  }

  file { '/etc/nginx/sites-enabled/supplier_portal.conf':
    ensure  => link,
    target  => '/etc/nginx/sites-available/supplier_portal.conf',
    require => File['/etc/nginx/sites-available/supplier_portal.conf'],
    notify  => Service['nginx'],
  }

  # 5. Nginx Service Management
  service { 'nginx':
    ensure     => running,
    enable     => true,
    hasrestart => true,
    hasstatus  => true,
    require    => Package['nginx'],
  }

  # 6. Docker Service Management
  service { 'docker':
    ensure     => running,
    enable     => true,
    hasrestart => true,
    require    => Package['docker.io'],
  }

  # 7. Health Probe Verification
  exec { 'verify_portal_health':
    command     => '/usr/bin/curl -f http://localhost:80/health/',
    refreshonly => true,
    subscribe   => Service['nginx'],
    tries       => 3,
    try_sleep   => 5,
  }
}
