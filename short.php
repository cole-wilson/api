<?php
header("Content-Type: text/plain");
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST');
header("Access-Control-Allow-Headers: X-Requested-With");

if ($_GET[''] == $_ENV['SHORTY_TOKEN']) {
   $url = "https://srv-captain--shorty/api/link";
   $curl = curl_init($url);
   curl_setopt($curl, CURLOPT_URL, $url);
   curl_setopt($curl, CURLOPT_POST, true);
   curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
   $headers = array(
      "Accept: application/json",
      "Content-Type: application/json",
   );
   curl_setopt($curl, CURLOPT_HTTPHEADER, $headers);

$data = <<<DATA
{
  "Id": 78912,
  "Customer": "Jason Sweet",
  "Quantity": 1,
  "Price": 18.00
}
DATA;

   curl_setopt($curl, CURLOPT_POSTFIELDS, $data);
   $resp = curl_exec($curl);
   curl_close($curl);
   echo $resp;
}
else {
  echo "403";
}
