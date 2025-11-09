"""
Module utilitaire pour calculer les angles articulaires à partir des landmarks MediaPipe.

Ce module fournit des fonctions pour calculer les angles entre trois points,
ce qui est essentiel pour analyser les mouvements d'exercices.
"""

import numpy as np
from typing import Tuple, Optional


def calculate_angle(
    point_a: np.ndarray,
    point_b: np.ndarray,
    point_c: np.ndarray
) -> float:
    """
    Calcule l'angle formé par trois points (point_b est le sommet de l'angle).
    
    Args:
        point_a: Premier point (landmark MediaPipe)
        point_b: Point central (sommet de l'angle)
        point_c: Troisième point (landmark MediaPipe)
    
    Returns:
        Angle en degrés (0-180)
    
    Raises:
        ValueError: Si les points sont invalides ou identiques
    """
    if point_a is None or point_b is None or point_c is None:
        raise ValueError("Tous les points doivent être valides")
    
    # Convertir en arrays numpy si nécessaire
    a = np.array(point_a)
    b = np.array(point_b)
    c = np.array(point_c)
    
    # Vérifier que les points ne sont pas identiques
    if np.array_equal(a, b) or np.array_equal(b, c) or np.array_equal(a, c):
        raise ValueError("Les points ne peuvent pas être identiques")
    
    # Calculer les vecteurs
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    # Normaliser l'angle entre 0 et 180
    if angle > 180.0:
        angle = 360 - angle
    
    return angle


def get_landmark_coordinates(
    landmarks: any,
    landmark_index: int
) -> Optional[Tuple[float, float]]:
    """
    Extrait les coordonnées (x, y) d'un landmark MediaPipe.
    
    Args:
        landmarks: Objet landmarks MediaPipe
        landmark_index: Index du landmark (0-32)
    
    Returns:
        Tuple (x, y) ou None si le landmark n'est pas visible
    """
    if landmarks is None or landmark_index < 0 or landmark_index >= 33:
        return None
    
    try:
        landmark = landmarks.landmark[landmark_index]
        # Vérifier la visibilité du landmark
        if landmark.visibility < 0.5:
            return None
        return (landmark.x, landmark.y)
    except (IndexError, AttributeError):
        return None


def calculate_elbow_angle(
    landmarks: any,
    side: str = "left"
) -> Optional[float]:
    """
    Calcule l'angle du coude pour un côté donné.
    
    Args:
        landmarks: Objet landmarks MediaPipe
        side: "left" ou "right"
    
    Returns:
        Angle du coude en degrés ou None si les landmarks ne sont pas visibles
    """
    if side == "left":
        shoulder_idx = 11  # Épaule gauche
        elbow_idx = 13     # Coude gauche
        wrist_idx = 15     # Poignet gauche
    else:  # right
        shoulder_idx = 12  # Épaule droite
        elbow_idx = 14     # Coude droit
        wrist_idx = 16     # Poignet droit
    
    shoulder = get_landmark_coordinates(landmarks, shoulder_idx)
    elbow = get_landmark_coordinates(landmarks, elbow_idx)
    wrist = get_landmark_coordinates(landmarks, wrist_idx)
    
    if shoulder is None or elbow is None or wrist is None:
        return None
    
    try:
        return calculate_angle(shoulder, elbow, wrist)
    except ValueError:
        return None


def calculate_knee_angle(
    landmarks: any,
    side: str = "left"
) -> Optional[float]:
    """
    Calcule l'angle du genou pour un côté donné.
    
    Args:
        landmarks: Objet landmarks MediaPipe
        side: "left" ou "right"
    
    Returns:
        Angle du genou en degrés ou None si les landmarks ne sont pas visibles
    """
    if side == "left":
        hip_idx = 23      # Hanche gauche
        knee_idx = 25     # Genou gauche
        ankle_idx = 27   # Cheville gauche
    else:  # right
        hip_idx = 24      # Hanche droite
        knee_idx = 26     # Genou droit
        ankle_idx = 28    # Cheville droite
    
    hip = get_landmark_coordinates(landmarks, hip_idx)
    knee = get_landmark_coordinates(landmarks, knee_idx)
    ankle = get_landmark_coordinates(landmarks, ankle_idx)
    
    if hip is None or knee is None or ankle is None:
        return None
    
    try:
        return calculate_angle(hip, knee, ankle)
    except ValueError:
        return None



