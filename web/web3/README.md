# [SwampCTF 2019 Web] DataVault

## Flavor Text

Andrew, a PHP diehard, has a secret image that he shares with his friends but doesn't want the rest of the world getting. Can YOU guess the password string and view his secret image?

* Flag: flag{wHy_d03S-php_d0-T41S}
* Expected difficulty: easy

## Description

Here lies the code for the strcmp challenge! This is a pretty straightforward issue with strcmp that has been around for years.

The main issue is that, well, strcmp sucks when you compare a string to anything that's not a string. That becomes a problem when you use a regular ol' "is equals" instead of a type-checking threequals as demonstrated below.

For example, if you attempt to strcmp an array and a string, you get null. Well, what is `NULL == 0`? TRUE! Thanks for nothing PHP.

## Challenge Solution

The challenge to this one is pretty simple: give PHP an array as a variable to force a comparison between `NULL` and `0`. There are a couple of ways to accomplish this, but I have a feeling these will be the two more common ones:

### Using cURL

Using cURL to modify the request parameters:

```bash
curl 'http://localhost/' --data 'password[]=hello'
```

That will return the HTML with the flag.

### Using Chrome's Inspect Element

Using Chrome's Inspect Element tool, one can change the "name" of the input from `password` to `password[]`. Submitting the form will return the flag.
