// document.addEventListener("DOMContentLoaded", () => {
//     const tabs = document.querySelectorAll(".tab");

//     // Switch between "Today" and "Week" tabs
//     tabs.forEach((tab) => {
//         tab.addEventListener("click", () => {
//             tabs.forEach((t) => t.classList.remove("active"));
//             tab.classList.add("active");
//         });
//     });
// });

function submitForm() {
    const form = document.getElementById('temperature-form');
    form.submit();
}

