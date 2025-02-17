import argparse
import logging
import pathlib
import subprocess
import sys

PROJECT_DIR = pathlib.Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description='Run multiple experiments.')
parser.add_argument('--batch_size_train', type=int, default=230, help='Batch size for training.')
parser.add_argument('--batch_size_val', type=int, default=128, help='Batch size for validation.')
parser.add_argument('--batch_size_test', type=int, default=1, help='Batch size for testing.')

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
        'gru+cross+trans-encoder': ['--seq2seq_method', 'gru', '--use_transformer', '--encoder_only', '--use_cross_attention'],
        'gru+trans-encoder': ['--seq2seq_method', 'gru', '--use_transformer', '--encoder_only'],
        'lstm': ['--seq2seq_method', 'lstm'],
        'trans-encoder': ['--use_transformer', '--encoder_only'],
        'trans': ['--use_transformer'],
    }
    # run main.py with different args]
    processes = []
    for run_name, args in runs.items():
        logger.info(f'Running {run_name}, Args: {args}')
        args += ['--work_dir', f'./trained_models/{run_name}', '--run_name', run_name]
        p = subprocess.Popen([sys.executable, 'main.py'] + args, cwd=PROJECT_DIR)
        p.wait()