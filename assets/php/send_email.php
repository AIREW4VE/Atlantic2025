<?php
  if(!isset($_POST['submit']))
{
  //This page shouldn't accessed directly
  echo " Error Please Submit the message";
}
//Get inputs
  $name = $_POST['name'];
  $visitor_email = $_POST['email'];
  $message = $_POST['message'];

//Validate 
if(empty($name)||empty($visitor_email))
{
  echo "Name and email are Mandatory";
  exit;
}


	$email_from = "jake.still@live.co.uk";

	$email_subject = "Aire Wave Website response";

	$email_body = "You have received a new message from the user $name.\n".
                            "email address is $visitor_email.\n".
                            "Here is the message:\n $message".

  $to = "jake.still@live.co.uk";

  $headers = "From: $email_from \r\n";

  $headers .= "Reply-To: $visitor_email \r\n";




  function isInjected($str) {
    $inject = "/(\r|\t|%0A|%0D|%08|%09)+/i";
    return (preg_match($inject, $str) > 0);
}

if(IsInjected($visitor_email))
{
    echo "Bad email value!";
    exit;
}


mail($to,$email_subject,$email_body,$headers);
?>