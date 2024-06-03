function openPopup() {
    // Define as dimensões do popup
    var width = 600;
    var height = 400;
    // Calcula a posição para centralizar o popup
    var left = (screen.width / 2) - (width / 2);
    var top = (screen.height / 2) - (height / 2);

    // Abre o popup e captura a referência
    var popup = window.open("", "popup", "width=" + width + ",height=" + height + ",top=" + top + ",left=" + left);

    // Verifica se o popup foi aberto com sucesso
    if (popup) {
        // Faz uma requisição para obter o conteúdo de popup.html
        fetch('templates/popup.html')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao carregar o arquivo popup.html');
                }
                return response.text();
            })
            .then(html => {
                // Inclui o conteúdo de popup.html no popup
                popup.document.open();
                popup.document.write(html);
                popup.document.close();
            })
            .catch(error => {
                console.error('Erro:', error);
                alert('Não foi possível carregar o popup.');
            });
    } else {
        alert("O popup foi bloqueado pelo navegador. Por favor, permita popups para este site.");
    }
}
