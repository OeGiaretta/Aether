# 📚 Documentação AETHER Dashboard

> **Documentação completa do sistema de monitoramento automotivo**

---

## 🗂️ Índice da Documentação

### 📖 **Para Usuários**
| Documento | Descrição | Público-Alvo |
|-----------|-----------|--------------|
| **[📖 Manual do Usuário](MANUAL_USUARIO.md)** | Guia completo de utilização do dashboard | Usuários finais |
| **[🔧 Guia de Instalação](INSTALACAO.md)** | Instalação, configuração e troubleshooting | Usuários e desenvolvedores |

### 🔧 **Para Desenvolvedores**
| Documento | Descrição | Público-Alvo |
|-----------|-----------|--------------|
| **[⚙️ Documentação Técnica](TECNICA.md)** | Arquitetura, APIs e implementação | Desenvolvedores |
| **[📚 API Reference](API.md)** | Referência completa das APIs | Desenvolvedores |

### 📋 **Gerenciamento do Projeto**
| Documento | Descrição | Público-Alvo |
|-----------|-----------|--------------|
| **[🗺️ Roadmap](todo.md)** | Plano de desenvolvimento e progresso | Equipe e stakeholders |

---

## 🚀 Início Rápido

### Para Usuários
1. **Leia o [Guia de Instalação](INSTALACAO.md)** para configurar o sistema
2. **Consulte o [Manual do Usuário](MANUAL_USUARIO.md)** para aprender a usar o dashboard
3. **Execute o dashboard:**
   ```bash
   streamlit run ui/streamlit_dashboard.py
   ```

### Para Desenvolvedores
1. **Estude a [Documentação Técnica](TECNICA.md)** para entender a arquitetura
2. **Consulte a [API Reference](API.md)** para integração e extensão
3. **Acompanhe o [Roadmap](todo.md)** para ver o progresso do projeto

---

## 📊 Visão Geral do Sistema

### 🏗️ Arquitetura
```
┌─────────────────────────────────────────────────────────────┐
│                    CAMADA DE APRESENTAÇÃO                   │
├─────────────────────────────────────────────────────────────┤
│  Streamlit Dashboard  │  Terminal UI (TUI)  │  Future Mobile │
├─────────────────────────────────────────────────────────────┤
│                    CAMADA DE APLICAÇÃO                      │
├─────────────────────────────────────────────────────────────┤
│  Data Manager  │  Logger  │  Storage  │  Alert System      │
├─────────────────────────────────────────────────────────────┤
│                    CAMADA DE DADOS                          │
├─────────────────────────────────────────────────────────────┤
│  Mock OBD Reader  │  Real OBD Reader  │  CSV Storage       │
├─────────────────────────────────────────────────────────────┤
│                    CAMADA DE HARDWARE                       │
├─────────────────────────────────────────────────────────────┤
│  ELM327 Adapter  │  Bluetooth/USB  │  Vehicle ECU         │
└─────────────────────────────────────────────────────────────┘
```

### 🎯 Funcionalidades Principais
- **Monitoramento em tempo real** de sensores automotivos
- **Gauges visuais interativos** para dados críticos
- **Gráficos de histórico** e análise de tendências
- **Sistema de alertas** para condições críticas
- **Armazenamento de dados** para análise posterior
- **Interface responsiva** adaptável a diferentes dispositivos

---

## 🔧 Tecnologias Utilizadas

### Backend
- **Python 3.10+** - Linguagem principal
- **Streamlit** - Framework web
- **Plotly** - Visualizações interativas
- **Pandas** - Manipulação de dados
- **Python-OBD** - Comunicação OBD-II

### Frontend
- **Streamlit Components** - Interface web
- **Plotly Dash** - Gráficos interativos
- **HTML/CSS** - Componentes personalizados

### Storage & Logging
- **CSV** - Armazenamento de dados
- **Python Logging** - Sistema de logs
- **RotatingFileHandler** - Rotação de logs

---

## 📈 Status do Projeto

### ✅ **Concluído (75%)**
- ✅ Dashboard Streamlit completo
- ✅ Sistema de logs e storage
- ✅ Componentes visuais personalizados
- ✅ Sistema de alertas
- ✅ Documentação completa

### 🚧 **Em Desenvolvimento**
- 🔄 Terminal UI (TUI)
- 🔄 CLI e main.py
- 🔄 OBD real com fallback

### 📋 **Planejado**
- 📋 Testes automatizados
- 📋 Mobile app
- 📋 Wi-Fi OBD-II

---

## 🤝 Contribuindo

### Como Contribuir
1. **Fork** o repositório
2. **Crie uma branch** para sua feature
3. **Desenvolva** seguindo as diretrizes
4. **Teste** suas mudanças
5. **Documente** novas funcionalidades
6. **Abra um Pull Request**

### Diretrizes de Desenvolvimento
- **Type hints** obrigatórios
- **Docstrings** para funções públicas
- **Testes** para novas funcionalidades
- **Documentação** atualizada

---

## 📞 Suporte

### Canais de Suporte
- **GitHub Issues** - Bugs e feature requests
- **Documentação** - Guias e tutoriais
- **Código** - Exemplos e referências

### Reportar Problemas
1. **Verifique** a documentação primeiro
2. **Procure** em issues existentes
3. **Crie** uma nova issue com detalhes
4. **Inclua** logs e screenshots se possível

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License**.

```
MIT License © 2025 Eduh Giaretta

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 🎉 Agradecimentos

- **Comunidade Python** - pelas bibliotecas incríveis
- **Streamlit** - pelo framework web fantástico
- **Plotly** - pelas visualizações interativas
- **Contribuidores** - pelo feedback e sugestões

---

**🚀 Explore a documentação e aproveite o AETHER Dashboard!**
