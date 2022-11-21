<?php
// If POST call made then validate input
if ($_POST["name"] || $_POST["pass"]) {
    // Display the input Data
    echo "Welcome " . $_POST["name"] . "<br />";
    echo "Password " . $_POST['pass'] . "";
    exit();
}
?>
<html>
<!-- Get sample input data of username password -->

<body>

    <form action="<?php echo $_PHP_SELF ?>" method="POST">
        Username: <input type="text" name="name" />
        Password: <input type="password" name="pass" />
        <input type="submit" />
    </form>

</body>

</html>