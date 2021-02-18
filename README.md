## Fuzzy Battle Royale

A Python based pong-styled game with fuzzy logics players.

Main goal of this project is to find out which of four most popular fuzzy logics algorithms is best in the pong game: Mamdani, Sugeno, Tsukamoto or Larsen.

![Game field](http://www.mandysam.com/img/random.jpg)

All four algorithms are implemented from scratch and set up identically.

May the Best Win!

_____

Requirements:

1. Python 3

   ```bash
   sudo apt install python3.8
   ```

2. Scipy package

   ```bash
   pip install scipy
   ```

3. Tkinter package

   ```bash
   sudo apt-get install python3-tk
   ```

How to run:

```bash
python3.8 FuzzyBattleRoyale.py
```

_____
<details>
  <summary>Spoiler alert! (Huge test results)</summary>
  After handling 500 games to -10 score, the winner has arrived - Sugeno algorithm. Mamdani is 2nd, Larsen and Tsukamoto are 3rd and 4th.
   <blockquote class="spoiler">
     <img alt="Hidden game field" src="http://www.mandysam.com/img/random.jpg"/>
   </blockquote>
</details>
