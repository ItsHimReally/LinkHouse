<?php
include('php/db.php');
include('php/api.php');
$link = connectDB();

if (!isset($_GET["uid"], $_GET["table"])) {
    header("Location: /");
    exit();
}

$data = callApi("https://iih.tw1.su/api/search?uid=".urlencode($_GET["uid"])."&table=".urlencode($_GET["table"]));
$comparison = []; $title = null;
foreach ($data as $row) {
    $tableNumber = $row['table_number'];
    $fieldName = $row['field_name'];
    $fieldValue = $row['field_value'];
    $comparison[$fieldName]['table_' . $tableNumber] = $fieldValue;
    if ($fieldName === 'full_name' && empty($title)) {
        $title = $fieldValue;
    }
}
$table_columns = [];
foreach ($data as $row) {
    $table_columns[] = $row['table_number'];
}
$table_columns = array_unique($table_columns);
sort($table_columns);
?>
<html>
<head>
    <title>LinkHouse</title>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="css/style.css" media="all">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="Description" content="LinkHouse">
    <meta http-equiv="Content-language" content="ru-RU">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700;900&family=Roboto&display=swap" rel="stylesheet">
</head>
<div class="wrapper">
    <?php
    include ('php/side.php');
    ?>
    <div class="page sear">
        <div class="titleFlex">
            <div class="title"><?php echo $title ?? "LinkHouse"; ?></div>
        </div>
        <div class="pg-content">
            <form class="search" method="GET" action="search.php">
                <label>
                    <input type="text" name="q" placeholder="Найдется все...">
                </label>
	            <a href="random.php">
		            <img src="images/shuffle.svg" alt="Рандом">
	            </a>
                <button>
                    <img src="images/search.svg" alt="Найти">
                </button>
            </form>
            <div class="sResult">
	            <?php
                echo '<table border="1">';
                echo '<tr><th>Колонки</th>';
                foreach ($table_columns as $column) {
                    echo "<th>table_dataset$column</th>";
                }
                echo '</tr>';

                foreach ($comparison as $fieldName => $tables) {
                    echo '<tr>';
                    echo '<td>' . $fieldName . '</td>';
                    foreach ($table_columns as $column) {
                        echo '<td>' . (isset($tables['table_' . $column]) ? $tables['table_' . $column] : '') . '</td>';
                    }
                    echo '</tr>';
                }

                echo '</table>';
	            ?>
            </div>
        </div>
    </div>
</div>
<script>
    function toggle(el) {
        el.style.display = (el.style.display == 'block') ? '' : 'block'
    }
    document.getElementById('fileInput').addEventListener('change', function() {
        if (this.files.length > 0) {
            document.getElementById('uploadForm').submit();
        }
    });
</script>
</html>