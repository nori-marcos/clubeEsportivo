document.addEventListener('DOMContentLoaded', function () {
    const flashMessages = document.getElementById('flash-messages');
    const flashContainer = document.getElementById('flash-container');

    if (flashMessages) {
        const successMessage = document.querySelector('.alert-success');
        const errorMessageToInsert = document.querySelector('.alert-danger-insert');
        const errorMessageToEdit = document.querySelector('.alert-danger-edit');
        const errorMessageToDelete = document.querySelector('.alert-danger-remove');

        ajustarClassesMensagens();
        manterAccordionAberto();

        if (errorMessageToInsert) {
            mostrarErroModal('addMemberModal', 'error-container-add', flashMessages.innerHTML);
        }

        if (successMessage || errorMessageToEdit || errorMessageToDelete) {
            $('.modal').modal('hide');
            flashContainer.innerHTML = flashMessages.innerHTML;
        }

        flashMessages.parentNode.removeChild(flashMessages);
    }

    const select = document.getElementById("table-filter");
    const rows = document.querySelectorAll("tbody tr");

    select.addEventListener("keyup", (event) => {
        const value = event.target.value.toLowerCase();
        rows.forEach((row) => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(value) ? "table-row" : "none";
        });
    });

    function ajustarClassesMensagens() {
        document.querySelectorAll('.alert').forEach((alert) => {
            const parts = alert.className.split('-');
            if (parts.length > 2) {
                alert.className = parts.slice(0, 2).join('-') + ' alert-dismissible fade show';
            }
        });
    }

    function manterAccordionAberto() {
        const accordionContent = document.getElementById('collapseOne');
        if (accordionContent) {
            accordionContent.classList.add('show');
        }
    }

    function mostrarErroModal(modalId, containerId, messageHTML) {
        const modal = document.getElementById(modalId);
        const errorContainer = document.getElementById(containerId);
        errorContainer.innerHTML = messageHTML;
        $(modal).modal('show');
    }
});
