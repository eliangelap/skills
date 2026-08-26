# Perfil TLS 1.2 manual com mTLS

Esta referência descreve o perfil usado pelo cliente de NF-e/SEFAZ em `src/@core/modules/nfeImport/infra/tls`. É uma base para integrações legadas específicas, não uma receita para implementar um cliente TLS genérico ou moderno.

## Perfil suportado

- TLS 1.2 (`0x0303`), com SNI, `signature_algorithms` RSA/SHA-256 e extensão de renegociação segura.
- Uma única suite: `TLS_RSA_WITH_AES_128_GCM_SHA256` (`0x009c`). A suite deve ser confirmada no `ServerHello`.
- Troca de chave RSA PKCS#1 v1.5: o pré-mestre começa com a versão TLS e contém 46 bytes aleatórios; é cifrado com a chave pública do certificado folha do servidor.
- PRF TLS 1.2 com HMAC-SHA-256: `master secret` recebe `client_random || server_random`; `key expansion` recebe `server_random || client_random`.
- AES-128-GCM: 16 bytes de chave, IV fixo de 4 bytes e nonce explícito de 8 bytes. O AAD tem `sequence_number || content_type || TLS_version || plaintext_length`.

Não amplie suites, versões ou extensões sem modelar, implementar e testar todo o fluxo correspondente.

## Handshake inicial

1. Abra TCP com timeout e envie `ClientHello` em record de handshake em claro. Inclua um `client_random` de 32 bytes e SNI.
2. Leia records incrementalmente até obter, nessa ordem, `ServerHello`, `Certificate` e `ServerHelloDone`. O parser deve separar múltiplas mensagens de handshake no mesmo record.
3. Extraia `server_random`, `session_id`, suite e certificado folha. Rejeite suite inesperada e certificado ausente ou malformado.
4. Se o servidor não solicitar certificado nessa etapa, envie `ClientKeyExchange`, derive `master_secret` e as cifras das duas direções, envie `ChangeCipherSpec`, então `Finished` do cliente cifrado.
5. Espere `ChangeCipherSpec` do servidor e `Finished` cifrado. Decifre, valide o tipo da mensagem e compare o `verify_data` esperado em tempo constante quando o ambiente permitir.

O transcript inclui todas as mensagens de handshake enviadas e recebidas, mas não `ChangeCipherSpec`. O `Finished` do cliente é calculado antes de ser acrescentado ao transcript; o `Finished` do servidor é validado contra esse transcript que já contém o `Finished` do cliente.

## mTLS por renegociação

O servidor pode enviar `HelloRequest` cifrado depois de começar a resposta HTTP. Preserve qualquer `ApplicationData` recebido enquanto trata a renegociação.

1. Decifre `HelloRequest` com a cifra de leitura atual e crie um novo transcript.
2. Envie `ClientHello` cifrado pela cifra de escrita atual, reutilizando `session_id` e levando o `verify_data` do cliente anterior em `renegotiation_info`.
3. Espere `ServerHello`, `Certificate`, `CertificateRequest` e `ServerHelloDone`, todos ainda protegidos pelas cifras antigas.
4. Peça a cadeia DER e a assinatura do hash do transcript à fonte de certificado usando seu alias. Envie `Certificate`, `ClientKeyExchange`, `CertificateVerify`, `ChangeCipherSpec` e `Finished` sob a proteção aplicável.
5. Valide o `Finished` do servidor e somente então substitua `session_id`, `verify_data`, cifra de escrita e cifra de leitura.

O adaptador de certificado precisa oferecer, no mínimo, operações assíncronas para obter a cadeia em DER e assinar o hash SHA-256 do transcript. O TLS nunca deve depender de acesso direto a uma chave privada A3/HSM.

## Framing, transporte e HTTP

Um record TLS tem cabeçalho de 5 bytes: tipo, versão e comprimento de 16 bits. Acumule bytes TCP até haver o record completo, consuma-o do buffer e mantenha o excedente para a próxima leitura. Para cada record protegido, use o `ContentType` que corresponde ao payload ao cifrar/decifrar, pois ele participa do AAD.

Quando HTTP/1.1 for transportado sobre o canal:

- construa `Content-Length` em bytes UTF-8, não em caracteres;
- aceite somente resposta de status esperada;
- trate `Content-Length` e `Transfer-Encoding` como mutuamente exclusivos;
- valide a estrutura de `chunked`, inclusive CRLF e trailers, antes de devolver o corpo;
- finalize a conexão após a resposta quando o protocolo da integração usar `Connection: close`.

## Mapa de componentes da referência

| Responsabilidade | Arquivo |
| --- | --- |
| Constantes do protocolo | `protocol.constants.ts` |
| Framing incremental de records | `record.reader.ts` |
| Codec de handshake | `handshake.codec.ts` |
| PRF e derivação de chaves | `prf.ts` |
| AES-GCM por direção | `gcm.record.cipher.ts` |
| Handshake inicial e finalização | `tls.handshake.initial.ts`, `tls.handshake.finish.ts` |
| Renegociação mTLS | `tls.handshake.renegotiation.ts` |
| Socket e ciclo de records | `tls12.client.ts`, `tls12.connection.ts` |
| SOAP/HTTP sobre TLS | `soap.client.ts` |

Ao alterar qualquer componente, localize e atualize o teste unitário de mesmo escopo em `__test__/`.
