---
title: "Modern Stack to Publish a Python Package"
lastmod: 2025-12-23
date: 2025-12-23
draft: false
topics: ["python"]
summary: ""
---

The python package ecosystem has changed a lot since the last time I attempted to 
create a Python package.

I put myself the challenge for the past couple of weeks to publish a python package 
with some simple domain-knowledge functionality, in this case, relative permeabilities 
and capillary pressures in the context of the O&G industry.

The purpose of this exercise is to go having nothing, to create a full project that can 
be published to PyPI, using a modern tech stack, CI/CD and testing. I want this to 
serve as a blueprint for future packages that I can built or to help somebody else in 
the same boat as me.

## Setting up the project using uv.

Before Astral came along with all the suite of python tooling, there were many options 
available to manage your python project (poetry, pdm, pip, setuptools, etc). 

Now, everything is more straightforward, since you just know you have to use **uv**.

