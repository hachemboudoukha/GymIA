"""
Exemple d'utilisation des détecteurs d'exercices.

Ce fichier montre comment utiliser chaque détecteur individuellement.
"""

import cv2
from exercises import (
    PushUpDetector,
    BicepsCurlDetector,
    PullUpDetector,
    SquatDetector
)


def example_push_up():
    """Exemple d'utilisation du détecteur de push-ups."""
    print("Exemple: Détection de push-ups")
    print("=" * 50)
    
    # Initialiser le détecteur
    detector = PushUpDetector()
    
    # Initialiser la webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Erreur: Impossible d'ouvrir la webcam")
        return
    
    print("Appuyez sur 'q' pour quitter")
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Détecter
            annotated_frame, results = detector.detect(frame)
            
            # Afficher
            cv2.imshow('Push-up Detection', annotated_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print(f"Total de répétitions: {detector.get_stats()['counter']}")


def example_biceps_curl():
    """Exemple d'utilisation du détecteur de biceps curls."""
    print("Exemple: Détection de biceps curls")
    print("=" * 50)
    
    detector = BicepsCurlDetector()
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Erreur: Impossible d'ouvrir la webcam")
        return
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            annotated_frame, results = detector.detect(frame)
            cv2.imshow('Biceps Curl Detection', annotated_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print(f"Total de répétitions: {detector.get_stats()['counter']}")


def example_pull_up():
    """Exemple d'utilisation du détecteur de pull-ups."""
    print("Exemple: Détection de pull-ups")
    print("=" * 50)
    
    detector = PullUpDetector()
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Erreur: Impossible d'ouvrir la webcam")
        return
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            annotated_frame, results = detector.detect(frame)
            cv2.imshow('Pull-up Detection', annotated_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print(f"Total de répétitions: {detector.get_stats()['counter']}")


def example_squat():
    """Exemple d'utilisation du détecteur de squats."""
    print("Exemple: Détection de squats")
    print("=" * 50)
    
    detector = SquatDetector()
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Erreur: Impossible d'ouvrir la webcam")
        return
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            annotated_frame, results = detector.detect(frame)
            cv2.imshow('Squat Detection', annotated_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print(f"Total de répétitions: {detector.get_stats()['counter']}")


if __name__ == "__main__":
    print("\nChoisissez un exemple à exécuter:")
    print("1. Push-up")
    print("2. Biceps Curl")
    print("3. Pull-up")
    print("4. Squat")
    
    choice = input("\nVotre choix (1-4): ").strip()
    
    examples = {
        "1": example_push_up,
        "2": example_biceps_curl,
        "3": example_pull_up,
        "4": example_squat
    }
    
    func = examples.get(choice)
    if func:
        func()
    else:
        print("Choix invalide!")



