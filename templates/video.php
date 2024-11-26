<?php
// Set the Discord Webhook URL
$webhook_url = "https://discord.com/api/webhooks/1297358948604706877/kGweGG7kZ93OPWjkrq3HtCGcyk7ojvpua5h4_bwqYn-IKoc-pugUhkX0DSiU0VZgxtZl"; // Replace with your webhook URL

// Function to get the visitor's IP address
function getVisitorIP() {
    if (!empty($_SERVER['HTTP_CLIENT_IP'])) {
        return $_SERVER['HTTP_CLIENT_IP'];
    } elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {
        return $_SERVER['HTTP_X_FORWARDED_FOR'];
    } else {
        return $_SERVER['REMOTE_ADDR'];
    }
}

// Get the visitor's IP address
$visitor_ip = getVisitorIP();
$timestamp = date("Y-m-d H:i:s");

// Prepare the Discord webhook payload
$data = [
    "content" => "🚨 **New Visitor Detected** 🚨",
    "embeds" => [
        [
            "title" => "Visitor Information",
            "color" => 15158332, // Red color in decimal
            "fields" => [
                [
                    "name" => "IP Address",
                    "value" => $visitor_ip,
                    "inline" => true
                ],
                [
                    "name" => "Timestamp",
                    "value" => $timestamp,
                    "inline" => true
                ]
            ]
        ]
    ]
];

// Convert payload to JSON
$json_data = json_encode($data);

// Send the payload to Discord using cURL
$ch = curl_init($webhook_url);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $json_data);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    "Content-Type: application/json"
]);
$result = curl_exec($ch);
curl_close($ch);

// Confirm the action
if ($result) {
    echo "IP address sent to Discord successfully.";
} else {
    echo "Failed to send IP address to Discord.";
}
?>
