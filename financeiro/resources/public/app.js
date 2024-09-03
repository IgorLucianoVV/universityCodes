const jsonData = {
  "indice": 1,
  "nonce": 46499,
  "dados": "30323",
  "hash-anterior": "d3776120d03b18cff8837417b248d88ab0d457c0ea769459d8f7ff6009b97f85",
  "hash": "0000eaa0229ce3aed7f17bc087111ad8db83516d2353f2e8a2894e0cf05b151d"
};

function syntaxHighlight(json) {
  if (typeof json != 'string') {
       json = JSON.stringify(json, undefined, 2);
  }
  json = json.replace(/&/g, '&').replace(/</g, '<').replace(/>/g, '>');
  return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
      var cls = 'json-number';
      if (/^"/.test(match)) {
          if (/:$/.test(match)) {
              cls = 'json-key';
          } else {
              cls = 'json-string';
          }
      } else if (/true|false/.test(match)) {
          cls = 'json-boolean';
      } else if (/null/.test(match)) {
          cls = 'json-null';
      }
      return '<span class="' + cls + '">' + match + '</span>';
  });
}

document.getElementById('json-container').innerHTML = syntaxHighlight(jsonData);

async function transferToBlockchain() {
  try {
    const response = await fetch('/transacoes');
    const data = await response.json();

    if (data.transacoes.length === 0) {
      alert('Não há transações para minerar.');
      return;
    }

    const todasTransacoes = data.transacoes.map(transaction => ({
      tipo: transaction.tipo,
      valor: transaction.valor
    }));

    const blocoDados = { transacoes: todasTransacoes };

    const responseBlockchain = await fetch('/blockchain/transacao', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(blocoDados)
    });

    if (responseBlockchain.ok) {
      alert('Todas as transações foram transferidas para a blockchain com sucesso!');
      fetchBlockchain(); // Atualiza a exibição da blockchain
    } else {
      const error = await responseBlockchain.json();
      alert(`Erro ao adicionar transações na blockchain: ${error.mensagem}`);
    }
  } catch (error) {
    console.error('Erro ao transferir transações para a blockchain:', error);
    alert('Erro ao transferir transações para a blockchain. Verifique o console para mais detalhes.');
  }
}


async function addTransactionToBlockchain(tipo, valor) {
try {
  const newTransaction = { transacao: tipo, valor };
  const response = await fetch('/blockchain/transacao', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(newTransaction)
  });

  if (!response.ok) {
    const error = await response.json();
    alert(`Erro ao adicionar transação na blockchain: ${error.mensagem}`);
  }
} catch (error) {
  console.error('Erro ao adicionar transação na blockchain:', error);
  alert('Erro ao adicionar transação na blockchain. Verifique o console para mais detalhes.');
}
}


async function fetchTransactions() {
try {
  const response = await fetch('/transacoes');
  const data = await response.json();
  const transactionsList = document.getElementById('transactions');
  transactionsList.innerHTML = '';

  data.transacoes.forEach(transaction => {
    const li = document.createElement('li');
    li.textContent = `${transaction.tipo}: R$ ${transaction.valor}`;
    transactionsList.appendChild(li);
  });
} catch (error) {
  console.error('Erro ao buscar transações:', error);
  alert('Erro ao buscar transações. Verifique o console para mais detalhes.');
}
}

async function fetchBalance() {
try {
  const response = await fetch('/saldo');
  const data = await response.json();
  var balanceValue = data.saldo;
  document.getElementById('balance').textContent = 'R$ ' + balanceValue.toFixed(2);
} catch (error) {
  console.error('Erro ao buscar saldo:', error);
  alert('Erro ao buscar saldo. Verifique o console para mais detalhes.');
}
}

async function addTransaction() {
try {
  const valor = parseFloat(document.getElementById('valor').value);
  const tipo = document.getElementById('tipo').value;

  if (!valor || !tipo) {
    alert('Por favor, preencha todos os campos.');
    return;
  }

  const newTransaction = { valor, tipo };
  const response = await fetch('/transacoes', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(newTransaction)
  });

  if (response.ok) {
    document.getElementById('valor').value = '';
    document.getElementById('tipo').value = 'receita';
    fetchTransactions();
    fetchBalance();
  } else {
    const error = await response.json();
    alert(`Erro ao adicionar transação: ${error.mensagem}`);
  }
} catch (error) {
  console.error('Erro ao adicionar transação:', error);
  alert('Erro ao adicionar transação. Verifique o console para mais detalhes.');
}
}

function showTransactionForm() {
const form = document.getElementById('transaction-form');
form.style.display = 'block';
}

async function fetchBlockchain() {
  try {
    const response = await fetch('/blockchain');
    const data = await response.json();
    const blockchainElement = document.getElementById('blockchain');
    blockchainElement.innerHTML = ''; // Limpa o conteúdo anterior

    data.blockchain.forEach((block, index) => {
      const blockDiv = document.createElement('div');
      blockDiv.classList.add('block');

      const blockIndex = document.createElement('h3');
      blockIndex.textContent = `Bloco ${index}`;
      blockDiv.appendChild(blockIndex);

      const blockContent = document.createElement('div');
      blockContent.classList.add('block-content');

      const blockIndice = document.createElement('p');
      blockIndice.innerHTML = `<strong>Índice:</strong> ${block.indice}`;
      blockContent.appendChild(blockIndice);

      const blockNonce = document.createElement('p');
      blockNonce.innerHTML = `<strong>Nonce:</strong> ${block.nonce}`;
      blockContent.appendChild(blockNonce);

      const blockDados = document.createElement('p');
      blockDados.innerHTML = `<strong>Dados:</strong> ${block.dados}`;
      blockContent.appendChild(blockDados);

      const blockHashAnterior = document.createElement('p');
      blockHashAnterior.innerHTML = `<strong>Hash Anterior:</strong> ${block['hash-anterior']}`;
      blockContent.appendChild(blockHashAnterior);

      const blockHash = document.createElement('p');
      blockHash.innerHTML = `<strong>Hash:</strong> ${block.hash}`;
      blockContent.appendChild(blockHash);

      blockDiv.appendChild(blockContent);
      blockchainElement.appendChild(blockDiv);
    });
  } catch (error) {
    console.error('Erro ao buscar blockchain:', error);
    alert('Erro ao buscar blockchain. Verifique o console para mais detalhes.');
  }
}