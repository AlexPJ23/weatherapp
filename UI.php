<!DOCTYPE html>
<html>
<head>
    <title>The Weather App</title>
    <style>
        h1 {text-align: center;}
        p {text-align: center;}
    </style>
</head>
<body>
    <h1>Alex Joseph-Weather App</h1>
    <form method="POST">
        <label for="states">Please choose the state you are currently living in:</label>
        <select id="states" name="states" onchange="this.form.submit()">
            <option value="NY">New York</option>
            <option value="CA">California</option>
            <option value="IL">Illinois</option>
            <option value="AZ">Arizona</option>
            <option value="TX">Texas</option>
            <option value="PA">Pennsylvania</option>
            <option value="FL">Florida</option>
        </select>
    </form>

    <?php
    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $state = $_POST["states"];
        echo "<h2>Weather in " . $state . "</h2>";
        $cnx = new mysqli('localhost', 'root', '', 'weather');
        if ($cnx->connect_error) {
            die('Connection failed: '. $cnx->connect_error);
        }

        $query = "SELECT * FROM " . $state . "_T";
        $cursor = $cnx->query($query);
        echo "<table>";
        echo "<tr><th>Date</th><th>Temperature</th><th>Description</th><th>Even Longer Description</tr>";
        while ($row = $cursor->fetch_assoc()) {
            echo '<tr>';
            echo '<td>' . $row['date'] . '</td><td>' . $row['temp'] . '</td><td>' . $row['short_desc'] .'</td><td>'.$row['long_desc'].'</td>';
            echo '</tr>';
        }
        echo "</table>";
        $cnx->close();
    } else {
        echo "<p>Please select a state to see the weather</p>";
    }
    ?>
</body>
</html>