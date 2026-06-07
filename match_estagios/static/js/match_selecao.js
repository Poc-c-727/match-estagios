document.addEventListener("DOMContentLoaded", function() {
    const selectVagas = document.querySelectorAll('.select-vaga-match');

    selectVagas.forEach(select => {
        select.addEventListener('change', function() {
            const idEstudante = this.getAttribute('data-candidato-id');
            const idVagaSelecionada = this.value;
            const form = document.getElementById(`form-like-${idEstudante}`);
            const btnSubmit = form.querySelector('.btn-curtir-submit');

            if (idVagaSelecionada) {
                let actionUrl = form.getAttribute('action');
                
                // Substitui dinamicamente o trecho da URL pelo ID da vaga escolhida
                actionUrl = actionUrl.replace(/\/vagas\/[^\/]+\/candidatos/, `/vagas/${idVagaSelecionada}/candidatos`);
                
                form.setAttribute('action', actionUrl);
                btnSubmit.removeAttribute('disabled'); // Ativa o botão de curtir
            }
        });
    });
});