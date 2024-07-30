# Einführung in Reinforcement Learning
- **Dozent**: Prof. Dr. Steffen Herbold
- **Schriftführer**: Leo Gall
- **Zeitraum**: 30.07.2024 | 13:30-14:30

## AI Engineering
AI Engineering beschäftigt sich mit der Nutzung von AI als Produkt von Software.

## Definition
Zwei gängige Anwendungsgebiete von Reinforcement Learning sind Robotik und die Entwicklung von Bots für Videospiele.
<br>
Für Reinforcement Learning in Videospielen benötigt man:
- Eine **Umgebung**: Die Spielewelt (nicht nur der beobachtbare, sondern der gesamte geladene Bereich)
- Einen **Agenten**: Der Spieler
- Eine **Belohnung**: Das Objekt, das zu erreichen, das Ziel des Agenten ist
- Verschiedene **Aktionen**: Die der Spieler auführen kann

**Reinforcement Learning ist die Aufgabe zu lernen, wie Agenten Sequenzen von Aktionen durchführen sollen, um die kumulativen Belohnungen zu optimieren.**

### Durchführung einer Aktion zum Zeitpunkt $t$
#### Wissen des Agenten
- Die aktuelle Beobachtung
- Evtl. Informationen über die letzten n Zeitschritte

1. Agent führt Aktion $a_t ∈ A$ durch
2. Der Zustand der Umgebung ändert sich durch die Aktion zu $s_{t+1} ∈ S$
3. Der Agent bekommt die Bleohnung $r_t$ mitgeteilt
4. Wenn nötig Wiederholung

## Markov Eigenschaft
Eine Auswahl der Aktion ist ohne Wissen über die Vergangenheit möglich. **Die Aktion hängt nur vom aktuellen Zustand ab**. <br>
Entscheidungen sollten über einen möglichst knappen Zeitraum getroffen werden, um unnötigen Datenmüll zu vermeiden.

### Markov Decision Process (MDP)
- Sei S der Zustandsraum und A der Aktionausraum
- $t: S × A × S$ -> $[0,1]$ ist die Übergangsfunktion als bedingte Wahrscheinlichkeit
- $r: S × A × S$ -> $R$ ist die Belohnungsfunktion
- $γ ∈ [0,1]$ ist der "discount factor"

### Policies
Die Policy beim Reinforcement Learning beschreibt die Strategie des Agentens. Es gibt zwei verschiedene Arten von Policies:
- Deterministisch: $π(s):S$ -> $A$ (z.B.: Schere, Stein, Papier)
- Stochastisch: $π(s,a): S×A$ -> [0,1] (z.B.: Rundenbasiertes Spiel mit verschiedenen Optionen)
    - Wahrscheinlichkeit von Aktion a in Zustand s

### Q-Learning
$Q^π(s,a)=$ Die erwartete Belohnung, wenn man im Zustand $s$ $a$ ausführt.

#### Zustandsraum oft riesig
- Wie definiert man eine Policy für eine komplexe Beobachtung mit vielen Variablen?

## Neuronale Netzwerke
- Nertzwerke von Neuronen sind organisiert in Ebenen
- Kommunikation zwischen Neuronen verschiedener Ebenen
- "Input Layer" füttert das Netzwerk mit Daten
- "Hidden Layer" gewichten und korrelieren die Daten
- "Output Layer" liefer die Ergebnisse der Berechnung

### Deep $Q$-Learning
- Input Layer: Zustand
- Hidden Layer: Policy
- Output Layer $Q$-Wert für Aktion

Über die Bellmann Gleichung wird der $Q$-Wert geschätzt.

### Training
Über die $ε$-Greedy-Q-Policy:
- Mit Wahrscheinlichkeit Epsilon zufällige Aktion
- Ansonsten bekannte Aktion mit bestem Wert $Q$
- Nach jedem Zeitschritt bessere Schätzung des $Q$-Werts möglich
- Nach jedem Schritt neues Training
<br>
**->** Zielgerichtetes durchsuchen von Kombinationen von Aktionen

### Double Deep $Q$-Learning
Stabilisieren der Fehlfunktionen durch zwei verschiedene Netzwerke

## Zusammenfassung
- Reinforcement Learning lernt optimale Sequenzen von Aktionen
- Deep Reinforcement Learning als Lösung für riesige Zustands- und Aktionsräume
- Fitneßstudio-Ansatz erlaubt dynamisches und zielgerichtetes Lernen von Trainingsdaten und Zielfunktion