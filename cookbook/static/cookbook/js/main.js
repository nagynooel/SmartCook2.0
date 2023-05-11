window.addEventListener("load", () => {
    // Initialize bootstrap 5 tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
})

// Ask user to confirm action ("Are you sure?")
function confirm_action(action="") {
    let answer = confirm(`Are you sure${action=="" ? '' : ' '}${action}?`)
    return answer
}