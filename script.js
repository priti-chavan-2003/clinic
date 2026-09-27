document.addEventListener(
    "DOMContentLoaded",
    function () {

        // Automatically hide flash messages
        setTimeout(
            function () {

                const alerts =
                    document.querySelectorAll(
                        ".alert"
                    );

                alerts.forEach(
                    function (alert) {

                        try {

                            const bsAlert =
                                bootstrap.Alert.getOrCreateInstance(
                                    alert
                                );

                            bsAlert.close();

                        } catch (error) {

                            alert.style.display =
                                "none";

                        }

                    }
                );

            },
            4000
        );


        // Set minimum appointment date to today

        const dateInputs =
            document.querySelectorAll(
                'input[type="date"]'
            );


        const today =
            new Date()
                .toISOString()
                .split("T")[0];


        dateInputs.forEach(
            function (input) {

                input.min = today;

            }
        );


        // Confirm dangerous actions

        const deleteForms =
            document.querySelectorAll(
                ".delete-form"
            );


        deleteForms.forEach(
            function (form) {

                form.addEventListener(
                    "submit",
                    function (event) {

                        const confirmed =
                            confirm(
                                "Are you sure you want to continue?"
                            );

                        if (!confirmed) {

                            event.preventDefault();

                        }

                    }
                );

            }
        );

    }
);
