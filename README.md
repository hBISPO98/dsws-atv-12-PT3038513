Módulo 2 ✉️

Evolução da aplicação web em Flask com transição para o serviço de e-mail seguro via Flask-Mail/SMTP (Gmail com Senha de App) e refinamento das notificações multi-destinatários. O grande objetivo desta versão foi garantir o envio estável de e-mails de notificação sem bloqueios de rede no PythonAnywhere, atendendo aos requisitos de notificação simultânea para o professor, o aluno e o novo usuário cadastrado).

---

🚀 O que mudou? (Refinamento da Infraestrutura de E-mail)

1. Transição de API Externa para Flask-Mail (SMTP via Gmail)

- Autenticação por Senha de App: Substituição da API do Mailgun pelo Relay SMTP do Gmail com autenticação de dois fatores e Senha de App, garantindo alta entregabilidade e contornando bloqueios de porta do servidor.


2. Notificação Multi-destinatários e Inclusão de Formulário
- Campo Dinâmico de E-mail: Inclusão de campo obrigatório e validado no formulário (`forms.py`) para capturar o e-mail do novo usuário cadastrado.


- Disparo Múltiplo e Simultâneo: A cada novo cadastro, a notificação é disparada simultaneamente para o e-mail do professor, o e-mail institucional do aluno e o e-mail informado no formulário.


- Formatação da Mensagem de Notificação: Organização do corpo da mensagem em HTML contendo os dados do aluno (Nome e Prontuário) e as informações do usuário recém-cadastrado.

---

⚙️ O que foi necessário implementar?

- Configuração de Ambiente (.env & config.py): Definição dinâmica do servidor SMTP (`smtp.gmail.com`), porta 587 com suporte a TLS e carregamento seguro de credenciais via variáveis de ambiente.


- Módulo de E-mail Refatorado (app/email.py): Disparo assíncrono via `Thread/Linha de execução` com tratamento de exceções *anti-crash* para garantir que o cadastro no banco de dados ocorra mesmo em caso de oscilações no envio do e-mail.


- Atualização do Fluxo e Interface (views.py e index.html): Captura dos dados do formulário e renderização atualizada com exibição da listagem de usuários e feedback de cadastro.

---

💡 Boas Práticas Adotadas

- Gestão Segura de Credenciais: Isolamento completo de senhas e dados sensíveis através de variáveis de ambiente (`.env`), impedindo o vazamento de chaves no repositório.


- Disparo Assíncrono com Tratamento Anti-crash: O envio de e-mails em threads separadas evita que a requisição web fique travada aguardando o servidor SMTP, enquanto o bloco `try-except` garante a resiliência do cadastro de usuários.

- Uso de listas para os destinatários no `app/email.py`, evitando erros de envio e garantindo que as mensagens cheguem corretamente sem falhas de protocolo.
