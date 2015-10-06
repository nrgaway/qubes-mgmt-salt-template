# -*- coding: utf-8 -*-
# vim: set syntax=yaml ts=2 sw=2 sts=2 et :

##
# template
# ========
# 
# State description
#
# Execute:
#   qubesctl state.sls template
##

template-always-passes:
  test.succeed_without_changes:
    - name: foo
