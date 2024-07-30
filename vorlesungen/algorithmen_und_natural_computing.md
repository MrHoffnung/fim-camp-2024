# Algorithmen & Natural Computing
- **Dozent**: Prof. Dr. Gordon Fraser
- **Schriftführer**: Zhuo "Christoph" Chen
- **Zeitraum**: 29.07.2024 | 13:30-14:30

## Eigenschaften von Algorithmen
- **Finitheit**: Der Algorithmus selbst muss eine endliche Beschreibung haben.
- **Terminierung**: Die Anzahl der Schritte ist endlich, das Verfahren liefert nach dem finalen Schritt ein Ergebnis.
- **Komplexität**: Wie lange braucht der Algorithmus und wie viel Speicher benötigt er?
- **Determiniertheit**: Das Schema ist deterministisch, weil es jedem Teilergebnis einen eindeutigen nächsten Schritt zuordnet.
- **Korrektheit**: Funktioniert der Algorithmus und werden die erwarteten Ergebnisse erzielt?

## Suchalgorithmen
- **Lineare Suche**: Geht die Liste Element für Element durch, bis man es gefunden hat. <br>
    - **Bester Fall**: $O(n)=1$ 
    - **Schlechtester Fall**: $O(n)=n$
- **Binäre Suche**: Teilt eine sortierte Liste oder Array in zwei Hälften und wiederholt die Suche in der entsprechenden Hälfte, bis der gesuchte Wert gefunden ist oder die Suche abgebrochen wird. 
    - **Bester Fall**: $O(n)=1$ 
    - **Schlechtester Fall**: $log{n}$

## Sortieralgorithmen
- **Bubble Sort**: Die größeren Elemente bewegen sich nach und nach von links nach rechts in der Folge. Sie steigen somit ähnlich wie Blasen im Wasser nach oben, daher auch der Name Bubblesort.
    - **Bester Fall**: $n*O(n)=n-1$
    - **Schlechtester Fall**: $n*(n-1)$
- **Insertion Sort**:  Sortiert Datenmenge, indem er sie von vorn bis hinten durchgeht, die Elemente vergleicht und bei Bedarf ein Element entnimmt und weiter vorn wieder einsetzt.
    - **Bester Fall**: $n*O(n)=n-1$
    - **Schlechtester Fall**: $n*(n-1)$
- **Merge Sort**: Zerlegt Liste rekursiv in kleinere Teillisten, sortiert diese und fügt sie anschließend zu einer sortierten Gesamtliste zusammen.
    - **Bester Fall**: $O(n)=n*log{n}$
    - **Schlechtester Fall**: $O(n)=n*log{_2}{n}$

## P vs NP
Man unterscheidet zwischen polynomialer (P) und nicht polynomialer, also exponentieller, Komplexität (NP). Aktuell steht noch aus zu beweise ob $NP ∈ P$ gilt.

## Heuristik
Bei Heuristik handelt es sich um die Ermittlung von Näherungswerten zu einem Problem. Sie ist für einfache Probleme und schnelle Ergebnisfindung sehr praktisch. <br>
Allerdings können die Ergebnisse ungenau und nicht optimal sein und sind oftmals sehr situationsabhängig. <br>
Heuristik wird sehr häufig im Natural Computing genutzt.

## Natural Computing
Natural Computing ist ein interdisziplinäres Forschungsfeld, das sich mit der Untersuchung und dem Einsatz von Rechenprozessen beschäftigt, die in der Natur vorkommen. Diese Prozesse werden verwendet, um Probleme zu lösen oder Technologien zu entwickeln, die von natürlichen Systemen inspiriert sind. 