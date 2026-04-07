# 🔒 Sistema de Proctoring v0.3

Sistema de monitoramento de integridade acadêmica com logs criptografados, para consultas de professores e tutores, os auxiliando de monitoramento de provas/testes online de alunos realizados, visando privacidade, segurança, proteção, confidencialidade e respeito a todas as normas de LGPD para estruturação desse projeto visando o meio educacional.

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
