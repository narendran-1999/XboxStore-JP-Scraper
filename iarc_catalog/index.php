<!DOCTYPE html>
<html>
<head>
    <title>Game Catalog (IARC)</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        /* Custom CSS styles */
        .game-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            grid-gap: 20px;
            margin-top: 20px;
        }

        .game-tile {
            background-color: #fff;
            border: 1px solid #e4e4e4;
            padding: 20px;
            text-align: center;
            transition: background-color 0.2s;
        }

        .game-tile:hover {
            background-color: #ddd;
        }

        .game-tile a {
            text-decoration: none;
            color: inherit;
        }

        .game-tile img {
            max-width: 100%;
            height: auto;
        }

        .game-title {
            font-size: 18px;
            font-weight: bold;
            margin: 10px 0;
        }

        .back-to-top {
            display: none;
            position: fixed;
            bottom: 20px;
            right: 20px;
            color: #fff;
            padding: 10px;
            border-radius: 5px;
            cursor: pointer;
        }

        .btn-group{
            background-color:#050;
            border-radius: 5px;
            padding: 3px;
        }

        .right-grp{
            text-align:right;
        }
    </style>
</head>
<body>

<div class="container">
    <div class="row">
        <div id="ageFilter" class="btn-group">
                <button class="btn btn-success mr-1" data-filter="all">All</button>
                <button class="btn btn-success mr-1" data-filter="12">12+</button>
                <button class="btn btn-success mr-1" data-filter="16">16+</button>
                <button class="btn btn-success" data-filter="18">18+</button>
        </div>
    </div>
</div>

<div class="back-to-top" onclick="scrollToTop()"><img src="./to-top-64.png"></div>

<div class="container">
    <div class="game-grid">
        <?php
        // Open the CSV file
        $csvFile = fopen('catalog_bkp.csv', 'r');
        $firstRow = true; // Flag to ignore the first row

        if ($csvFile !== false) {
            // Loop through the CSV rows
            while (($row = fgetcsv($csvFile)) !== false) {
                // Check if it's the first row (header) and skip it
                if ($firstRow) {
                    $firstRow = false;
                    continue;
                }

                list($gameTitle, $boxartURL, $gamePageURL, $ageRating) = $row;
        ?>
                <div class="game-tile" data-age="<?php echo $ageRating; ?>">
                    <a href="<?php echo $gamePageURL; ?>">
                        <img src="<?php echo $boxartURL; ?>" alt="<?php echo $gameTitle; ?>">
                        <div class="game-title"><?php echo $gameTitle; ?></div>
                        <div class="age-rating"><?php echo $ageRating; ?>+</div>
                    </a>
                </div>
        <?php
            }
            // Close the CSV file
            fclose($csvFile);
        } else {
            echo 'Failed to open CSV file.';
        }
        ?>
    </div>
</div>

<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.3/dist/umd/popper.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
<script>
    // JavaScript function for filtering game tiles based on age ratings
    document.addEventListener('DOMContentLoaded', function() {
        const ageFilter = document.getElementById('ageFilter');
        const gameTiles = document.querySelectorAll('.game-tile');

        ageFilter.addEventListener('click', function(event) {
            const filterValue = event.target.getAttribute('data-filter');
            if (filterValue === 'all') {
                gameTiles.forEach(tile => tile.style.display = 'block');
            } else {
                gameTiles.forEach(tile => {
                    const tileAge = tile.getAttribute('data-age');
                    tile.style.display = tileAge === filterValue ? 'block' : 'none';
                });
            }
        });
    });
</script>
<script>
    // Show or hide the "Back to Top" button based on scroll position
    window.onscroll = function() {
        toggleBackToTopButton();
    };

    function toggleBackToTopButton() {
        var button = document.getElementsByClassName('back-to-top')[0];
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            button.style.display = 'block';
        } else {
            button.style.display = 'none';
        }
    }

    // Scroll to the top when the button is clicked
    function scrollToTop() {
        document.body.scrollTop = 0;
        document.documentElement.scrollTop = 0;
    }
</script>
</body>
</html>
