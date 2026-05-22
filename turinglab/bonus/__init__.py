"""TuringLab bonus modülleri (el kitabı Bölüm bonus).

- ``TwoTapeTM``: iki şeritli deterministik TM
- ``NondeterministicTM``: BFS ile NTM simülasyonu
- ``step_compare``: adım sayısı karşılaştırma ve grafik (matplotlib isteğe bağlı)
- ``visualize``: şerit kareleri PPM / GIF (Pillow isteğe bağlı)
"""

from turinglab.bonus.multi_tape import MultiTapeTM, MultiTapeStep
from turinglab.bonus.ntm_bfs import BFSResult, NondeterministicTM, NTMStep
from turinglab.bonus.step_compare import StepComparison, compare_step_counts, save_comparison
from turinglab.bonus.visualize import export_history_gif, export_history_ppm, write_ppm_frame

__all__ = [
    "BFSResult",
    "MultiTapeStep",
    "MultiTapeTM",
    "NTMStep",
    "NondeterministicTM",
    "StepComparison",
    "compare_step_counts",
    "export_history_gif",
    "export_history_ppm",
    "save_comparison",
    "write_ppm_frame",
]
