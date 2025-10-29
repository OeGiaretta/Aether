# 📖 Manual do Usuário - AETHER Dashboard

> **Guia completo para utilização do sistema de monitoramento automotivo**

---

## 🌟 Visão Geral

O **AETHER Dashboard** é um sistema completo de monitoramento automotivo que permite visualizar dados de sensores do veículo em tempo real através de uma interface web moderna e intuitiva.

### 🎯 Funcionalidades Principais
- **Monitoramento em tempo real** de sensores automotivos
- **Gauges visuais interativos** para dados críticos
- **Gráficos de histórico** e análise de tendências
- **Sistema de alertas** para condições críticas
- **Armazenamento de dados** para análise posterior
- **Interface responsiva** adaptável a diferentes dispositivos

---

## 🖥️ Interface Principal

### 📊 Dashboard Principal
O dashboard é dividido em seções principais:

#### 1. **Sidebar (Painel Lateral)**
- **🌌 Logo e título** do AETHER
- **⚙️ Configurações** de refresh e intervalos
- **📊 Filtros de sensores** para personalizar visualização
- **📈 Estatísticas** dos dados históricos
- **💾 Informações de armazenamento**
- **🚨 Alertas** em tempo real

#### 2. **Métricas Principais**
Cards com os dados mais importantes:
- **RPM do Motor** - rotações por minuto
- **Velocidade** - km/h atual
- **Temperatura do Motor** - °C do líquido de arrefecimento
- **Acelerador** - posição do pedal em %

#### 3. **Detalhes do Motor**
Informações secundárias:
- **Carga do Motor** - percentual de carga
- **Temperatura de Admissão** - °C do ar aspirado
- **Pressão MAP** - pressão do coletor em kPa
- **Nível de Combustível** - percentual do tanque

#### 4. **Gauges Visuais**
Indicadores circulares interativos:
- **Gauge RPM** - com cores dinâmicas (verde/amarelo/vermelho)
- **Gauge Velocidade** - com alertas de velocidade
- **Gauge Temperatura** - com zonas de temperatura
- **Gauges Percentuais** - para acelerador, carga e combustível

---

## 🎛️ Controles e Configurações

### 🔄 Controles de Refresh
- **Auto-refresh:** Ativa/desativa atualização automática
- **Intervalo:** Configura tempo entre atualizações (1-30 segundos)
- **Atualizar Dados:** Botão para refresh manual
- **Limpar Histórico:** Remove dados históricos da memória

### 📊 Filtros de Sensores
- **Seleção múltipla** de sensores para exibir
- **Sensores disponíveis:** RPM, velocidade, temperatura, etc.
- **Aplicação em tempo real** nos gráficos

### 📈 Estatísticas
- **Período:** Últimos 7 dias por padrão
- **Métricas:** Média, mínimo, máximo, desvio padrão
- **Sensores principais:** RPM, velocidade, temperatura, acelerador

---

## 📊 Visualizações e Gráficos

### 📈 Gráfico de Histórico
- **Linha temporal** dos sensores selecionados
- **Zoom e pan** interativos
- **Legenda** com cores dos sensores
- **Eixos** com unidades apropriadas

### 🔗 Matriz de Correlação
- **Heatmap** mostrando correlações entre sensores
- **Cores:** Verde (correlação positiva), Vermelho (negativa)
- **Valores numéricos** de correlação
- **Identificação** de padrões nos dados

---

## 🚨 Sistema de Alertas

### ⚠️ Alertas Automáticos
O sistema monitora continuamente e alerta sobre:

#### **RPM Alto** (🟡 Warning)
- **Condição:** RPM > 6000
- **Ação:** Alerta visual na sidebar
- **Cor:** Amarelo

#### **Temperatura Alta** (🔴 Error)
- **Condição:** Temperatura > 100°C
- **Ação:** Alerta crítico
- **Cor:** Vermelho

#### **Velocidade Alta** (🟡 Warning)
- **Condição:** Velocidade > 120 km/h
- **Ação:** Alerta de velocidade
- **Cor:** Amarelo

