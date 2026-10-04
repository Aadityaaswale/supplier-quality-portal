# ==============================================================================
# Puppet Master Site Manifest
# Project: Puppet-Provisioned Supplier Quality Review Portal
# Student: AADITYA ASWALE (23102B0044)
# ==============================================================================

node default {
  include supplier_portal
}

node /.*\.supplierportal\.local$/ {
  include supplier_portal
}
