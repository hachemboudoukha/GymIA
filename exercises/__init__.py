"""
Module d'exercices de détection de fitness.
"""

from .push_up.push_up_detector import PushUpDetector
from .biceps_curl.biceps_curl_detector import BicepsCurlDetector
from .pull_up.pull_up_detector import PullUpDetector
from .squat.squat_detector import SquatDetector

__all__ = [
    'PushUpDetector',
    'BicepsCurlDetector',
    'PullUpDetector',
    'SquatDetector'
]



