document.addEventListener('DOMContentLoaded', function () {
    var flashMessages = document.getElementById('flash-messages');
    if (flashMessages) {
        var successMessage = document.querySelector('.alert-success');
        var errorMessageToInsert = document.querySelector('.alert-danger-insert');
        var errorMessageToEdit = document.querySelector('.alert-danger-edit');
        var errorMessageToDelete = document.querySelector('.alert-danger-remove');
        var flashContainer = document.getElementById('flash-container');

        function ajustarClassesMensagens() {
            var alerts = document.querySelectorAll('.alert');
            alerts.forEach(function (alert) {
                var originalClass = alert.className;
                var parts = originalClass.split('-');
                if (parts.length > 2) {
                    var newClass = parts.slice(0, 2).join('-'); // Mantém apenas até o segundo traço
                    alert.className = newClass + ' alert-dismissible fade show';
                }
            });
        }

        function manterAccordionAberto() {
            var accordionContent = document.getElementById('collapseOne');
            if (accordionContent) {
                accordionContent.classList.add('show');
            }
        }

        if (errorMessageToInsert) {
            var errorInsertModal = document.getElementById('addMemberModal');
            var errorContainerAdd = document.getElementById('error-container-add');
            errorContainerAdd.innerHTML = flashMessages.innerHTML;
            $(errorInsertModal).modal('show');
            ajustarClassesMensagens();
            manterAccordionAberto();
        }

        if (successMessage) {
            $('.modal').modal('hide');
            flashContainer.innerHTML = flashMessages.innerHTML;
            ajustarClassesMensagens();
            manterAccordionAberto();
        }

        if (errorMessageToEdit) {
            $('.modal').modal('hide');
            flashContainer.innerHTML = flashMessages.innerHTML;
            ajustarClassesMensagens();
            manterAccordionAberto();
        }

        if (errorMessageToDelete) {
            flashContainer.innerHTML = flashMessages.innerHTML;
            ajustarClassesMensagens();
            manterAccordionAberto();
        }

        flashMessages.parentNode.removeChild(flashMessages);
    }
});