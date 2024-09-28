<?php
include('php/db.php');
include('php/api.php');
$link = connectDB();

if (!isset($_GET["q"])) {
	header("Location: /");
	exit();
}
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
            <div class="title">Поиск</div>
        </div>
        <div class="pg-content">
            <form class="search" method="GET" action="">
                <label>
                    <input type="text" name="q" value="<?=htmlspecialchars($_GET["q"])?>" placeholder="Найдется все...">
                </label>
	            <a href="random.php">
		            <img src="images/shuffle.svg" alt="Рандом">
	            </a>
                <button>
                    <img src="images/search.svg" alt="Найти">
                </button>
            </form>
	        <div class="result">
		        <?php
            if (strlen($_GET["q"]) < 3) {
                echo "<span class='error'>Строка не содержит как минимум три символа.</span>";
				exit();
            }
            $initialApiUrl = "https://iih.tw1.su/api/search?q=".urlencode(mb_strtoupper($_GET["q"]));
            $data = callApi($initialApiUrl);
            if ($data === null) {
                echo "<span class='error'>Ошибка при запросе к API или статус ответа не 200.</span>";
            } else {
                foreach ($data as $a) {
                            echo '<div class="block">    
		<span class="s_title">'.$a['field_value'].'</span>
		<a href="https://iih.tw1.su/profile.php?uid='.$a["uid"].'&table='.$a["table_number"].'">
			Открыть
		</a>
</div>';
                }
            }
		?>
	        </div>
        </div>
    </div>
</div>
</html>