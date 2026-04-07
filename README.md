# 🔒 Sistema de Proctoring v0.3

Sistema de monitoramento de integridade acadêmica com logs criptografados, para consultas de professores e tutores, os auxiliando de monitoramento de provas/testes online de alunos realizados, visando privacidade, segurança, proteção, confidencialidade e respeito a todas as normas de LGPD para estruturação desse projeto visando o meio educacional.

O projeto foi visado para pensar na vigilância do conhecimento nos ambientes educacionais, para com alunos e até professores para evitar que ocorra métodos de trapacear, burlar, colar e printar.

O intuito desse projeto não é de espionar em si, mas apenas de melhoria de monitoramento em aplicações de atividades online. Pois todos nós sabemos que apenas copiar e colar, não enriquece e muito menos desenvolve nosso conhecimento e aprendizagem. Por isso esse método criado é para trazer esse tipo de prevenção para evitar qualquer tipo de trapaça para efetuar um certificado ou uma pontuação melhor.

"Precisamos de mentes, projetos e pessoas brilhantes de bastante inteligencia, com capacidade de criar e melhorar as coisas, e não apenas o mais do que já existe em todo lugar."


## Video de demonstração de projeto
https://www.linkedin.com/posts/denundng_projeto-de-estudo-e-pr%C3%A1tica-de-proctoring-activity-7445875733304057856-xCOK?utm_source=social_share_send&utm_medium=member_desktop_web&rcm=ACoAAFyPfE4BrhkcvOfPsTevdRj97apbqYoF7xw


## 🚀 Instalação

```bash
# Windows
instalar.bat

# Linux/Mac
pip install -r requirements.txt

# 🔐 SEGURANÇA E ACESSO AOS LOGS

## Como Deve Funcionar a Proteção

1. **Durante a Prova:**
   - Todos os logs são salvos em memória
   - Screenshots são salvos temporariamente

2. **Ao Finalizar:**
   - Logs e screenshots são compactados em um arquivo ZIP
   - O ZIP é criptografado com AES-256
   - Apenas a senha do ADM pode extrair

3. **Acesso do Administrador:**
   - Use a ferramenta `utils/extract_logs.py`
   - Ou use 7-Zip / WinRAR com a senha

4. **Política de Retenção**
   - Logs devem ser mantidos por 180 dias no máximo. (configurável)
   - Após esse período, devem ser apagados (LGPD)
   - Mas atualmente está codado para ser excluído assim que executa novamente. (configurável)
   - Apenas pessoal autorizado pode acessar
	
## Senha Padrão
