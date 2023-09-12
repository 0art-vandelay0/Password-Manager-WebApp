document.addEventListener("DOMContentLoaded", function() {
    var twoFactorType = document.getElementsByName("two_factor_type")[0];
    var questionField = document.getElementsByName("question")[0].parentNode.parentNode;
    var answerField = document.getElementsByName("answer")[0].parentNode.parentNode;
    var authenticationField = document.getElementsByName("authentication")[0].parentNode.parentNode;

    function toggleFields() {
        if (twoFactorType.value === "question") {
            questionField.style.display = "table-row";
            answerField.style.display = "table-row";
            authenticationField.style.display = "none";
        } else if (twoFactorType.value === "authentication") {
            questionField.style.display = "none";
            answerField.style.display = "none";
            authenticationField.style.display = "table-row";
        }
    }

    twoFactorType.addEventListener("change", toggleFields);
    toggleFields();
});
