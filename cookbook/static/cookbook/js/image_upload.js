/* Make image preview when user selects it in a file input. */

document.addEventListener("DOMContentLoaded", () => {
    const image_preview = document.querySelector(".image-preview")
    const image_input = document.querySelector(".image-input")
    const reset_field = document.querySelector(".reset-field")
    
    // Preview image when one is uploaded
    image_input.onchange = e => {
        const [file] = image_input.files
        reset_field.value=""
        
        if (file) {
            image_preview.src = URL.createObjectURL(file)
        }
    }
    
    // Remove image if button clicked
    const remove_btn = document.querySelector(".remove-image-file-btn")
    
    remove_btn.addEventListener("click", e => {
        if (confirm_action("you want to remove your profile picture")) {
            image_input.value = ""
            image_preview.src = "/media/profile/default.svg"
            reset_field.value = "reset"
        }
    })
})

