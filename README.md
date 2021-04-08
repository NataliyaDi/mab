# mab
Reinfocement learning. Kernel for MAB model

If we want to find optimal sorting of items, multi-arms bandit approach can be used. 
We can sort items by different ways: by price, by sale, by popularity or reviews. In my term these ways are strategies (arms).

I use Beta distribution to sample probability for each arm. We initialize params (alpa, beta) with 1, then update them according to user reward. If user interact more with the first arm, we increase alpha param for the first arm, so next time this arm would be shown frequently then others.

In [mab.py](https://github.com/NataliyaDi/mab/blob/main/mab.py) the  realisation of this approach can be found. We can add descriptions for arm, add/remove arms, get reward, update distribution etc.

Examples of using mab.py are in [how_to_use_mab.ipynb](https://github.com/NataliyaDi/mab/blob/main/how_to_use_mab.ipynb). 
