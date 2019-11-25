<?php
/**
 * This challenge is another PHP trick; parse_url treats special URLs differently than cURL.
 */
session_start();

if (empty($_SESSION['links'])) {
    $_SESSION['links'] = [];
}

?>

<html>
<head>
    <title>Link Fetcher</title>
</head>
<body>
    <h1>The Link Fetcher</h1>
    <p>Want to remember cool links? This link fetcher will fetch links and store them for you!</p>
    <form action="/" method="POST">
        <input type="text" name="link" />
        <input type="submit" />
    </form>

    <?php
        /**
         * Expected Opengraph tags.
         * @var array The expected Opengraph tags.
         */
        const OPENGRAPH_TAGS = [
            'og:url' => 'url',
            'og:title' => 'title',
            'og:description' => 'description',
        ];

        /**
         * The hosts for 'localhost'.
         * @var array The hosts for 'localhost'.
         */
        const LOCALHOST_HOSTS = [
            'localhost',
            '127.0.0.1',
            // Other? TODO: Add the internal IP that Docker gives this container in Prod.
            // Other? TODO: Add URL for this challenge :joy:.
        ];

        /**
         * Gets the content returned from a URL.
         *
         * @param string $url The URL to fetch.
         *
         * @return string The content returned from a URL.
         */
        function get_data(string $url): string
        {
            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, $url);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
            curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 1); // Timeout after one second.
            $content = curl_exec($ch);
            curl_close($ch);
            return $content;
        }

        /**
         * Gets the Opengraph information from a blob of HTML.
         *
         * @param string $content The HTML content.
         *
         * @return array The Opengraph data; namely the title & description.
         */
        function opengraph_data(string $content): array
        {
            $doc = new DomDocument();
            $doc->loadHTML($content);
            $xpath = new DOMXPath($doc);
            $query = '//*/meta[starts-with(@property, \'og:\')]';
            $metas = $xpath->query($query);
            $rmetas = array();
            foreach ($metas as $meta) {
                $property = $meta->getAttribute('property');

                // Check if we care about the property or not.
                if (!isset(OPENGRAPH_TAGS[$property])) {
                    continue;
                }

                $content = $meta->getAttribute('content');
                $rmetas[OPENGRAPH_TAGS[$property]] = $content;
            }

            return $rmetas;
        }

        /**
         * Processes a new link and returns a formatted array to add to the session's links.
         *
         * @param string $link The link to process.
         *
         * @return array The data to add to the session's links array.
         */
        function process_link(string $link): array
        {
            $link_content = get_data($link);

            // If the link content is empty, just return the standard array.
            if (empty($link_content)) {
                return [
                    'url' => $link,
                    'title' => '',
                    'description' => '',
                ];
            }

            // lol, lots of warnings returned here. Just... don't output the errors.
            $og_data = @opengraph_data($link_content);

            // Return the Opengraph data (if available).
            $return_array = [
                'url' => $og_data['url'] ?? $link,
                'title' => $og_data['title'] ?? '',
                'description' => $og_data['description'] ?? '',
            ];

            return $return_array;
        }

        /**
         * Does a string contain a the needle string?
         *
         * @param string $needle The needle
         * @param string $haystack The haystack in which to find the needle in
         *
         * @return bool Does the haystack contain the needle?
         */
        function string_contains(string $needle, string $haystack): bool
        {
            return (strpos($haystack, $needle) !== false);
        }

        // Script start!
        $links = $_SESSION['links'];
        if ($_POST) {
            $link = $_POST['link'];

            // Check if we have a valid link. If we do, add it!
            if (
                !is_string($link) ||
                !($url_parts = parse_url($link)) ||
                empty($url_parts['scheme']) ||
                empty($url_parts['host'])
            ) {
                echo "<p>Ruh roh, this doesn't look like a valid link!</p>";
                // Check for "internal" URLs.
            } elseif (string_contains('localhost', $url_parts['host']) || string_contains('127.0.0.1', $url_parts['host'])) {
                echo "<p>Ruh roh, we don't allow you to fetch internal URLs!";
                // Here is the challenge magic :)
            } elseif (
                !empty($url_parts['fragment']) &&
                string_contains('@', $url_parts['fragment']) && (
                string_contains('localhost/key', $url_parts['fragment']) ||
                string_contains('127.0.0.1/key', $url_parts['fragment']))
            ) {
                $_SESSION['links'][] = [
                    'url' => $link,
                    'title' => 'The flag!',
                    'description' => 'flag{y0u_cANn0t_TRU5t_php}',
                ];
                echo "<p>Link added!</p>";
            } else {
                $_SESSION['links'][] = process_link($link);
                echo "<p>Link added!</p>";
            }
        }

        foreach ($_SESSION['links'] as $link) {
            echo "<p>Link: " . htmlentities($link['url']) . "</p>";
            echo "<p>Title: " . htmlentities($link['title']) . "</p>";
            echo "<p>Description: " . htmlentities($link['description']) . "</p>";
            echo "<hr />";
        }
    ?>
</body>
</html>
