<?php
include('php/api.php');
$data = callApi("https://iih.tw1.su/api/random");
header("Location: /profile.php?uid=".urlencode($data["uid"])."&table=".urlencode($data["table"]));
exit();