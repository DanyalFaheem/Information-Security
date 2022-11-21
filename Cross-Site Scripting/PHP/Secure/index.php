<?php
// If POST call made then validate input
if ($_POST["name"] || $_POST["pass"]) {
    // Trim to remove whitespaces
    $username = trim($_POST['name']);
    $password = trim($_POST['pass']);
    // Look for script tag in username
    if (strpos($username, "<script>") !== false || strpos($username, "<\script>") !== false ) {
        echo "Script tag found in the username input, please try again";
    }
    // Look for password tag in username
    elseif (strpos($password, "<script>") !== false || strpos($password, "<\script>") !== false ) {
        echo "Script tag found in the password input, please try again";
    }
    // Sanitize input for any HTML tag and store in database
    else {
        // Sanitize input nonetheless
        $username = strip_tags($username);
        $password = strip_tags($password);
        // Display the input Data
        echo "Welcome " . $username . "<br />";
        echo "Password " . $_POST['pass'] . "";
    }

    exit();
}
?>
<html>
<!-- Get sample input data of username password -->
<body>

    <form action="<?php echo $_PHP_SELF ?>" method="POST">
        Username: <input type="text" name="name" />
        Password: <input type="text" name="pass" />
        <input type="submit" />
    </form>

</body>

</html>

