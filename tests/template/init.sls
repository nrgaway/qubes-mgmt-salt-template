# -*- coding: utf-8 -*-
# vim: set syntax=yaml ts=2 sw=2 sts=2 et :

##
# template tests
# ==============
# 
# Execute:
#   qubesctl state.sls template test
##

template-test-always-passes:
  test.succeed_without_changes:
    - name: foo
