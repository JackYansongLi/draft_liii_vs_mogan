from __future__ import annotations
import argparse, json, os
import matplotlib.pyplot as plt
from typing import List, Tuple


# Fixed smoothing window for the displayed moving average
SMOOTH_WINDOW = 7
# Deep blue palette for raw and smoothed curves
TEXMACS_COLOR = "#0044C1"
LATEX_COLOR = "#7c1313"


def moving_avg(xs: List[float], k: int) -> List[float]:
	if k <= 1:
		return xs
	out, acc = [], 0.0
	for i, v in enumerate(xs):
		acc += v
		if i >= k:
			acc -= xs[i - k]
		out.append(acc / min(i + 1, k))
	return out


def parse_jsonl_loss(path: str) -> Tuple[List[int], List[float]]:
	steps, losses = [], []
	with open(path, 'r', encoding='utf-8') as f:
		for idx, line in enumerate(f, start=1):
			if not line.strip():
				continue
			try:
				obj = json.loads(line)
			except json.JSONDecodeError:
				continue
			if 'loss' not in obj:
				continue
			loss_val = obj['loss']
			try:
				loss_float = float(loss_val)
			except (TypeError, ValueError):
				continue
			step_val = obj.get('step', obj.get('current_steps', idx))
			steps.append(step_val)
			losses.append(loss_float)
	return steps, losses


def plot_loss(ax, steps: List[int], losses: List[float], color: str, label: str, smooth: int):
	if not steps:
		return False
	loss_s = moving_avg(losses, smooth)
	ax.plot(steps, losses, label=f'{label} (raw)', color=color, alpha=0.3)
	ax.plot(steps, loss_s, label=f'{label} (MA{smooth})', color=color)
	return True


def main():
	texmacs_path = "log_texmacs.jsonl"
	latex_path = "log_latex.jsonl"

	fig, ax = plt.subplots(figsize=(8, 5))

	if texmacs_path and os.path.isfile(texmacs_path):
		steps, losses = parse_jsonl_loss(texmacs_path)
		plot_loss(ax, steps, losses, TEXMACS_COLOR, 'Mogan Loss', SMOOTH_WINDOW)
	else:
		print(f'Warning: cannot read {texmacs_path}')
	if latex_path:
		if os.path.isfile(latex_path):
			steps, losses = parse_jsonl_loss(latex_path)
			plot_loss(ax, steps, losses, LATEX_COLOR, 'LaTeX Loss', SMOOTH_WINDOW)
		else:
			print(f'Warning: cannot read {latex_path}')

	ax.set_xlabel('Step')
	ax.set_ylabel('Loss')
	ax.legend()
	ax.grid(True, alpha=0.3)
	fig.tight_layout()

	plt.show()


if __name__ == '__main__':
	main()