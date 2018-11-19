#!/usr/bin/env python
# Copyright 2018 Gene Kong
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This file is use for collect compile information

import sys

# 0 -> scripts name
# 1 .. -> compile options

"""
files_db.files :
    {
        "path": "/mnt/k/fastembedded/FASTEMBEDDED_RTOS_SDK/components/feHAL/ST/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_nor.c",
        "opath" : "",
        "component" : "",
        "macros" : ["xx", "yy=1"],
        "include" : ["include=xx.h"],
        "incdir" : ["/abc", "ecd/a/"],
        "options" : ["-Og", "-Wall"],
    }
files_db.linker :
    {
        "opath" : "",
        "options" : [],
    }
"""
OPTS_MACRO = "-D"
OPTS_INCLUDE = "-include"
OPTS_INCDIR = "-I"
OPTS_OPATH = "-o"

options_with_arg = [OPTS_MACRO, OPTS_INCLUDE, OPTS_INCDIR, OPTS_OPATH, "-T", "-L", "-u", "-Xlinker"]

def parse_compile_options(options, path, name) :
    files_obj = {
        "path": path,
        "component": name,
        "opath" : "",
        "macros": [],
        "include": [],
        "incdir" : [],
        "options" : []
    }
    i = 0
    while i < len(options):
        # process macros
        if options[i].startswith(OPTS_MACRO) :
            if len(options[i]) == len(OPTS_MACRO):
                files_obj["macros"].append(options[i + 1])
            else:
                files_obj["macros"].append(options[i][len(OPTS_MACRO):])
        elif options[i].startswith(OPTS_INCLUDE) :
            if len(options[i]) == len(OPTS_INCLUDE):
                files_obj["include"].append(options[i + 1])
            else:
                files_obj["include"].append(options[i][len(OPTS_INCLUDE):])
        elif options[i].startswith(OPTS_INCDIR) :
            if len(options[i]) == len(OPTS_INCDIR):
                files_obj["incdir"].append(options[i + 1])
            else:
                files_obj["incdir"].append(options[i][len(OPTS_INCDIR):])
        elif options[i].startswith(OPTS_OPATH) :
            if len(options[i]) == len(OPTS_OPATH):
                files_obj["opath"] = options[i + 1]
            else:
                files_obj["opath"] = options[i][len(OPTS_OPATH):]
        else:
            if options[i] in options_with_arg:
                files_obj["options"].append(options[i])
                files_obj["options"].append(options[i + 1])
            else:
                files_obj["options"].append(options[i])

        if options[i] in options_with_arg:
            i += 2
        else:
            i += 1
    return files_obj

def parse_linker_options(options) :
    linker_obj = {"opath" : "", "options":[]}
    i = 0
    while i < len(options):
        # process
        if not options[i].endswith(".o") :            
            if options[i].startswith(OPTS_OPATH) :
                if len(options[i]) == len(OPTS_OPATH):
                    linker_obj["opath"] = options[i + 1]
                    i += 1
                else:
                    linker_obj["opath"] = options[i][len(OPTS_OPATH):]
            else:
                linker_obj["options"].append(options[i])
        i += 1
    return linker_obj

with open(sys.argv[1], "r") as f:
    for line in f:
        items = line.split()
        if items[-1].endswith(".map") :    
            linker_obj = parse_linker_options(items[:-1])
        else:
            files_obj = parse_compile_options(items[1:-1], items[-1], items[0])