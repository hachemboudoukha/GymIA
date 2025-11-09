"""
Module de détection et comptage des squats.

Ce module utilise MediaPipe Pose pour détecter les squats en temps réel
en analysant l'angle du genou.
"""

import cv2
import numpy as np
import mediapipe as mp
from typing import Tuple, Optional, Dict
from pathlib import Path
import json

from utils.angle_calculator import calculate_knee_angle


class SquatDetector:
    """
    Détecteur de squats utilisant MediaPipe Pose.
    
    Analyse l'angle du genou pour détecter les répétitions de squats.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialise le détecteur de squats.
        
        Args:
            config_path: Chemin vers le fichier de configuration JSON
        """
        # Charger la configuration
        if config_path is None:
            config_path = Path(__file__).parent / "squat_config.json"
        
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        # Initialiser MediaPipe Pose
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=self.config.get('min_detection_confidence', 0.5),
            min_tracking_confidence=self.config.get('min_tracking_confidence', 0.5),
            model_complexity=self.config.get('model_complexity', 1)
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Paramètres de détection
        self.min_angle = self.config.get('min_angle', 90.0)  # Angle minimum (position basse)
        self.max_angle = self.config.get('max_angle', 160.0)  # Angle maximum (position haute)
        self.side = self.config.get('side', 'left')  # Côté à analyser
        
        # État de détection
        self.counter = 0
        self.stage = "up"  # "down" ou "up"
        self.current_angle = None
        
    def detect(self, frame: np.ndarray) -> Tuple[np.ndarray, Dict]:
        """
        Détecte les squats dans une frame vidéo.
        
        Args:
            frame: Frame vidéo (BGR)
        
        Returns:
            Tuple contenant:
                - Frame annotée avec les landmarks et informations
                - Dictionnaire avec les résultats de détection
        """
        # Convertir BGR en RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        
        # Détecter la pose
        results = self.pose.process(image)
        
        # Reconvertir en BGR pour l'affichage
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Dessiner les landmarks
        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                self.mp_drawing.DrawingSpec(
                    color=(0, 255, 0),
                    thickness=2,
                    circle_radius=2
                ),
                self.mp_drawing.DrawingSpec(
                    color=(0, 0, 255),
                    thickness=2
                )
            )
            
            # Calculer l'angle du genou
            self.current_angle = calculate_knee_angle(
                results.pose_landmarks,
                side=self.side
            )
            
            # Détecter la répétition
            if self.current_angle is not None:
                self._update_counter()
        
        # Ajouter les informations à l'image
        image = self._draw_info(image)
        
        # Préparer les résultats
        detection_results = {
            'counter': self.counter,
            'stage': self.stage,
            'angle': self.current_angle,
            'pose_detected': results.pose_landmarks is not None
        }
        
        return image, detection_results
    
    def _update_counter(self) -> None:
        """
        Met à jour le compteur de répétitions basé sur l'angle du genou.
        """
        if self.current_angle is None:
            return
        
        # Position basse (squat): angle < min_angle
        if self.current_angle < self.min_angle:
            if self.stage == "up":
                self.stage = "down"
        
        # Position haute (debout): angle > max_angle
        elif self.current_angle > self.max_angle:
            if self.stage == "down":
                self.stage = "up"
                self.counter += 1
    
    def _draw_info(self, image: np.ndarray) -> np.ndarray:
        """
        Dessine les informations de détection sur l'image.
        
        Args:
            image: Image à annoter
        
        Returns:
            Image annotée
        """
        # Zone d'information
        cv2.rectangle(image, (0, 0), (300, 150), (0, 0, 0), -1)
        cv2.rectangle(image, (0, 0), (300, 150), (255, 255, 255), 2)
        
        # Titre
        cv2.putText(
            image,
            "SQUAT",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )
        
        # Compteur
        cv2.putText(
            image,
            f"Reps: {self.counter}",
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )
        
        # Stage
        stage_color = (0, 255, 0) if self.stage == "up" else (0, 0, 255)
        cv2.putText(
            image,
            f"Stage: {self.stage.upper()}",
            (10, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            stage_color,
            2
        )
        
        # Angle
        if self.current_angle is not None:
            cv2.putText(
                image,
                f"Angle: {int(self.current_angle)}°",
                (10, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2
            )
        
        return image
    
    def reset_counter(self) -> None:
        """Réinitialise le compteur de répétitions."""
        self.counter = 0
        self.stage = "up"
    
    def get_stats(self) -> Dict:
        """
        Retourne les statistiques actuelles.
        
        Returns:
            Dictionnaire avec les statistiques
        """
        return {
            'counter': self.counter,
            'stage': self.stage,
            'current_angle': self.current_angle
        }



