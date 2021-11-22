<?php
header("Content-Type: text/plain");
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST');
header("Access-Control-Allow-Headers: X-Requested-With");

if ($_GET['token'] == $_ENV['SHORTY_TOKEN']) {
   $url = "https://srv-captain--shorty/api/link";
   $curl = curl_init($url);
   curl_setopt($curl, CURLOPT_URL, $url);
   curl_setopt($curl, CURLOPT_POST, true);
   curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
   $headers = array(
      "Accept: application/json",
      "Content-Type: application/json",
      "Authorization: Bearer ".$_ENV["SHORTY_TOKEN"]
   );
   curl_setopt($curl, CURLOPT_HTTPHEADER, $headers);

$data = '{"url": "'.$_GET['url'].'"}';

   curl_setopt($curl, CURLOPT_POSTFIELDS, $data);
   $resp = curl_exec($curl);
   curl_close($curl);
   $json = json_decode($result, true);
   echo $resp;
}
else {
   header('HTTP/1.0 403 Forbidden');
   echo "403 forbidden";
}
