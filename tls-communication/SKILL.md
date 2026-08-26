---
name: tls-communication
description: Implemente, mantenha e diagnostique comunicação TLS/mTLS em clientes Node.js, inclusive handshakes TLS 1.2 manuais exigidos por integrações legadas. Não use para endpoints HTTP comuns que possam usar a pilha TLS nativa sem restrições especiais.
---

# Comunicação TLS

Construa comunicação segura e interoperável, preservando o contrato de transporte e os requisitos do servidor. Comece identificando versão TLS, suites aceitas, autenticação de cliente, cadeia de certificados, SNI, timeout e a necessidade real de renegociação.

## Escolha da abordagem

- Prefira `node:tls` ou o cliente HTTP do runtime quando a integração for compatível. Configure protocolo mínimo/máximo, validação do servidor, SNI e certificado de cliente pelos mecanismos suportados, sem desabilitar a validação de certificado para contornar erros.
- Implemente TLS sobre `node:net` somente quando houver um requisito de compatibilidade que a pilha nativa não atende — por exemplo, uma renegociação mTLS legada iniciada pelo servidor. Declare no código e na entrega qual requisito justifica essa exceção.
- Mantenha as capacidades negociadas explícitas. Um cliente de handshake manual não deve aceitar silenciosamente cipher suite, versão ou ordem de mensagens que não tenha implementado e testado.

## Cliente TLS 1.2 manual

Para criar, alterar ou investigar um cliente com o perfil `TLS_RSA_WITH_AES_128_GCM_SHA256` e mTLS, leia [o guia do perfil TLS 1.2 manual](references/tls12-manual-mtls.md). Ele registra as invariantes extraídas da implementação de referência de NF-e/SEFAZ.

Ao adaptar esse perfil:

1. Separe framing de records, codec de handshake, derivação criptográfica, máquina de estados do handshake e transporte de aplicação. Não misture parsing HTTP/SOAP com lógica TLS.
2. Preserve um transcript somente de mensagens de handshake, na ordem transmitida/recebida. Calcule `CertificateVerify` e `Finished` a partir do ponto correto do transcript.
3. Use cifras independentes para escrita e leitura. Cada direção mantém seu próprio número de sequência; em AES-GCM, ele integra AAD e nonce explícito.
4. Trate fragmentação e coalescência do TCP: um `data` pode conter parte de um record ou vários records; um record de handshake pode conter várias mensagens.
5. Aplique limites e validações antes de indexar buffers ou decifrar payloads: tamanho do record, campos de 24 bits, presença de certificado e tipos esperados. Converta falhas de protocolo em erros de integração compreensíveis, sem vazar material criptográfico.
6. Em renegociação, mantenha as cifras antigas para proteger o handshake que cria as novas e só substitua o estado após validar o `Finished` do servidor.

## Certificados, logs e operação

- Receba chaves/certificados por uma abstração de fonte de certificado quando o material vier de A3/HSM. Solicite a assinatura ao provedor; não exporte chave privada nem registre DER, segredo pré-mestre, chaves de sessão, IVs ou `verify_data`.
- Feche o socket em qualquer falha do handshake e sempre ao encerrar a requisição. Configure timeout de conexão e remova listeners temporários para evitar vazamentos e corridas entre leituras.
- Registre host, porta, tipo de record/mensagem e fase do handshake apenas em modo de depuração controlado. Preserve erros de `alert`, timeout, autenticação e resposta HTTP como causas distinguíveis.
- Teste records fragmentados/coalescidos, nonce/AAD e contador de sequência, derivação PRF, ordem e transcript do handshake, `Finished` inválido, renegociação e limpeza de socket. Simule o transporte; não use certificados ou serviços reais nos testes unitários.

## Diagnóstico

Antes de mudar o código, determine em qual camada ocorre a falha: conexão TCP, ClientHello/ServerHello, cadeia/certificado de cliente, troca de chaves, `Finished`, renegociação ou HTTP sobre TLS. Compare versão, suite, SNI, cadeia e sequência observada com a exigida pelo servidor. Não proponha reduzir a segurança como solução.
