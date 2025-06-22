**Możliwe argumenty dla algorytmów w CLI:**

--input, -i **(wymagane)** – ścieżka do pliku z instancją<br>
--target, -T – nadpisuje target z pliku<br>
--algorithm, -a **(wymagane)** – jeden z full, hill, tabu, sa<br>
--neighborhood, -n – flip lub all (domyślnie flip)<br>
--time-limit, -t – limit czasu w sekundach<br>
--seed, -s – ziarno generatora losowego<br>

**Przykład:**<br>
python -m solver.cli --algorithm full --input data/small.txt --time-limit 5 --seed 42<br>
python -m solver.cli --algorithm hill --input data/medium.txt --neighborhood all --time-limit 2 --seed 1<br>
python -m solver.cli --algorithm tabu --input data/medium.txt --neighborhood all --tabu-size 30 --time-limit 2 --seed 1<br>
python -m solver.cli --algorithm sa --input data/large.txt --schedule exponential --initial-temp 500 --alpha 0.9 --min-temp 0.01 --time-limit 5 --seed 1<br>

Zmierzone przykłady:<br>
_limit 60 sekund_<br>
Wspinaczkowy deterministyczny, input 1k<br>
![large_hill_det.png](assets%2Flarge_hill_det.png)<br>
Wspinaczkowy losowy, input 1k<br>
![large_hill_rand.png](assets%2Flarge_hill_rand.png)<br>
Wspinaczkowy deterministyczny, input 10k<br>
![huge_hill_det.png](assets%2Fhuge_hill_det.png)<br>
Wspinaczkowy losowy, input 10k<br>
![huge_hill_rand.png](assets%2Fhuge_hill_rand.png)<br>

**Wnioski**
Algorytm wspinaczkowy lepiej radzi sobie przy podejściu deterministycznym 
w obu przypadkach, oba są jednak mało skuteczne dla próbki wielkości 10k.

Tabu na rozmiarze 10, input 1k <br>
![large_tabu.png](assets%2Flarge_tabu.png)<br>
Tabu na rozmiarze 10, input 10k <br>
![huge_tabu.png](assets%2Fhuge_tabu.png)<br>
Tabu na rozmiarze 20, input 1k <br>
<br>
Tabu na rozmiarze 20, input 10k <br>
<br>
