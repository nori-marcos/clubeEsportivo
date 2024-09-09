document.getElementById('btn-clear').addEventListener('click', function () {
    const modal = document.getElementById('addMemberModal');
    const errorContainer = modal.querySelector('#error-container-add');
    errorContainer.innerHTML = '';
    document.querySelectorAll('.form-control').forEach(input => input.value = '');
});

document.addEventListener('DOMContentLoaded', function () {

    restaurarEstadoAccordions();

    const accordionToggles = document.querySelectorAll('[data-toggle="collapse"]');

    accordionToggles.forEach(function (toggle) {
        toggle.addEventListener('click', function () {
            const targetAccordionId = toggle.getAttribute('data-target').substring(1); // remove o "#" do ID

            if (document.getElementById(targetAccordionId).classList.contains('show')) {
                removerEstadoAccordion(targetAccordionId);
            } else {
                salvarEstadoAccordion(targetAccordionId);
            }
        });
    });

    const submited_form = document.querySelector('form');
    if (submited_form) {
        submited_form.addEventListener('submit', function () {
            accordionToggles.forEach(function (toggle) {
                const targetAccordionId = toggle.getAttribute('data-target').substring(1);
                if (document.getElementById(targetAccordionId).classList.contains('show')) {
                    salvarEstadoAccordion(targetAccordionId);
                }
            });
        });
    }

    const flashMessages = document.getElementById('flash-messages');
    const flashContainer = document.getElementById('flash-container');

    if (flashMessages) {
        const successMessage = document.querySelector('.alert-success');
        const errorMessageToInsert = document.querySelector('.alert-danger-insert-member');
        const errorMessageToEdit = document.querySelector('.alert-danger-edit-member');
        const errorMessageToDelete = document.querySelector('.alert-danger-remove-member');

        if (errorMessageToInsert) {
            const cpf = errorMessageToInsert.getAttribute('data-cpf');
            const nome = errorMessageToInsert.getAttribute('data-nome');
            const dataNascimento = errorMessageToInsert.getAttribute('data-data_nascimento');
            const tipo = errorMessageToInsert.getAttribute('data-tipo');
            const endereco = errorMessageToInsert.getAttribute('data-endereco');
            const telefone1 = errorMessageToInsert.getAttribute('data-telefone1');
            const telefone2 = errorMessageToInsert.getAttribute('data-telefone2');
            const email = errorMessageToInsert.getAttribute('data-email');
            const plano = errorMessageToInsert.getAttribute('data-plano');
            const associadoTitular = errorMessageToInsert.getAttribute('data-associado_titular');
            preencherFormulario(cpf, nome, dataNascimento, tipo, endereco, telefone1, telefone2, email, plano, associadoTitular);
            mostrarErroModal('addMemberModal', 'error-container-add', flashMessages.innerHTML);
            ajustarClassesMensagens();
        }

        if (errorMessageToEdit) {
            const cpf = errorMessageToEdit.getAttribute('data-cpf');
            const nomeModal = `editMemberModal${cpf}`;
            mostrarErroModal(nomeModal, 'error-container-edit', flashMessages.innerHTML);
            ajustarClassesMensagens();
        }

        if (successMessage || errorMessageToDelete) {
            $('.modal').modal('hide');
            flashContainer.innerHTML = flashMessages.innerHTML;
            ajustarClassesMensagens();
        }

        flashMessages.parentNode.removeChild(flashMessages);
        fecharAlertasAutomaticamente();
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

    function ajustarClassesMensagens() {
        document.querySelectorAll('.alert').forEach((alert) => {
            const parts = alert.className.split('-');
            if (parts.length > 2) {
                alert.className = parts.slice(0, 2).join('-') + ' alert-dismissible fade show';
            }
        });
    }

    function salvarEstadoAccordion(accordionId) {
        let accordionsAbertos = JSON.parse(sessionStorage.getItem('accordionsAbertos')) || [];

        if (!accordionsAbertos.includes(accordionId)) {
            accordionsAbertos.push(accordionId);
            sessionStorage.setItem('accordionsAbertos', JSON.stringify(accordionsAbertos));
        }
    }

    function removerEstadoAccordion(accordionId) {
        let accordionsAbertos = JSON.parse(sessionStorage.getItem('accordionsAbertos')) || [];
        accordionsAbertos = accordionsAbertos.filter(id => id !== accordionId);
        sessionStorage.setItem('accordionsAbertos', JSON.stringify(accordionsAbertos));
    }

    function restaurarEstadoAccordions() {
        let accordionsAbertos = JSON.parse(sessionStorage.getItem('accordionsAbertos')) || [];

        accordionsAbertos.forEach(function (accordionId) {
            const accordionContent = document.getElementById(accordionId);
            if (accordionContent) {
                accordionContent.classList.add('show');
            }
        });
    }

    function mostrarErroModal(modalId, containerId, messageHTML) {
        const modal = document.getElementById(modalId);
        const errorContainer = modal.querySelector(`#${containerId}`);
        errorContainer.innerHTML = messageHTML;
        $(modal).modal('show');
    }

    function preencherFormulario(cpf, nome, dataNascimento, tipo, endereco, telefone1, telefone2, email, plano, associadoTitular) {
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

            if (tipo === "dependente") {
                const associadoTitularGroup = form.querySelector('#associado_titular_group');
                if (associadoTitularGroup) associadoTitularGroup.classList.remove('d-none');
            }

            const associadoTitularInput = form.querySelector('#associado_titular');
            if (associadoTitularInput) {
                associadoTitularInput.value = associadoTitular;
            }

            const enderecoInput = form.querySelector('#endereco');
            if (enderecoInput) enderecoInput.value = endereco;

            const telefoneInput = form.querySelector('#telefone1');
            if (telefoneInput) telefoneInput.value = telefone1;

            const telefone2Input = form.querySelector('#telefone2');
            if (telefone2Input) telefone2Input.value = telefone2;

            const emailInput = form.querySelector('#email');
            if (emailInput) emailInput.value = email;

            const planoInput = form.querySelector('#plano');
            if (planoInput) planoInput.value = plano;
        }
    }

    function fecharAlertasAutomaticamente() {
        const alerts = document.querySelectorAll('.alert-dismissible');

        alerts.forEach(function (alert) {
            setTimeout(function () {
                alert.classList.remove('show');
                alert.classList.add('fade');
                alert.style.display = 'none';
            }, 15000);
        });
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

    document.querySelectorAll('#tipo').forEach(function (tipoInput) {
        tipoInput.addEventListener('change', function (event) {
            const tipo = event.target.value.toLowerCase();
            const associadoTitularGroup = document.getElementById('associado_titular_group');
            const associadoTitular = document.getElementById('associado_titular');
            const associadoPlano = document.getElementById('plano');
            const planoHidden = document.getElementById('plano_hidden');
            if (tipo === "dependente") {
                associadoTitularGroup.classList.remove('d-none');
            } else {
                associadoTitularGroup.classList.add('d-none');
                associadoTitular.value = '';
                associadoPlano.removeAttribute('disabled');
                associadoPlano.value = '';
                planoHidden.value = '';
            }
        });
    });

    document.querySelectorAll('#associado_titular').forEach(function (titularInput) {
        titularInput.addEventListener('change', function (event) {
            const selectedOption = event.target.options[event.target.selectedIndex];
            const tipo = selectedOption.getAttribute('data-tipo');
            const associadoPlano = document.getElementById('plano');
            const planoHidden = document.getElementById('plano_hidden');
            associadoPlano.value = tipo.toLowerCase();
            associadoPlano.setAttribute('disabled', 'disabled');
            planoHidden.value = tipo.toLowerCase();
        });
    });

    document.querySelectorAll('[id^="edit-tipo-"]').forEach(function (tipoInput) {
        tipoInput.addEventListener('change', function (event) {
            const tipoId = event.target.id.split('-')[2];
            const tipo = event.target.value;
            const associadoTitularGroup = document.getElementById('edit-associado_titular_group-' + tipoId);
            const associadoTitular = document.getElementById('edit-associado_titular-' + tipoId);
            const associadoPlano = document.getElementById('edit-plano-' + tipoId);
            const planoHidden = document.getElementById('edit-plano_hidden-' + tipoId);

            if (tipo === "dependente") {
                associadoTitularGroup.classList.remove('d-none');
            } else {
                associadoTitularGroup.classList.add('d-none');
                associadoTitular.value = '';
                associadoPlano.removeAttribute('disabled');
                associadoPlano.value = '';
                planoHidden.value = '';
            }
        });
    });

    document.querySelectorAll('[id^="edit-associado_titular-"]').forEach(function (titularInput) {
        titularInput.addEventListener('change', function (event) {
            const titularId = event.target.id.split('-')[2];
            const selectedOption = event.target.options[event.target.selectedIndex];
            const tipo = selectedOption.getAttribute('data-tipo');
            const associadoPlano = document.getElementById('edit-plano-' + titularId);
            const planoHidden = document.getElementById('edit-plano_hidden-' + titularId);

            associadoPlano.value = tipo.toLowerCase();
            associadoPlano.setAttribute('disabled', 'disabled');
            planoHidden.value = tipo;
        });
    });

});
