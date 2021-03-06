#!/usr/bin/python2

import sys;
from structs import structs;

# command line arguments
arch    = sys.argv[1];
outfile = sys.argv[2];
archs   = sys.argv[3:];

f = open(outfile, "w");
f.write('''
/*
 * sanity checks for generated foreign headers:
 *  - verify struct sizes
 *
 * generated by %s -- DO NOT EDIT
 */
#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <inttypes.h>
#include "../xen.h"
''');

for a in archs:
    f.write('#include "%s.h"\n' % a);

f.write('int main(int argc, char *argv[])\n{\n');

f.write('\tprintf("\\n");');
f.write('printf("%-25s |", "structs");\n');
for a in archs:
    f.write('\tprintf("%%8s", "%s");\n' % a);
f.write('\tprintf("\\n");');

f.write('\tprintf("\\n");');
for struct in structs:
    f.write('\tprintf("%%-25s |", "%s");\n' % struct);
    for a in archs:
        if a == arch:
            s = struct; # native
        else:
            s = struct + "_" + a;
        f.write('#ifdef %s_has_no_%s\n' % (a, struct));
        f.write('\tprintf("%8s", "-");\n');
        f.write("#else\n");
        f.write('\tprintf("%%8zd", sizeof(struct %s));\n' % s);
        f.write("#endif\n");

    f.write('\tprintf("\\n");\n\n');

f.write('\tprintf("\\n");\n');
f.write('\texit(0);\n');
f.write('}\n');

f.close();

