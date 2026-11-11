#! /usr/bin/python3
#
# Copyright (c) 2017 Intel Corporation
#
# SPDX-License-Identifier: Apache-2.0
#

#
# Invoke with
#
# VERSION=$(git describe) python ./setup.py bdist_rpm
#
#
import os
import sys

import distutils
import distutils.command.bdist_rpm
import distutils.command.install_data
import distutils.command.sdist
import distutils.command.build_py
import distutils.core
import distutils.sysconfig

import setupl

import setuptools.command.bdist_rpm
# setuptools names sdists with the PEP 625 normalized name (tcf_client-*)
# but the bdist_rpm spec still refers to the unnormalized one
class _bdist_rpm(setuptools.command.bdist_rpm.bdist_rpm):
    def _make_spec_file(self):
        norm = self.distribution.get_name().replace('-', '_')
        return [ l.replace('%{name}-%{unmangled_version}',
                           norm + '-%{unmangled_version}')
                 for l in super()._make_spec_file() ]

distutils.core.setup(
    name = 'ttbd-pos',
    description = "TCF TTBD server Provisioning OS extensions",
    long_description = """\
These are the extensions to the TTBD server that enable to do fast
imaging on PC-class targets via DHCP / TFTP.
""",
    version = setupl.version,
    url = "http://intel.github.com/tcf",
    author = "Inaky Perez-Gonzalez",
    author_email = "inaky.perez-gonzalez@intel.com",
    cmdclass = dict(
        bdist_rpm = _bdist_rpm,
        install_data = setupl._install_data,
    ),
    packages = [ ],
    scripts = [ ],
    data_files = [
        ( '@sysconfigdir@/systemd/system/ttbd@.service.d/', [
            'pos.conf'
        ]),
        ( '@sysconfigdir@/httpd/conf.d/', [
            'ttbd.conf',
        ]),
        ( '@sysconfigdir@/exports.d/', [
            'ttbd-pos.exports',
        ]),
        ( '@prefix@/share/tcf/', [
            'kickstart-install.sh',
            'qemu-nbd-dynamic.sh',
            'tcf-image-setup.sh',
            'tcf-pos-live-setup.sh',
        ]),
        ( '@prefix@/share/tcf/content', [
            'evemu.bin.armv7l.tar.gz',
            'evemu.bin.x86_64.tar.gz',
        ]),
        ( '@prefix@/share/tcf/ttbd/pos', [
            'requirements.txt',
        ]),
    ],
)
