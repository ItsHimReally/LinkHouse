<?php
include('php/db.php');
$link = connectDB();
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
	<div class="page pg-center">
		<div class="titleFlex">
			<div class="title large">LinkHouse</div>
			<div class="stitle">Единый профиль клиента через устранение дубликатов</div>
		</div>
		<div class="pc-content">
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
			<span class="comment">Может занять некоторое время.<br>Создано для демонстрации. Более точный результат при запуске скриптов локально.</span>
		</div>
	</div>
</div>
</html>