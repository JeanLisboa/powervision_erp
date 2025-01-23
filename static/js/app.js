const canvas = document.getElementById('canvas');
let nodes = [];

// Função para adicionar um novo nó
function addNode() {
  const node = document.createElement('div');
  node.className = 'node';
  node.contentEditable = true; // Permite edição de texto
  node.style.top = `${Math.random() * 400}px`;
  node.style.left = `${Math.random() * 600}px`;

  // Torna o nó arrastável
  node.draggable = true;
  node.ondragstart = (e) => {
    e.dataTransfer.setData('text/plain', e.target.id);
  };
  node.ondragend = (e) => {
    e.target.style.top = `${e.pageY - 25}px`;
    e.target.style.left = `${e.pageX - 25}px`;
  };

  canvas.appendChild(node);
  nodes.push({ id: node.id, x: node.style.left, y: node.style.top, text: '' });
}

// Função para salvar o diagrama
function saveDiagram() {
  const nodeData = [...canvas.querySelectorAll('.node')].map((node) => ({
    id: node.id,
    x: node.style.left,
    y: node.style.top,
    text: node.innerText,
  }));
  localStorage.setItem('diagram', JSON.stringify(nodeData));
  alert('Diagrama salvo!');
}

// Função para carregar o diagrama salvo
function loadDiagram() {
  const savedNodes = JSON.parse(localStorage.getItem('diagram'));
  if (!savedNodes) return alert('Nenhum diagrama salvo encontrado!');

  canvas.innerHTML = ''; // Limpa o canvas atual
  savedNodes.forEach((data) => {
    const node = document.createElement('div');
    node.className = 'node';
    node.contentEditable = true;
    node.style.left = data.x;
    node.style.top = data.y;
    node.innerText = data.text;

    canvas.appendChild(node);
  });
  alert('Diagrama carregado!');
}
