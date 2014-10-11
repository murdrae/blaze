from blaze.partition import *

import numpy as np

x = np.arange(24).reshape(4, 6)


def eq(a, b):
    if isinstance(a == b, bool):
        return a == b
    if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
        return (a == b).all()
    else:
        return a == b


def test_partition_get():
    assert eq(partition_get(x, (0, slice(0, None)), blockshape=(1, 6)),
              x[0, :])
    assert eq(partition_get(x, (slice(0, None), 0), blockshape=(4, 1)),
              x[:, 0])
    assert eq(partition_get(x, (slice(2, 4), slice(0, 2)), blockshape=(2, 2)),
              x[2:4, 0:2])


def test_partition_set():
    x = np.arange(24).reshape(4, 6)
    partition_set(x, (slice(0, 2), slice(0, 2)), np.array([[1, 1], [1, 1]]))

    assert (x[:2, :2] == 1).all()


def test_partitions():
    assert partitions(x, blockshape=(1, 6)) == \
            [[(i, slice(0, 6))] for i in range(4)]
    assert partitions(x, blockshape=(4, 1)) == \
            [[(slice(0, 4), i) for i in range(6)]]
    assert partitions(x, blockshape=(2, 3)) == [
            [(slice(0, 2), slice(0, 3)), (slice(0, 2), slice(3, 6))],
            [(slice(2, 4), slice(0, 3)), (slice(2, 4), slice(3, 6))]]


def dont_test_partitions_flat():
    assert partitions(x, blockshape=(2, 3)) == [
            (slice(0, 2), slice(0, 3)), (slice(0, 2), slice(3, 6)),
            (slice(2, 4), slice(0, 3)), (slice(2, 4), slice(3, 6))]


def test_slicesnd():
    assert slicesnd((6, 4), (3, 2)) == \
    [[(slice(0, 3, None), slice(0, 2, None)),
      (slice(0, 3, None), slice(2, 4, None))],
     [(slice(3, 6, None), slice(0, 2, None)),
      (slice(3, 6, None), slice(2, 4, None))]]
