--- 
title: "Inferring Percentiles for Lognormal Distributions in Reserves Estimation"
date: 2024-11-11T17:28:00
draft: false
description: "A technical deep dive on using SciPy and NumPy to calculate unknown percentile values for probabilistic modeling."
topics: ["python", "statistics", "tutorial"]
---

Calculating a percentile X, based on two other percentiles for a lognormal distribution, sounds familiar❓

That's right, in reserves estimation, when we have any two rough estimates of high / low / medium reserves values, and you need to estimate the unknown one (if you don't have a full probabilistic run at hand of course).

Here is a deep dive on calculating it in #Python using only #scipy and #numpy. Beyond the reserves estimation application itself, it is an interesting topic to understand a bit more about distributions and revisit some university topics 😉

Also, here is the link to the notebook version: https://lnkd.in/esPhRWaX

- psst, you can run it in your browser if you use #codespaces without installing anything, the repo already has the #devcontainer in it.

Have you done this before, and if so, what did you use to calculate the unknown percentile? Let me know in the comments 👇

<object data="attachment.pdf" type="application/pdf" width="100%" height="800px">
    <p>Your browser does not support PDFs. <a href="attachment.pdf">Download the PDF</a> to view it.</p>
</object>

{{< subscription >}}
