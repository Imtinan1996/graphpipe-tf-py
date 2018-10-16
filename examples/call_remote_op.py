#!/usr/bin/env python
#
# Copyright (c) 2018, Oracle and/or its affiliates. All rights reserved.
#
# Licensed under the Universal Permissive License v 1.0 as shown at
# http://oss.oracle.com/licenses/upl.

"""This example illustrates using remote_ops in a tensorflow graph

In this example, we use two calls to the same VGG graph. We collect
the output of the last fully connected layer and then send that as
input through the rest of the graph to get class predictions.

This illustrates how one might extract bottleneck features from a
trained model and use them as input to another model.
"""

import argparse

import numpy as np
from graphpipe_tf import ops
import tensorflow as tf

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--inputs', nargs='+',
                        help='inputs to send to model')

    args = parser.parse_args()
    inputs = []
    for fname in args.inputs:
        with open(fname, mode='rb') as f:
            inputs.append([f.read()])

    g1 = tf.Graph()
    with g1.as_default():
        x = tf.placeholder(tf.string, shape=(None, 1))
        bottle = ops.remote_op_multi(
            "http://localhost:9000",
            [x],
            ["import/input"],
            ["import/fc2/Relu:0"],
            output_types=[tf.float32]
        )
        y = ops.remote_op(
            "http://localhost:9000",
            bottle[0],
            "import/fc2/Relu:0"
        )
    with tf.Session(graph=g1) as sess:
        res = sess.run(y, feed_dict={x: inputs})
    print(res)
