DO : pip -r requirements.txt or pip install colorama (since you only need to download one python lib)
⚠️⚠️ Made for ethical and learning purposes only !! ⚠️⚠️


### ------------------------ FRENCH HERE ------------------------ ###
Scanner de ports en asynchrone développé en python

## CARACTERISTIQUES
- **Asynchrone** : Utilisation de asyncio pour avoir un scan rapide au lieu de O(n) on a O(n/K) ou K est la valeur du sémaphore
- **Gestion des flux** : Utilisation d'un `Sémaphore` pour éviter une saturation
- **Couleurs** : Outputs coloré avec colorama :P

## STRUCTURE
- `main.py` : Point d'entrée, lancement du scanner de ports
- `/src/scanner.py` : Le code du scanner de ports
- `requirements.txt` : Les dépendances du projet

Ici les goulots d'étranglements sont les entrées / sorties réseau (I/O bound)


### ------------------------ ENGLISH HERE ------------------------ ###
Async port scanner developped in python

## CARACTERISTICS
- **Async** : Usage of asyncio for a faster scan otherwise it would have a complexity of O(n) but we have instead O(n/K) where K equals the val of the semaphore
- **Flow management** : Usage of a `Semaphore` to avoid saturation
- **Colors** : Colored outputs using colorama :P

## STRUCTURE
- `main.py` : Entry point, launch of the ports scanner
- `/src/scanner.py` : Ports scanner code
- `requirements.txt` : Project dependencies

Tho, the bottleneck here are the I/O bound

**.exe file made with pyinstaller, and you can download it in releases**
