#!/usr/bin/env python3


import jinja2
import argparse
import os
import fnmatch
import numpy as np

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('env_dir')
    parser.add_argument('--mavlink_tcp_port', default=4560)
    parser.add_argument('--mavlink_udp_port', default=14560)
    args = parser.parse_args()
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(args.env_dir))
    template = env.get_template(os.path.relpath(args.filename, args.env_dir))

    # create dictionary with useful modules etc.
    try:
        import rospkg
        rospack = rospkg.RosPack()
    except ImportError:
        pass
        rospack = None

    d = {'np': np, 'rospack': rospack, 'mavlink_tcp_port': args.mavlink_tcp_port, 'mavlink_udp_port': args.mavlink_udp_port}
    result = template.render(d)
    filename_out = args.filename.replace('.sdf.jinja', '-gen.sdf')
    with open(filename_out, 'w') as f_out:
        print(('{:s} -> {:s}'.format(args.filename, filename_out)))
        f_out.write(result)
