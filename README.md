# oc_share_portofolio

:books: Made for an [OpenClassrooms](https://openclassrooms.com) studies project.

This repo aims to solve a problem similar to *0-1 KP*.

Considering two datasets representing multiple *Shares* with respective *Cost* and *Profit* after 2 years, we need to determine wihch portofolio composition would be the most profitable.

Two different approaches are represented:
- `bruteforce.py` creates all possible combinations, in the same way `itertools.combinations` do, and calculates possible profit. At the end of each iteration, this possible profit is compared to the currently highest one.

- `optimized.py` uses a Dynamic Programmation method to compose the portofolio. A matrix is created to calculate, for each share, the potential profit if added at each price in range 0 to total money invested. This potential profit values are compared only with the previously considered shared and added to portofolio if more profitable. This method is again optimized to reduce the multi-dimensional matrix to a 1D array.

You can give a look to these slides for a more in-depth description (french): https://docs.google.com/presentation/d/16OA6zkDQef0wYIhshRBoZkC0HFBbePJbd2dAtguyvR0/edit?usp=sharing