#### **Combustível Baixo** (🟡 Warning)
- **Condição:** Nível < 20%
- **Ação:** Alerta de abastecimento
- **Cor:** Amarelo

### ✅ Status Normal
- **Condição:** Todos os sensores dentro dos limites
- **Indicador:** "Sistema Operacional"
- **Cor:** Verde

---

## 💾 Gerenciamento de Dados

### 📁 Armazenamento Automático
- **Formato:** CSV com timestamp
- **Localização:** `data/telemetry_data.csv`
- **Retenção:** 100 registros em memória, ilimitado em arquivo
- **Backup:** Rotação automática de logs

### 📊 Informações de Armazenamento
- **Tamanho dos arquivos** (CSV, logs)
- **Número de registros** armazenados
- **Período dos dados** mais antigos e recentes
- **Fontes de dados** utilizadas

### 📤 Exportação de Dados
- **Formato CSV:** Dados brutos para análise
- **Formato JSON:** Para integração com outros sistemas
- **Formato Excel:** Para relatórios e apresentações

---

## 🎨 Personalização

### 🎯 Gauges Personalizáveis
- **Cores dinâmicas** baseadas nos valores
- **Escalas adaptáveis** por tipo de sensor
- **Thresholds configuráveis** para alertas
- **Animações suaves** nas transições

### 📱 Interface Responsiva
- **Desktop:** Layout completo com sidebar
- **Tablet:** Layout adaptado para tela média
- **Mobile:** Interface otimizada para toque

---

## 🔧 Modos de Operação

### 🎭 Modo Mock (Padrão)
- **Dados simulados** para demonstração
- **Geração realística** de valores
- **Funciona sem hardware** OBD-II
- **Ideal para testes** e desenvolvimento

### 🔌 Modo OBD-II Real
- **Conexão real** com adaptador ELM327
- **Dados autênticos** do veículo
- **Fallback automático** para mock se falhar
- **Configuração** via variáveis de ambiente

---

## 📱 Navegação e Atalhos

### 🖱️ Navegação Básica
- **Scroll:** Navegar pelas seções
- **Clique:** Interagir com controles
- **Hover:** Ver informações adicionais
- **Zoom:** Nos gráficos interativos

### ⌨️ Atalhos do Streamlit
- **R:** Refresh manual da página
- **Ctrl+R:** Atualizar dados
- **Esc:** Fechar modais e popups

---

## 🆘 Solução de Problemas

### ❌ Problemas Comuns

#### **Dashboard não carrega**
- Verificar se Streamlit está rodando
- Confirmar porta 8501 disponível
- Checar logs de erro no terminal

#### **Dados não atualizam**
- Verificar conexão OBD-II
- Confirmar auto-refresh ativado
- Checar logs de erro

#### **Gráficos não aparecem**
- Verificar se há dados históricos
- Confirmar sensores selecionados
- Checar console do navegador

#### **Alertas não funcionam**
- Verificar configurações de threshold
- Confirmar dados sendo recebidos
- Checar logs do sistema

### 🔍 Logs e Debug
- **Logs do sistema:** `logs/aether.log`
- **Logs de erro:** `logs/aether_errors.log`
- **Console do navegador:** F12 → Console
- **Terminal:** Verificar saída do Streamlit

---

## 📚 Recursos Adicionais

### 🔗 Links Úteis
- **Documentação técnica:** [docs/](docs/)
- **Código fonte:** [GitHub](https://github.com/OeGiaretta/Aether)
- **Issues e suporte:** [GitHub Issues](https://github.com/OeGiaretta/Aether/issues)

### 📖 Documentação Relacionada
- **Guia de instalação:** [INSTALACAO.md](INSTALACAO.md)
- **Documentação técnica:** [TECNICA.md](TECNICA.md)
- **API Reference:** [API.md](API.md)

---

## 🎉 Conclusão

O AETHER Dashboard oferece uma experiência completa de monitoramento automotivo com interface moderna e funcionalidades avançadas. Explore todas as funcionalidades e personalize conforme suas necessidades!

**🚀 Aproveite o monitoramento inteligente do seu veículo!**
