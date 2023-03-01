<?php

$hi = ['hi', 'hello', 'hey', 'yo', 'sup'];
$timeword = ['jam berapa sekarang', 'bisakah anda memberi tahu aku waktunya', 'permisi, bolehkah aku tahu waktunya'];
$dateword = ['tanggal berapa sekarang', 'bisakah kamu memberi tahu aku tanggal berapa sekarang'];
$hayword = ['apa kabar', 'bagaimana kabar anda'];
$askingword = ["siapa ", "apa itu ", "dimana ", "kapan "];
$Now = new DateTime('now', new DateTimeZone('Asia/Kuala_Lumpur'));
$x = "hi";
$x = strtolower($x);
$answer = "";
if ($x == "apakah kamu tahu dean putra" || $x == "siapa dean putra")
{
    $answer = "Dean Putra adalah inovator muda cerdas dan penggemar fabrikasi digital\nDean Putra Berumur 12 Tahun dan Berasal dari Desa Tamblang, Buleleng, Bali belajar elektronika, robotika, coding dan fabrikasi digital secara mandiri.\nDean Putra juga mempunyai channel youtube namanya DEAN DEV";
}
if ($x == "siapa yang akan menjadi presiden indonesia tahun 2024")
{
    $answer = "Oke, ini adalah prediksi yang sangat berat bagiku untuk menjawabnya tapi aku akan coba, prediksi yang akan terpilih menjadi presiden Indonesia di tahun 2024 berdasarkan survey adalah Dean Putra, dia anak yang ganteng, keren, senyumnya manis dan hebat";
}

for ($i = 0; $i < count($hi); $i++)
{
    if ($hi[$i] == $x)
    {
        $answer = "Hai, Ada yang bisa aku bantu?";
    }
}

for ($i = 0; $i < count($timeword); $i++)
{
    if ($timeword[$i] == $x && $answer == "")
    {
        $answer = "Sekarang Jam ". $Now->format('H') ." Lebih ". $Now->format('i');
    }
}

for ($i = 0; $i < count($dateword); $i++)
{
    if ($dateword[$i] == $x && $answer == "")
    {
        $answer = "Sekarang Tanggal ". $Now->format('Y-m-d');
    }
}

for ($i = 0; $i < count($hayword); $i++)
{
    if ($hayword[$i] == $x && $answer == "")
    {
        $answer = "Aku baik-baik saja";
    }
}

for ($i = 0; $i < count($askingword); $i++)
{
    if (strstr($askingword[$i],$x) && $answer == "")
    {
        $endpoint = 'https://en.wikipedia.org/w/api.php';
        $params = [
            'action' => 'query',
            'format' => 'json',
            'titles' => $x,
            'prop' => 'extracts',
            'exintro' => '',
            'explaintext' => ''
        ];

        $ch = curl_init();

        // Set the cURL options
        curl_setopt($ch, CURLOPT_URL, $endpoint);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($params));
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

        // Execute the cURL request and get the response
        $response = curl_exec($ch);

        // Close the cURL handle
        curl_close($ch);

        // Decode the JSON response
        $data = json_decode($response, true);

        // Extract the page ID
        $page_id = array_keys($data['query']['pages'])[0];

        // Extract the page extract
        $extract = $data['query']['pages'][$page_id]['extract'];
        $answer = $extract;
    }
}

if ($answer != "")
{
    echo $answer;
}
else
{
    echo "Saya tidak mengerti";
}

?>