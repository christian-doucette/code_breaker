# Code Breaker
Code Breaker is live [here](https://code-breaker.azurewebsites.net/)!

&nbsp;  
## Summary
Code Breaker is a Flask web application with encryption functions for ciphers, and automatic decryption functions for some of them. Currently, it includes encryption for:
1. Caesar cipher
2. Substitution cipher
3. Vignere cipher

And, it includes decryption functions for:
1. Caesar cipher
2. Substitution cipher

&nbsp;  
## Decryption Techniques
To decrypt, I use a simple language model called an *n-gram* model. It is trained on common English words, and is able to assign a score to any sequence of letters, which represents how similar that sequence is to standard English.

A Caesar cipher is a rotation of the alphabet, so there are only 26 possibilities for encryption. So, I just check each of these and return the one that my model scores the highest.

A substitution cipher is a permutation of the alphabet, so there are 26! &thickapprox; 4.03 * 10<sup>26</sup> different possible decryptions. So, unlike in the case of the Caesar cipher, I cannot just check each one and return the one with the highest score. To solve this, I implemented the beam search algorithm from the paper ["Beam Search for Solving Substitution Ciphers"](https://www.aclweb.org/anthology/P13-1154.pdf) by Nuhn, Schamper and Ney. It iteratively builds up the solution letter by letter, keeping only the best partial solutions.
