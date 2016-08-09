# My Cookbook Recipes

A generic REST API for highly-structured recipes designed specifically for VUI (voice user interface).

### Components & Design

There is an AWS API Gateway instance which forwards HTTP requests to the lambda functions included in this repository. The folder structure matches the URL structure, with the most common endpoints being `/recipes` and `/search`. The get http methods are in the get folder, and the same with post.

API documentation will be generated with swagger, although currently I can't figure out how to do it.
