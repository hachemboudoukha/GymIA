# GymIA - Détection d'Exercices en Temps Réel

Application de détection et comptage automatique d'exercices de fitness en temps réel utilisant MediaPipe Pose et OpenCV.

## 🎯 Fonctionnalités

- **Détection en temps réel** de 4 exercices :
  - Push-ups
  - Biceps Curls
  - Pull-ups
  - Squats

- **Comptage automatique** des répétitions basé sur l'analyse des angles articulaires
- **Feedback visuel** avec affichage des landmarks et statistiques
- **Architecture modulaire** pour faciliter l'ajout de nouveaux exercices

## 📋 Prérequis

- Python 3.8 ou supérieur
- Webcam
- Système d'exploitation : Linux, Windows, ou macOS

## 🚀 Installation

1. **Cloner ou télécharger le projet**

2. **Créer un environnement virtuel (recommandé)**
```bash
python -m venv venv
source venv/bin/activate  # Sur Linux/macOS
# ou
venv\Scripts\activate  # Sur Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

## 💻 Utilisation

### Application principale

Lancer l'application principale avec un menu interactif :

```bash
python main.py
```

Sélectionnez l'exercice souhaité dans le menu :
1. Push-up
2. Biceps Curl
3. Pull-up
4. Squat

### Utilisation des notebooks Jupyter

Chaque exercice possède son propre notebook pour des tests individuels :

- `exercises/push_up/push_up_detection.ipynb`
- `exercises/biceps_curl/biceps_curl_detection.ipynb`
- `exercises/pull_up/pull_up_detection.ipynb`
- `exercises/squat/squat_detection.ipynb`

Pour lancer Jupyter :
```bash
jupyter notebook
```

### Utilisation programmatique

```python
from exercises import PushUpDetector
import cv2

# Initialiser le détecteur
detector = PushUpDetector()

# Capturer la vidéo
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Détecter l'exercice
    annotated_frame, results = detector.detect(frame)
    
    # Afficher
    cv2.imshow('Detection', annotated_frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

## 🎮 Contrôles

- **'q'** : Quitter l'application
- **'r'** : Réinitialiser le compteur de répétitions

## 📊 Paramètres de détection

### Push-up
- **Angle analysé** : Coude (épaule-coude-poignet)
- **Position basse** : Angle < 90°
- **Position haute** : Angle > 160°

### Biceps Curl
- **Angle analysé** : Coude (épaule-coude-poignet)
- **Position basse** : Angle < 50°
- **Position haute** : Angle > 160°

### Pull-up
- **Angle analysé** : Coude (épaule-coude-poignet)
- **Position basse** : Angle < 90°
- **Position haute** : Angle > 160°

### Squat
- **Angle analysé** : Genou (hanche-genou-cheville)
- **Position basse** : Angle < 90°
- **Position haute** : Angle > 160°

Les paramètres peuvent être modifiés dans les fichiers de configuration JSON de chaque exercice :
- `exercises/push_up/push_up_config.json`
- `exercises/biceps_curl/biceps_curl_config.json`
- `exercises/pull_up/pull_up_config.json`
- `exercises/squat/squat_config.json`

## 📁 Structure du projet

```
GymIA/
├── main.py                      # Application principale
├── requirements.txt             # Dépendances Python
├── README.md                    # Documentation
├── utils/                       # Utilitaires
│   ├── __init__.py
│   └── angle_calculator.py      # Calcul des angles articulaires
└── exercises/                   # Modules d'exercices
    ├── __init__.py
    ├── push_up/
    │   ├── push_up_detector.py
    │   ├── push_up_config.json
    │   └── push_up_detection.ipynb
    ├── biceps_curl/
    │   ├── biceps_curl_detector.py
    │   ├── biceps_curl_config.json
    │   └── biceps_curl_detection.ipynb
    ├── pull_up/
    │   ├── pull_up_detector.py
    │   ├── pull_up_config.json
    │   └── pull_up_detection.ipynb
    └── squat/
        ├── squat_detector.py
        ├── squat_config.json
        └── squat_detection.ipynb
```

## 🔧 Configuration

Chaque exercice possède un fichier de configuration JSON permettant de personnaliser :

- `min_detection_confidence` : Confiance minimale pour la détection (0.0-1.0)
- `min_tracking_confidence` : Confiance minimale pour le suivi (0.0-1.0)
- `model_complexity` : Complexité du modèle MediaPipe (0, 1, ou 2)
- `min_angle` : Angle minimum pour la position basse (degrés)
- `max_angle` : Angle maximum pour la position haute (degrés)
- `side` : Côté à analyser ("left" ou "right")

## 🎨 Améliorations possibles

- [ ] Détection de la forme d'exécution (feedback sur la qualité)
- [ ] Support de plusieurs exercices simultanés
- [ ] Enregistrement des statistiques dans une base de données
- [ ] Interface graphique avec Tkinter ou PyQt
- [ ] Export des données d'entraînement
- [ ] Détection de fatigue basée sur la vitesse d'exécution
- [ ] Support pour l'analyse de vidéos préenregistrées

## 🐛 Dépannage

### La webcam ne s'ouvre pas
- Vérifiez que la webcam n'est pas utilisée par une autre application
- Essayez de changer l'index de la caméra : `cv2.VideoCapture(1)` au lieu de `cv2.VideoCapture(0)`

### La détection ne fonctionne pas correctement
- Assurez-vous d'avoir un bon éclairage
- Positionnez-vous face à la caméra avec tout le corps visible
- Ajustez les paramètres de confiance dans les fichiers de configuration

### Erreurs d'importation
- Vérifiez que toutes les dépendances sont installées : `pip install -r requirements.txt`
- Assurez-vous d'être dans le bon répertoire lors de l'exécution

## 📝 Licence

Ce projet est fourni à des fins éducatives et de démonstration.

## 👨‍💻 Auteur

Développé avec MediaPipe, OpenCV et Python.

## 🙏 Remerciements

- [MediaPipe](https://mediapipe.dev/) pour la détection de pose
- [OpenCV](https://opencv.org/) pour le traitement vidéo



