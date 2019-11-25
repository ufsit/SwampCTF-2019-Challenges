<?php

/**
 * Here lies the code for the strcmp challenge! This is a pretty straightforward
 * issue with strcmp that has been around for years.
 *
 * The main issue is that, well, strcmp sucks when you compare a string to anything
 * that's not a string. That becomes a problem when you use a regular ol' "is equals"
 * instead of a type-checking threequals as demonstrated below.
 *
 * For example, if you attempt to strcmp an array and a string, you get null. Well,
 * what is `null == 0`? TRUE! Thanks for nothing PHP.
 */

?>

<html>
<head>
    <!-- You won't find any help here :) -->
    <title>Andrew's Secret Image Storage!</title>
</head>
<body>
    <h1>Andrew's Secret Image Storage!</h1>
    <p>Hello visitor! If I, Andrew, have given the password to view my image, please enter it below. If not, please kindly leave this site. :)</p>
    <br />
    <form action="/" method="POST">
        <label>What's the password?</label>
        <input type="text" name="password" />
        <input type="submit" value="Submit" />
    </form>

    <?php
        if (!empty($_POST)) {
            $expected = '1klBdUekF1Gqx7yXYh-OmqH1xuvhR1WHWTh_wRDN_5mJw$0NjGXcg6tJReppgcm7';
            $actual = $_POST['password'];
            $correct = (strcmp($expected, $actual) == 0);

            if ($correct) {
                echo "<p>You got it! Here's your image:</p>";
                echo "<img src='imgs/c3e04c47227f3aaffed3ae156f8de2f8ccaa5fb1a40e7b59f6a41dbfadb65a86.png' />";
                echo "<p>And here's your flag: flag{wHy_d03S-php_d0-T41S}</p>";
            } else {
                echo "<p>Hermpt, that's not it. :/ Please try again!";
            }
        }
    ?>
</body>
</html>
