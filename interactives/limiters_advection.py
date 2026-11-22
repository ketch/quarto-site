"""Compute the advection results shown on interactives/limiters.qmd.

Uses the same PyClaw setup as the "Comparison of several limiters for advection"
section of HyperPython's Guide_to_limiters.ipynb, with 5 output frames per cycle
instead of 1 so that the page can animate the solution smoothly.

Run from the site root:
    python3 interactives/limiters_advection.py interactives/limiters_advection.json
"""
import json
import sys

import numpy as np
from clawpack import pyclaw, riemann

FRAMES_PER_CYCLE = 5
CYCLES = 10
SCHEMES = ('first-order', 'Lax-Wendroff', 'minmod', 'superbee', 'MC', 'vanleer',
           'weno5', 'weno7', 'weno9')


def setup(scheme='minmod', cfl_max=0.9, mx=100):
    if 'weno' in scheme:
        solver = pyclaw.SharpClawSolver1D(riemann.advection_1D)
    else:
        solver = pyclaw.ClawSolver1D(riemann.advection_1D)

    solver.bc_lower[0] = pyclaw.BC.periodic
    solver.bc_upper[0] = pyclaw.BC.periodic

    if scheme in ('minmod', 'superbee', 'MC', 'vanleer'):
        solver.limiters = getattr(pyclaw.limiters.tvd, scheme)
    elif scheme == 'Lax-Wendroff':
        solver.limiters = 0
    elif scheme == 'first-order':
        solver.order = 1
    elif 'weno' in scheme:
        solver.weno_order = int(scheme[4:])
    else:
        raise ValueError('Unrecognized scheme: ' + scheme)

    solver.cfl_max = cfl_max
    solver.cfl_desired = cfl_max * 0.9

    x = pyclaw.Dimension(0.0, 1.0, mx)
    domain = pyclaw.Domain(x)
    state = pyclaw.State(domain, 1)
    state.problem_data['u'] = 1.

    xc = state.grid.x.centers
    beta, x0 = 200., 0.3
    state.q[0, :] = np.exp(-beta * (xc - x0)**2) + (xc > 0.6) * (xc < 0.8)

    claw = pyclaw.Controller()
    claw.solution = pyclaw.Solution(state, domain)
    claw.solver = solver
    claw.keep_copy = True
    claw.output_format = None
    claw.verbosity = 0
    claw.tfinal = float(CYCLES)
    claw.num_output_times = FRAMES_PER_CYCLE * CYCLES
    return claw


def main(out_path):
    data = {'framesPerCycle': FRAMES_PER_CYCLE, 'cycles': CYCLES, 'schemes': {}}
    for scheme in SCHEMES:
        claw = setup(scheme)
        claw.run()
        frames = [f.q[0, :] for f in claw.frames]
        if len(frames) != FRAMES_PER_CYCLE * CYCLES + 1:
            raise RuntimeError(f'{scheme}: got {len(frames)} frames')
        data['x'] = [round(float(v), 4) for v in claw.frames[0].p_centers[0]]
        dx = 1.0 / len(frames[0])
        err = dx * np.sum(np.abs(frames[-1] - frames[0]))
        data['schemes'][scheme] = {
            'frames': [[round(float(v), 4) for v in q] for q in frames],
            'error': float(err),
        }
        print(f'{scheme:13s} 1-norm error after {CYCLES} cycles: {err:.4f}')
    with open(out_path, 'w') as f:
        json.dump(data, f, separators=(',', ':'))


if __name__ == '__main__':
    main(sys.argv[1])
