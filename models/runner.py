import logging
import pathlib
import subprocess
import sys

PROJECT_DIR = pathlib.Path(__file__).resolve().parents[1]

"""
parser.add_argument('--debug', type="store_true", default=False, help='Whether to use debug model.')
parser.add_argument('--use_transformer', type="store_true", default=False, help='Whether to use transformer.')
parser.add_argument('--use_3d', type="store_true", default=True, help='Whether to use 3D.')
parser.add_argument('--use_cross_attention', type="store_true", default=False, help='Whether to use cross attention.')
parser.add_argument('--seq2seq_method', type=str, default='gru', choices=['gru', 'lstm', 'none'], help='Seq2Seq method to use.')

parser.add_argument('--work_dir', type=str, default='./trained_models', help='Directory to save trained models.')
parser.add_argument('--log_file', type=str, default='log_test.txt', help='Log file name.')
"""

logger = logging.getLogger()
logger.handlers.clear()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

if __name__ == '__main__':
    runs = {
        'gru': ['--seq2seq_method', 'gru'],
        'gru+3d': ['--seq2seq_method', 'gru', '--use_3d'],
        # 'gru+cross+trans': ['--seq2seq_method', 'gru', '--use_transformer', '--use_cross_attention'],
        # 'gru+trans': ['--seq2seq_method', 'gru', '--use_transformer'],
        # 'lstm': ['--seq2seq_method', 'lstm'],
        # 'trans-encoder': ['--use_transformer'],
        # 'trans': ['--use_transformer'],
    }
    # run main.py with different args]
    processes = []
    for run_name, args in runs.items():
        logger.info(f'Running {run_name}, Args: {args}')
        args += ['--work_dir', f'./trained_models/{run_name}', '--run_name', run_name]
        p = subprocess.Popen([sys.executable, 'main.py'] + args, cwd=PROJECT_DIR)
        processes.append(p)
    for p in processes:
        p.wait()
