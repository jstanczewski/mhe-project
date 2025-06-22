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
**_limit 60 sekund_**<br>
Wspinaczkowy deterministyczny, input 1k<br>
![large_hill_det.png](assets%2Flarge_hill_det.png)<br>
Wspinaczkowy losowy, input 1k<br>
![large_hill_rand.png](assets%2Flarge_hill_rand.png)<br>
Wspinaczkowy deterministyczny, input 10k<br>
![huge_hill_det.png](assets%2Fhuge_hill_det.png)<br>
Wspinaczkowy losowy, input 10k<br>
![huge_hill_rand.png](assets%2Fhuge_hill_rand.png)<br>

**Wnioski**<br>
Algorytm wspinaczkowy lepiej radzi sobie przy podejściu deterministycznym 
w obu przypadkach, oba są jednak mało skuteczne dla próbki wielkości 10k.<br>

Tabu na rozmiarze 10, input 1k <br>
![large_tabu.png](assets%2Flarge_tabu.png)<br>
Tabu na rozmiarze 10, input 10k <br>
![huge_tabu.png](assets%2Fhuge_tabu.png)<br>
Tabu na rozmiarze 20, input 1k <br>
![large_tabu_2.png](assets%2Flarge_tabu_2.png)<br>
Tabu na rozmiarze 20, input 10k <br>
![huge_tabu_2.png](assets%2Fhuge_tabu_2.png)<br>

**Wnioski**<br>
Algorytm Tabu osiąga podobne wyniki przy rozmiarach tabu 10 i 20, lepiej od wspinaczkowego radzi sobie z danymi wejściowymi 
większego rozmiaru, ale w ciągu 60 sekund nie jest w stanie znaleźć zadowalająco bliskiej odpowiedzi.<br>

Full Search dla inputu 20 <br>
![medium_full.png](assets%2Fmedium_full.png)<br>
Full Search dla inputu 1k <br>
![large_full.png](assets%2Flarge_full.png)<br>

**Wnioski**<br>
Z oczywistych powodów algorytm pełnego przeglądu działa sprawnie dla niewielkich rozmiarów wejść,
ale nie nadaje się do większych ze względu na swą złożoność obliczeniową<br>

Symulowane wyżarzanie<br>
Testowane dla inputu 10k<br>
Harmonogram wykładniczy, wolne schładzanie, dane wejściowe<br>
init-temp 1000, alpha 0.99, min-temp 0.0001<br>
![huge_sa_exp.png](assets%2Fhuge_sa_exp.png)<br><br>
Harmonogram liniowy, wolne schładzanie, dane wejściowe<br>
init-temp 1000, alpha 0.5, min-temp 0.01<br>
![huge_sa_lin.png](assets%2Fhuge_sa_lin.png)<br><br>
Harmonogram wykładniczy, umiarkowane schładzanie, dane wejściowe<br>
init-temp 500, alpha 0.95, min-temp 0.0001<br>
![huge_sa_exp2.png](assets%2Fhuge_sa_exp2.png)<br>
Harmonogram liniowy, umiarkowane schładzanie, dane wejściowe<br>
init-temp 500, alpha 1, min-temp 0.01<br>
![huge_sa_lin2.png](assets%2Fhuge_sa_lin2.png)<br><br>
Harmonogram wykładniczy, szybkie schładzanie, dane wejściowe<br>
init-temp 200, alpha 0.8, min-temp 0.0001<br>
![huge_sa_exp3.png](assets%2Fhuge_sa_exp3.png)<br>
Harmonogram liniowy, szybkie schładzanie, dane wejściowe<br>
init-temp 200, alpha 2, min-temp 0.01<br>
![huge_sa_lin3.png](assets%2Fhuge_sa_lin3.png)<br>