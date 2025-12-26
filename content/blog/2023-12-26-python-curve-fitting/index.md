--- 
title: "Curve Fitting with Python and SciPy: Moving Beyond Excel"
date: 2023-12-26T18:15:00
draft: false
description: "Learn how to use Python's SciPy library for curve fitting and understand the statistical assumptions behind linear regression."
topics: ["python", "scipy", "machine-learning", "tutorial"]
---
![Post Image](thumbnail.jpg)

For engineers, curve fitting is a common task. Instead of relying on Excel, let's use Python to find a function that fits the (x, y) data pairs. It's a great opportunity to start using Python in your daily work!

Here is the repl link: https://replit.com/@oskrgab/curve-fit-python

Did you know that what you're doing right now is actually machine learning? And to keep up with the hype, you're using AI 😜. Nowadays, some terms are abused, and much of what we refer to as AI is simply analytics. In this case, it's a simple linear regression.

The "curve_fit" function in scipy uses least squares to find the coefficients in an unconstrained problem. And there are some assumptions under which the linear regression model is valid:

- Linearity/zero mean
- Constant Variance
- Independence (hard to check)
- Normality

What can you do to check if these assumptions are valid? Can you create some plots? If so, what plots would you create?

(Hint: Calculate the residuals 😉)

{{< youtube cgZ9CISaU-o>}}



{{< subscription >}}
