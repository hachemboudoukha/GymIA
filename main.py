"""
Application principale pour la détection d'exercices en temps réel.

Ce module permet de sélectionner et d'utiliser différents détecteurs d'exercices
via la webcam en temps réel.
"""

import cv2
import sys
from pathlib import Path

# Ajouter le répertoire racine au path
sys.path.insert(0, str(Path(__file__).parent))

from exercises import (
    PushUpDetector,
    BicepsCurlDetector,
    PullUpDetector,
    SquatDetector
)


def select_exercise() -> str:
    """
    Affiche un menu pour sélectionner l'exercice.
    
    Returns:
        Nom de l'exercice sélectionné
    """
    print("\n" + "="*50)
    print("GYMIA - Détection d'Exercices en Temps Réel")
    print("="*50)
    print("\nSélectionnez un exercice:")
    print("1. Push-up")
    print("2. Biceps Curl")
    print("3. Pull-up")
    print("4. Squat")
    print("0. Quitter")
    print("="*50)
    
    choice = input("\nVotre choix: ").strip()
    
    exercise_map = {
        "1": "push_up",
        "2": "biceps_curl",
        "3": "pull_up",
        "4": "squat"
    }
    
    return exercise_map.get(choice, None)


def get_detector(exercise_name: str):
    """
    Crée et retourne le détecteur approprié.
    
    Args:
        exercise_name: Nom de l'exercice
    
    Returns:
        Instance du détecteur approprié
    """
    detectors = {
        "push_up": PushUpDetector,
        "biceps_curl": BicepsCurlDetector,
        "pull_up": PullUpDetector,
        "squat": SquatDetector
    }
    
    detector_class = detectors.get(exercise_name)
    if detector_class is None:
        raise ValueError(f"Exercice inconnu: {exercise_name}")
    
    return detector_class()


def main():
    """Fonction principale de l'application."""
    # Sélectionner l'exercice
    exercise = select_exercise()
    
    if exercise is None:
        print("Au revoir!")
        return
    
    # Créer le détecteur
    try:
        detector = get_detector(exercise)
        print(f"\nDétecteur {exercise} initialisé avec succès!")
    except Exception as e:
        print(f"Erreur lors de l'initialisation: {e}")
        return
    
    # Initialiser la webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Erreur: Impossible d'ouvrir la webcam")
        return
    
    print("\nInstructions:")
    print("- Appuyez sur 'q' pour quitter")
    print("- Appuyez sur 'r' pour réinitialiser le compteur")
    print("- Assurez-vous que votre corps est bien visible dans le cadre")
    print("\nDémarrage de la détection...\n")
    
    try:
        while True:
            # Lire la frame
            ret, frame = cap.read()
            
            if not ret:
                print("Erreur: Impossible de lire la frame")
                break
            
            # Détecter l'exercice
            annotated_frame, results = detector.detect(frame)
            
            # Afficher la frame
            cv2.imshow('GymIA - Detection d\'Exercices', annotated_frame)
            
            # Gérer les touches
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                print("\nArrêt de la détection...")
                break
            elif key == ord('r'):
                detector.reset_counter()
                print("Compteur réinitialisé!")
            
            # Afficher les résultats dans la console (optionnel)
            if results.get('pose_detected'):
                if results.get('angle') is not None:
                    print(f"\rReps: {results['counter']} | Stage: {results['stage']} | Angle: {int(results['angle'])}°", end='', flush=True)
    
    except KeyboardInterrupt:
        print("\n\nInterruption par l'utilisateur")
    except Exception as e:
        print(f"\nErreur: {e}")
    finally:
        # Nettoyer
        cap.release()
        cv2.destroyAllWindows()
        
        # Afficher les statistiques finales
        stats = detector.get_stats()
        print(f"\n\nStatistiques finales:")
        print(f"Total de répétitions: {stats['counter']}")
        print("Merci d'avoir utilisé GymIA!")


if __name__ == "__main__":
    main()



