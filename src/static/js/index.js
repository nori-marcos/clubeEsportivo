document.getElementById('btn-clear').addEventListener('click', function () {
    const modal = document.getElementById('addMemberModal');
    const errorContainer = modal.querySelector('#error-container-add');
    errorContainer.innerHTML = '';
    document.querySelectorAll('.form-control').forEach(input => input.value = '');
});

document.addEventListener('DOMContentLoaded', function () {
    const flashMessages = document.getElementById('flash-messages');
    const flashContainer = document.getElementById('flash-container');

    if (flashMessages) {
        const successMessage = document.querySelector('.alert-success');
        const errorMessageToInsert = document.querySelector('.alert-danger-insert');
        const errorMessageToEdit = document.querySelector('.alert-danger-edit');
        const errorMessageToDelete = document.querySelector('.alert-danger-remove');

        if (errorMessageToInsert) {
            const cpf = errorMessageToInsert.getAttribute('data-cpf');
            const nome = errorMessageToInsert.getAttribute('data-nome');
            const dataNascimento = errorMessageToInsert.getAttribute('data-data_nascimento');
            const tipo = errorMessageToInsert.getAttribute('data-tipo');
            const endereco = errorMessageToInsert.getAttribute('data-endereco');
            const telefone = errorMessageToInsert.getAttribute('data-telefone');
            const email = errorMessageToInsert.getAttribute('data-email');
            const plano = errorMessageToInsert.getAttribute('data-plano');
            console.log(cpf, nome, dataNascimento, tipo, endereco, telefone, email, plano);
            preencherFormulario(cpf, nome, dataNascimento, tipo, endereco, telefone, email, plano);
            mostrarErroModal('addMemberModal', 'error-container-add', flashMessages.innerHTML);
            ajustarClassesMensagens();
            manterAccordionAberto();
        }

        if (errorMessageToEdit) {
            const id = errorMessageToEdit.getAttribute('data-id');
            const nomeModal = `editMemberModal${id}`;
            mostrarErroModal(nomeModal, 'error-container-edit', flashMessages.innerHTML);
            ajustarClassesMensagens();
            manterAccordionAberto();
        }

        if (successMessage || errorMessageToDelete) {
            $('.modal').modal('hide');
            flashContainer.innerHTML = flashMessages.innerHTML;
            ajustarClassesMensagens();
            manterAccordionAberto();
        }

        flashMessages.parentNode.removeChild(flashMessages);
    }

    const selectMember = document.getElementById("table-filter-member");
    const memberTable = document.getElementById("memberTable");
    const memberRows = memberTable.querySelectorAll("tbody tr");

    selectMember.addEventListener("keyup", (event) => {
        const value = event.target.value.toLowerCase();
        memberRows.forEach((row) => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(value) ? "table-row" : "none";
        });
    });

    const selectPayment = document.getElementById("table-filter-payment");
    const paymentTable = document.getElementById("paymentTable");
    const rowsPayment = paymentTable.querySelectorAll("tbody tr");

    selectPayment.addEventListener("keyup", (event) => {
        const value = event.target.value.toLowerCase();
        rowsPayment.forEach((row) => {
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
        const errorContainer = modal.querySelector(`#${containerId}`);
        errorContainer.innerHTML = messageHTML;
        $(modal).modal('show');
    }

    function preencherFormulario(cpf, nome, dataNascimento, tipo, endereco, telefone, email, plano) {
        const form = document.getElementById('add-member-form');
        if (form) {
            const cpfInput = form.querySelector('#cpf');
            if (cpfInput) cpfInput.value = cpf;

            const nomeInput = form.querySelector('#nome');
            if (nomeInput) nomeInput.value = nome;

            const dataNascimentoInput = form.querySelector('#data_nascimento');
            if (dataNascimentoInput) dataNascimentoInput.value = dataNascimento;

            const tipoInput = form.querySelector('#tipo');
            if (tipoInput) tipoInput.value = tipo;

            const enderecoInput = form.querySelector('#endereco');
            if (enderecoInput) enderecoInput.value = endereco;

            const telefoneInput = form.querySelector('#telefone');
            if (telefoneInput) telefoneInput.value = telefone;

            const emailInput = form.querySelector('#email');
            if (emailInput) emailInput.value = email;

            const planoInput = form.querySelector('#plano');
            if (planoInput) planoInput.value = plano;
        }
    }

    const addMemberModal = document.getElementById('addMemberModal');
    const form = document.getElementById('add-member-form');

    if (addMemberModal && form) {
        const modal = document.getElementById('addMemberModal');
        const errorContainer = modal.querySelector('#error-container-add');
        $(addMemberModal).on('hidden.bs.modal', function () {
            errorContainer.innerHTML = '';
            form.reset();
        });
    }


    document.querySelectorAll('.telefone-mask').forEach(function (telefoneInput) {
        telefoneInput.addEventListener('input', function (event) {
            let input = event.target.value.replace(/\D/g, '');
            input = input.substring(0, 11);

            const parte1 = input.substring(0, 2);
            const parte2 = input.substring(2, 7);
            const parte3 = input.substring(7, 11);

            if (input.length > 7) {
                event.target.value = `(${parte1}) ${parte2}-${parte3}`;
            } else if (input.length > 2) {
                event.target.value = `(${parte1}) ${parte2}`;
            } else if (input.length > 0) {
                event.target.value = `(${parte1}`;
            }
        });
    });

    document.querySelectorAll('.cpf-mask').forEach(function (cpfInput) {
        cpfInput.addEventListener('input', function (event) {
            let input = event.target.value.replace(/\D/g, '');
            input = input.substring(0, 11);

            const parte1 = input.substring(0, 3);
            const parte2 = input.substring(3, 6);
            const parte3 = input.substring(6, 9);
            const parte4 = input.substring(9, 11);

            if (input.length > 9) {
                event.target.value = `${parte1}.${parte2}.${parte3}-${parte4}`;
            } else if (input.length > 6) {
                event.target.value = `${parte1}.${parte2}.${parte3}`;
            } else if (input.length > 3) {
                event.target.value = `${parte1}.${parte2}`;
            } else if (input.length > 0) {
                event.target.value = `${parte1}`;
            }
        });
    });
});
