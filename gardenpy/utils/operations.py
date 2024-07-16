import gc

import numpy as np

from .objects import Tensor


def nabla(grad, rspc):
    id_grad = id(grad)
    id_rspc = id(rspc)
    id_track = [rlt[1] for rlt in rspc._tracker['relations']]
    id_other = [rlt[0] for rlt in rspc._tracker['relations']]
    if not isinstance(rspc, Tensor):
        raise TypeError('not tensor')
    if id_grad in id_track:
        # todo: add default chain ruling here
        def d_matmul_m(_grad, _rspc):
            ...  # todo

        def d_matmul_c(_rspc, _other):
            ...  # todo

        def d_mul(_rspc, _other):
            ...  # todo

        def d_truediv_n(_rspc, _other):
            ...  # todo

        def d_truediv_d(_rspc, _other):
            ...  # todo

        def d_add(_rspc, _other):
            return _rspc * 0.0 + 1.0

        def d_sub_s(_rspc, _other):
            return _rspc * 0.0 + 1.0

        def d_sub_m(_rspc, _other):
            return _rspc * 0.0 - 1.0

        back = {
            'matmul_m': d_matmul_m,
            'matmul_c': d_matmul_c,
            'mul': d_mul,
            'truediv_n': d_truediv_n,
            'truediv_d': d_truediv_d,
            'add': d_add,
            'sub_s': d_sub_s,
            'sub_m': d_sub_m
        }

        operation_type = rspc._tracker['operations'][id_track.index(id_grad)]
        result = back[operation_type](rspc, other)
        result._type = 'grad'
        result._tracker['operations'].append(f'd_{operation_type}')
        result._tracker['relations'].append([id_grad, id_rspc])
        return result
    else:
        raise ValueError('no relation')


def chain(grad_loc, grad_glob):
    if not isinstance(grad_loc, Tensor):
        raise TypeError('loc not tensor')
    if not isinstance(grad_glob, Tensor):
        raise TypeError('glob not tensor')

    if not (grad_loc._type == 'grad' and grad_glob._type == 'grad'):
        raise TypeError('not gradients')

    glob_conn = grad_glob._tracker['relations'][0][0]
    loc_conn = grad_loc._tracker['relations'][-1][1]
    if glob_conn == loc_conn:
        result = Tensor(np.dot(grad_loc.to_np(), grad_glob.to_np()))  # todo: check this math
        result._type = 'grad'
        result._tracker['relations'] = grad_loc._tracker['relations'] + grad_glob._tracker['relations']
        result._tracker['operations'] = grad_loc._tracker['operations'] + grad_glob._tracker['operations']
        return result
    else:
        raise TypeError('no relation')
